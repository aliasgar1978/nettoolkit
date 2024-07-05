
Excel database Preparation - Manual
=====================================


* Requirement is to have an Excel database in appropriate format.
* Two tabs as per given below names are mandatory.

  #. ``Devices`` tab defines all images/icons, its position indexes, and icon informations; which are to be placed on the visio page(s).
  #. ``Cablings`` tab defines all cabling/connectivity related informations for above devices.


There is a simple sample Excel given at end of this page. Download and modify it as your requirement.

Read Below to understand it.

-----

**Devices Tab - Mandatory Columns**
-----------------------------------


     #. ``hostname`` hostname or identity of device. *( No Exception and column name modification not allowed )*
     #. ``x-axis`` horizontal position of device. *( column name can be changed by defining var argument `x` in input)*
     #. ``y-axis`` vertical position of device. *( column name can be changed by defining var argument `y` in input)*

**Cablings Tab - Mandatory Columns**
-------------------------------------

     #. ``a_device`` a-end device hostname for connectivity. *(column name can be changed by defining var argument `dev_a` in input)*
     #. ``b_device`` b-end device hostname for connectivity. *(column name can be changed by defining var argument `dev_b` in input)*

-----



**Devices Tab - Optional Columns**
-----------------------------------

     #. ``stencil`` stencil file for individual device icon *( column name modification not allowed )*
     #. ``item`` stencil name or number id from stencil *( column name modification not allowed )*
     #. ``iconHeight`` resizing of icon vertically *( column name modification not allowed )*
     #. ``iconWidth`` resizing of icon horizontaly *( column name modification not allowed )*
     #. There can be **N number of columns** for additional device information ( column-names choose as per your desire )

        * **Example**: *(device_model, serial_number, ip_address, rack_details, . . . and many more ).*
        * Add those into device information using ``cols_to_merge`` argument list.
        * Re-arrange those in list as desired in output.


**Cablings Tab - Optional Columns**
-------------------------------------

     #. ``aport`` port number for a-end device. It will appear at middle. *( column name modification not allowed )*
     #. ``connector_type`` line connector type. (default: *straight*, other options: *angled, curved*). *( column name modification not allowed )*
     #. ``color`` line connector color. (default: *blue*). *( column name modification not allowed )*
     #. ``weight`` line connector weigth/thickness. (default: *3*). *( column name modification not allowed )*
     #. ``pattern`` line connector pattern. (default: *1*). *( column name modification not allowed )*
     #. ``include`` displays only selected.

        * Non blank values will be selected and appeared in output.
        * It will get override by other sheet filters if defined.
        * Use this quick feature, if want to to have just one filter applied on data 
        * A single Page drawing will appear
        * It uses **filter_on_include_col** argument to enable. 


           .. code-block:: python

                 filter_on_include_col=True


     #. There can be many other filter columns  with any arbitrary names as per choice.

        * *Column name* with each matching *row values* will be considered as a filter, so multiple filters can be defined in a single column. ( see column: *draw_type* in given example data )
        * Each filtered data will create its own page in visio drawing.
        * Multiple columns with multiple matching row values can be combined together to generate more granular drawings.
        * Output will be multipage output.
        * It Uses **sheet_filters** argument in a form of dictionary for providing information  

           .. code-block:: python

                 sheet_filters = {
                   ## key = column header: 
                   ## value(s) = can be either single string or tuple of multiple strings.
                   'draw_type': ('core', 'access',),   
                   # Add more as desired .... 
                 }


-----


* Default, any device with no connectivity on `Cablings` tab, will be excluded.
* Change this behaviour by setting False to input var argument ``filter_on_cable``.

-----



sample excel database 
---------------------------------

:download:`Sample <samples/Excel-pyvig-sample.xlsx>`. Sample Excel file with *Devices* and *Cablings* tabs *prefilled*.

