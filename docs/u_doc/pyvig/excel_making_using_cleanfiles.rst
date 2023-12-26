
Excel database Preparation - Auto Generate
==========================================


Supported for nettoolkit version >= 1.5.0


Add Custom Functions
--------------------


* As a First step to prepare the Excel database, there are a few pre-requisite custom inputs requires as below.
* All custom function definitions will be your own native as per your requirement.

-----

**1. Mandatory custom functions**

  1. Define a *custom function* to identify **hierarchical_order** of identified devices. 

     * This is to identify the (x, y) position of the items on plane.
     * Function should accept pandas Devices DataFrame as input, and work on (*nbr_hostname*, *hostname*) columns.
     * Function should able to return updated series of *identified hierarchical order numbers*.
     
  2. Define a *custom function* to identify **item** of identified devices.

     * This is to select the appropriate item from provided visio stencils.
     * Function should accept pandas DataFrame as input, and work on (*nbr_hostname*, *hostname*) columns.
     * Function should return updated series of *item_name* from stencils.

Once defined, import those functions.

.. code-block:: python

  # ----------------------------------------------------------------------------------
  # import Mandatory Custom Functions (names can be arbitrary)
  # ----------------------------------------------------------------------------------
  from custom.custom_pyvig.general import get_hierarchical_order_series, get_sw_type_series



-----

**2. Optional custom functions**

* Use this step if want to add more data to device details, apart from hostname
* Define a few custom functions to derive the additional device details, Example as Management IP Address.
* All such functions should accept keyword arguments and process input data to derive the necessary detail. one of important argument is var_df DataFrame.
* All these functions should derive and return respective necessary device detail from input kwargs.

Once defined, import those functions.

.. code-block:: python

  # ----------------------------------------------------------------------------------
  # Optional Custom Functions import 
  # ----------------------------------------------------------------------------------
  from custom.custom_pyvig import get_dev_mgmt_ip



-----

**3. custom sheet filters**

* Use this step if you want to generate multi tab layout in visio. i.e. You want to split your data in to multiple tabs.
* If you want all data to be on a single page, than exclude this step.

* You need to define two custom functions such as: *add_sheet_filter_columns*, *get_sheet_filter_columns*.
* **add_sheet_filter_columns** will accept dictionary of DataFrames with key as 'Cablings' & 'Devices'. and updates the 'Cablings' DataFrame with additional (x, y) pair columns 
* **get_sheet_filter_columns** will accept dictionary of DataFrames with key as 'Cablings' & 'Devices'. and returns dictionary of filter columns, on how to segregate pages.

Import these functions.

.. code-block:: python

  # --------------------------------------------
  # Optional Custom sheet filters import
  # --------------------------------------------
  from custom.custom_pyvig import add_sheet_filter_columns, get_sheet_filter_columns


-----

A Lot of Custom Import happen So Far.

Feel Bored, Enough.  !!!

Lets start now working on visio project

-----




Provide Necessary Input Parameters for visio database preparation
-----------------------------------------------------------------


Lets start by defining a few static inputs. Modify these as needed. or exclude those which you want to go with default.

.. code-block:: python

  DEFAULT_STENCIL = 'My Shapes/Network and Peripherals.vssx'  # (optional, Default: None) Provide stencil name with full path 
  SPACING_X = 2      # horizontal spacing between two adjecent devices  (number, float )
  SPACING_Y = 2      # vertical spacing between two adjecent devices  (number, float)
  LINE_PATTERN_STYLE_SEPARATION_ON_COLUMN = 'int_filter'  # (optional, Default: None) Provide column name of clean file, based on which connectors should be separated
  LINE_PATTERN_STYLE_SHIFT = 2  # number by which connector style should be separated. (number)
  DEFAULT_CONNECTOR_TYPE = 'straight'      # connector/line type (options = 'curved', 'angled', 'straight')
  DEFAULT_LINE_COLOR = 'red'               # connector/line color
  DEFAULT_LINE_WT = 2                    # connector/line thickness (number)
  sheet_filter_dict = {'sheet_filters': {}}    # blank sheet filter dictionary initialization, it will be updated later stage.
  #
  # --- clean files to make cable matrix ---
  CLEAN_FILES_LIST = [          # Provide All devices list of clean excel files
    'file1-clean.xlsx',
    'file2-clean.xlsx',
    'file3-clean.xlsx',
    'file4-clean.xlsx',
    'file5-clean.xlsx',
    # ... add all those need in drawing
  ]

