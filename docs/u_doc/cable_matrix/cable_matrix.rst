
Cable-Matrix Preparation
==========================================

Supported for nettoolkit version >= 1.5.0



Provide Necessary Input Parameters for cable matrix
---------------------------------------------------


First define a few static inputs. Modify as actual.

.. code-block:: python

  CLEAN_FILES_LIST = [          # Provide All devices -clean excel files in a list (with full path)
    'file1-clean.xlsx',
    'file2-clean.xlsx',
    'file3-clean.xlsx',
    'file4-clean.xlsx',
    'file5-clean.xlsx',
    # ... add all those need in drawing
  ]

-----

  
Generate cable-matrix Excel file
--------------------------------


Lets import necessary packages first. Followed by some steps to generate excel.


.. code-block:: python

  # --------------------------------------------
  # IMPORTS
  # --------------------------------------------
  from nettoolkit.pyVig import DFGen
  import nettoolkit.nettoolkit_db  as nt

  # --------------------------------------------
  # create DataFrame Generateion Object, and run  
  # --------------------------------------------
  DFG = DFGen(CLEAN_FILES_LIST)
  DFG.run()

  # ----------------------------------------------------------------------------------
  # arrange cabling tab in appropriate order [optional]
  # change keep_all_cols=True ( if want a few additional informations )
  # ----------------------------------------------------------------------------------
  DFG.arrange_cablings(keep_all_cols=False)

  # ----------------------------------------------------------------------------------
  # write data to Excel
  # ----------------------------------------------------------------------------------
  CABLE_MATRIX_OP_FILE = 'cable-matrix.xlsx'        # output Excel file with full path
  nt.write_to_xl(CABLE_MATRIX_OP_FILE, DFG.df_dict, index=False, overwrite=True)


-----

At this point a new Cable Matrix Excel file will be generated.  

