
Excel database Preparation Guidelines
=====================================


* Requirement is to have an Excel database in appropriate format.
* Two tabs as per given below names are mandatory.

  #. ``Devices`` It defines all images/icons related to be placed on the visio page.
  #. ``Cablings`` It defines all cabling/connectivity related on placed images/icons.


There is a Sample Excel given at end of this page. Download and modify it as your requirement.

Read Below to understand it.

-----

Mandatory columns
-----------------

**Devices Tab**
^^^^^^^^^^^^^^^


     #. ``hostname`` Define hostname / identity of device. *( No Exception and column name modification not allowed )*
     #. ``x-axis`` Define horizontal position of device. *( column name can be changed by defining var argument `x` in input)*
     #. ``y-axis`` Define vertical position of device. *( column name can be changed by defining var argument `y` in input)*

**Cablings Tab**
^^^^^^^^^^^^^^^

     #. ``a_device`` Define identity of a-end device for connectivity. *(column name can be changed by defining var argument `dev_a` in input)*
     #. ``b_device`` Define identity of b-end device for connectivity. *(column name can be changed by defining var argument `dev_b` in input)*

-----

Optional columns
----------------



**Devices Tab**
^^^^^^^^^^^^^^^

     #. ``stencil`` Define stencil file of individual device *( column name modification not allowed )*
     #. ``item`` Define stencil name/number from stencil *( column name modification not allowed )*
     #. ``iconHeight`` Define resizing of icon vertically *( column name modification not allowed )*
     #. ``iconWidth`` Define resizing of icon horizontaly *( column name modification not allowed )*
     #. There can be **n-number of columns** for additional device details, with any column-names

        * **Example**: *(device_model, serial_number, ip_address, rack_details, . . . and many more ).*
        * As many of these columns information can be added to device information, by defining them to var argument list ``cols_to_merge``.
        * Arrange these in list as desired sequence in output.


**Cablings Tab**
^^^^^^^^^^^^^^^

     #. ``aport`` Define port number for a-end device. Will appear on middle. *( column name modification not allowed )*
     #. ``connector_type`` Define connector type. (default: *straight*, other options: *angled, curved*). *( column name modification not allowed )*
     #. ``color`` Define connector color. (default: *blue*). *( column name modification not allowed )*
     #. ``weight`` Define connector weigth/thickness. (default: *3*). *( column name modification not allowed )*
     #. ``pattern`` Define connector line pattern. (default: *1*). *( column name modification not allowed )*
     #. ``include`` Define to display only selected cable connectivities.

        * Non blank values will be selected and appeared in output.
        * This will get override by other sheet filters if defined.
        * Use this quick feature, if want to to have just one filter applied on data 
        * A single Page drawing will appear
        * use **filter_on_include_col** input var argument for providing this additional information  


           .. code-block:: python

                 filter_on_include_col=True


     #. There can be **many other filter columns**  with any arbitrary names as per choice.

        * *column name* with each matching *row values* will be considered as a filter, so multiple filters can be defined in a single column. ( see column: *draw_type* in given example data )
        * each filtered data will create its own page in visio drawing.
        * Multipls columns with multiple matching row values can be combined to generate more granular drawings.
        * Output will be multipage output.
        * use **sheet_filters** input var argument in a form of dictionary for providing this additional information  

           .. code-block:: python

                 sheet_filters = {
                   ## key = column header: 
                   ## value(s) = can be either single string or tuple of multiple strings.
                   'draw_type': ('core', 'access',),   
                   # Add more as desired .... 
                 }


-----


* By default, any device with no connectivity on `Cablings` tab, will be excluded.
* Change this behaviour by setting False to input var argument ``filter_on_cable``.

-----



sample excel database 
---------------------------------

:download:`Sample <samples/Excel-pyvig-sample.xlsx>`. Sample Excel file with *Devices* and *Cablings* tabs *prefilled*.

