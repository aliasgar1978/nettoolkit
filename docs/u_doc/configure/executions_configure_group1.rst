NT Configure - Group of devices by cmds_list
=================================================

This utility enables user to push the configuration changes to Multiple device. Follow below mentioned steps to understand it.

There are Multiple ways to configure Group of devices. Below described mentioned is one of it.

Currently supported platforms are Cisco IOS and Juniper Junos


**Execution Steps**

.. code-block:: python

    # --------------------------------------------
    # IMPORTS
    # --------------------------------------------
    from nettoolkit.configure import GroupsConfigure

    # --------------------------------------------------------------
    #    INPUT: Credentials
    #           Device IPs/FQDNs v/s commands list, log folder 
    # --------------------------------------------------------------
    ## auth**: Make sure to use static passwords. Refrain using OTP, as ID may get locked due to multiple simultaneous login.
    auth = {
        'un':'provide username' , 
        'pw':'provide login password', 
        'en':'provide enable password'  
    }
    DEVICES_CMDS_DICTIONARY = {
        '192.168.100.1': { 
            'cmds_list':[
                'interface Gig0/1',  
                ' description ** Available **',  
                ' shutdown',  
                '!', 
            ],
        },
        #
        '192.168.100.2': { 
            'cmds_list':[
                'interface Gig0/2',  
                ' description ** Not Available **',  
                ' shutdown',  
                '!', 
            ],
        },
        #
        '192.168.100.3': { 
            'cmds_list':[
                'interface Gig0/3',  
                ' description ** Faulty **',  
                ' shutdown',  
                '!', 
            ],
        },
        #
    }
    EXECUTION_ORDER_LIST = [ 
        ['192.168.100.1', '192.168.100.2'],       ## these two devices will be grouped and applied config simultaneously
        '192.168.100.3',                          ## this one device will be applied config after above two completed.     
    ]
    LOG_FOLDER = 'c:/users/xxx/desktop/logs'

    # --------------------------------------------
    #   Define and start Configuration apply
    # --------------------------------------------
    GC = GroupsConfigure(
        # Mandatory
        auth=auth,                          # authentication dicationary with 'un', 'pw'. 'en' keys.
        devices_config_dict=DEVICES_CMDS_DICTIONARY,

        # Optional: order list 
        config_by_order=True,               # execute devices in provided order or auto order.
        order_list=EXECUTION_ORDER_LIST,    # order list in which execution is to be done
        
        # optional parameters
        log_folder=LOG_FOLDER,           # path where logs to be stored. (Default: None)
        config_log=False,                # enable/disable configuration capture log (Default:True)
        exec_log=False,                  # enable/disable script execution log (Default:True)
        exec_display=True,               # enable/disable script execution on screen display (Default:True)
    )
    GC()

    # --------------------------------------------


-----

.. important::
    
    **Parameters**

        * ``auth`` (dict): authentication dicationary with 'un', 'pw'. 'en' keys.
        * ``devices_config_dict`` (dict, optional): {device:[list of config], } . Defaults to {}.
        * ``config_by_order`` (bool, optional): if True follows execution in provided order_list entries. Defaults to True.
        * ``order_list`` (list, optional): order list in which execution to be done. Defaults to [].
        * ``log_folder`` (str, optional): folder where logs to be stored. Defaults to None.
        * ``config_log`` (bool, optional): generate configuration log. Defaults to True.
        * ``exec_log`` (bool, optional): generate execution log. Defaults to True.
        * ``exec_display`` (bool, optional): on screen display execution log. Defaults to True.


.. Warning::

    * Script doesn't validate any trueness of configuration. Make sure to provide correct configuration changes

.. Note::

    Note here, in this case a device can appear only once in a ``devices_config_dict``. which is a limitation of using this method.
    
    In case if you want to schedule multiple stepwise changes on a single device at different stages, than use the upcoming method ``ConfigureByExcel``,
    where multiple changes can be performed on same device(s) at different stages.


-----------------------

Watch out terminal for errors.

Juniper devices requires exact commands without any spelling misses