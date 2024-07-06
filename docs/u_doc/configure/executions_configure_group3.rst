NT Configure - Group of devices by Excel Files
=================================================

This utility enables user to push the configuration changes to Multiple device. Follow below mentioned steps to understand it.

There are Multiple ways to configure Group of devices. Below described mentioned is one of it.

Additionally this method allows to perform/schedule multiple step changes on same device at different stages during change implementation.

Currently supported platforms are Cisco IOS and Juniper Junos


**Execution Steps**

.. code-block:: python

    # --------------------------------------------
    # IMPORTS
    # --------------------------------------------
    from nettoolkit.configure import ConfigureByExcel

    # -------------------------------------------------------------------------
    #    INPUT: Credentials
    #           Excel containing Device IPs/FQDNs v/s commands list, log folder 
    # -------------------------------------------------------------------------
    ## auth**: Make sure to use static passwords. Refrain using OTP, as ID may get locked due to multiple simultaneous login.
    auth = {
        'un':'provide username' , 
        'pw':'provide login password', 
        'en':'provide enable password'  
    }

    FILES = [                             ## Excel files will be executed in given order
        'c:/users/xxx/desktop/changes/step1.xlsx',
        'c:/users/xxx/desktop/changes/step2.xlsx',
        'c:/users/xxx/desktop/changes/step3.xlsx',
        'c:/users/xxx/desktop/changes/step4.xlsx',
        'c:/users/xxx/desktop/changes/step5.xlsx',
    ]

    ## Provide any one
    TAB_SORTING_ORDER = 'ascending'         ## Each excel tabs will be sorted by name in ascending order for execution (default)
    TAB_SORTING_ORDER = 'reversed'          ## Each excel tabs will be sorted by name in descending order for execution
    TAB_SORTING_ORDER = [                   ## Each excel tabs will be executed in specific given order
        ['Sheet1', 'Sheet2', 'Sheet3'],
        ['Sheet2', 'Sheet1', ],
        ['Sheet1',],
        ['Sheet1', ],
        ['Sheet3', 'Sheet2', 'Sheet1'],
    ]

    DELAY_BETWEEN_TWO_GROUPS = 2            ## wait before starting of next group of devices

    LOG_FOLDER = 'c:/users/xxx/desktop/logs'

    # --------------------------------------------
    #   Define and start Configuration apply
    # --------------------------------------------
    CBE = ConfigureByExcel(
        # Mandatory
        auth=auth,                          # authentication dicationary with 'un', 'pw'. 'en' keys.
        files=FILES,

        # Optional: order list 
        tab_sort_order=TAB_SORTING_ORDER,                   # execute tabs in sequences.
        sleep_time_between_group=DELAY_BETWEEN_TWO_GROUPS,  # delay beetween each next tab/group of devices 
        
        # optional parameters
        log_folder=LOG_FOLDER,           # path where logs to be stored. (Default: None)
        config_log=False,                # enable/disable configuration capture log (Default:True)
        exec_log=False,                  # enable/disable script execution log (Default:True)
        exec_display=True,               # enable/disable script execution on screen display (Default:True)
    )
    CBE()

    # --------------------------------------------


-----

.. important::
    
    **Parameters**

        * ``auth`` (dict): authentication dicationary with 'un', 'pw'. 'en' keys.
        * ``files`` (list, optional): list of excel files, will be executed in provided sequence. Defaults to [].
        * ``tab_sort_order`` (list, optional): Excel tabs execution order. Defaults to []. ( options: privide in list manually, `ascending`, `reversed`)
        * ``sleep_time_between_group`` (int, optional): sleep time between execution of two groups of executions. Defaults to 0.
        * ``log_folder`` (str, optional): folder where logs to be stored. Defaults to None.
        * ``config_log`` (bool, optional): generate configuration log. Defaults to True.
        * ``exec_log`` (bool, optional): generate execution log. Defaults to True.
        * ``exec_display`` (bool, optional): on screen display execution log. Defaults to True.


.. Warning::

    * Script doesn't validate any trueness of configuration. Make sure to provide correct configuration changes


.. admonition:: Excel File Requirements

    * Excel file name and its tabs names can be anything.
    * Sequence will be first based on provided Excel file names.
    * Each Excel can have sub-sequence based on its Tabs. (ascending, reversed, specific provided list)
    * Each column Entry in a single tab will be executed simultaneously. so group the devices by Tabs
    * Each column header (First Row) is to be provided with either device ip or its FQDN.
    * Each column remaining Rows will be considered as configuration change script for that particular device.



:download:`Sample Excel <files/sample_config_changes.xlsx>`. Sample Excel file.

Note here multiple tabs. 
And each tab has its own multiple device entries with its script changes.

Same device can appear at multiple tabs, and stepwise changes can be performed on to it.

-----------------------

Watch out terminal for errors.

Juniper devices requires exact commands without any spelling misses.