-----

  
Generate pyVig readable Excel file
-----------------------------------


Lets import packages first; than generate excel.


.. code-block:: python

  # --------------------------------------------
  # IMPORTS
  # --------------------------------------------
  from nettoolkit.pyVig import DFGen, pyVig
  import nettoolkit.nettoolkit_db  as nt

  # --------------------------------------------
  # create DataFrame Generateion Object  
  # --------------------------------------------
  DFG = DFGen(CLEAN_FILES_LIST)

  # ----------------------------------------------------------------------------------
  # add static attributes to object, (remove those which you want to go with default)
  # ----------------------------------------------------------------------------------
  DFG.custom_attributes(			
    default_stencil=DEFAULT_STENCIL,
    default_x_spacing=SPACING_X,
    default_y_spacing=SPACING_Y,
    line_pattern_style_separation_on=LINE_PATTERN_STYLE_SEPARATION_ON_COLUMN,
    line_pattern_style_shift_no=LINE_PATTERN_STYLE_SHIFT,
    connector_type=DEFAULT_CONNECTOR_TYPE,
    color=DEFAULT_LINE_COLOR,
    weight=DEFAULT_LINE_WT,
  )

  # ----------------------------------------------------------------------------------
  # add custom mandatory functions to object,	to decide on hierarchical order and items. 
  # we will use two custom functions which we imported above from custom module
  # ----------------------------------------------------------------------------------
  DFG.custom_functions(
    hierarchical_order=get_hierarchical_order_series,
    item=get_sw_type_series,
  )

  # ----------------------------------------------------------------------------------
  # add custom optional functions (if any)	to get any additional device informations. 
  # we will use those custom functions which we imported abve from custom module (add more as needed)
  # ----------------------------------------------------------------------------------
  DFG.custom_var_functions(
    ip_address=get_dev_mgmt_ip,
  )

  # ----------------------------------------------------------------------------------
  # Generate cable matrix Excel
  # ----------------------------------------------------------------------------------
  DFG.run()

  # ----------------------------------------------------------------------------------
  # update and get custom filter columns
  # we will use the two custom functions which we imported abve from custom module
  # ----------------------------------------------------------------------------------
  sheet_filter_dict = {}
  DFG.update(add_sheet_filter_columns)
  sheet_filter_dict['sheet_filters'] = get_sheet_filter_columns(DFG.df_dict)
  sheet_filter_dict['is_sheet_filter'] = True if sheet_filter_dict['sheet_filters'] else False 

  # ----------------------------------------------------------------------------------
  # Drop Points calculator
  # ----------------------------------------------------------------------------------
  DFG.calculate_cordinates(sheet_filter_dict=sheet_filter_dict['sheet_filters'])

  # ----------------------------------------------------------------------------------
  # Remove undefined cabling entries where device doesn't exist in devices tab
  # ----------------------------------------------------------------------------------
  DFG.remove_undefined_cabling_entries()

  # ----------------------------------------------------------------------------------
  # arrange cabling tab to appropriate order
  # ----------------------------------------------------------------------------------
  DFG.arrange_cablings(keep_all_cols=True)

  # ----------------------------------------------------------------------------------
  # write data to Excel (change filename if you want)
  # ----------------------------------------------------------------------------------
  CABLE_MATRIX_OP_FILE = 'pyVig_supported_cablematrix.xlsx'   # output Excel file with full path
  nt.write_to_xl(CABLE_MATRIX_OP_FILE, DFG.df_dict, index=False, overwrite=True)


-----

At this point a new Cable Matrix Excel file will be generated.  
We are going to use it for the generation of the visio.


Script will continue on next step to generate the visio file using the above cable matrix excel file.
Stay Tuned!!!
