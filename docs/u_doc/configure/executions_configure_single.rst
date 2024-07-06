NT Configure - Single device
=================================================

This utility enables user to push the configuration changes to a sinlge device. Follow below mentioned steps to understand it.

Currently supported platforms are Cisco IOS and Juniper Junos


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.configure import Configure

        # --------------------------------------------
        #    INPUT: Credentials
        #           Device IP/FQDN, commands, log folder 
        # --------------------------------------------
        ## auth**: Make sure to use static passwords. Refrain using OTP, as ID may get locked due to multiple simultaneous login.
        auth = {
            'un':'provide username' , 
            'pw':'provide login password', 
            'en':'provide enable password'  
        }
        DEVICE = '192.168.1.1'
        ## configuration changes (either one)
        CONFIG_CHANGE_LIST = [
            'interface Gig0/1',  
            ' description ** Available **',  
            ' shutdown',  
            '!',  
        ]
        CONFIG_CHANGE_FILE = 'c:/users/xxx/desktop/delta_config_changes.txt'
        LOG_FOLDER = 'c:/users/xxx/desktop/logs'

        # --------------------------------------------
        #   Define and start Configuration apply
        # --------------------------------------------
        CFG = Configure(
            # Mandatory input
            ip=DEVICE,                          # Device IP or FQDN
            auth=auth,                          # authentication dicationary with 'un', 'pw'. 'en' keys.
            
            # Mandatory: Provide Either input
            conf_list=CONFIG_CHANGE_LIST,        ## refers to changes list.
            conf_file=CONFIG_CHANGE_FILE,        ## refers to changes file. -- flie will override list. 
            
            # optional parameters
            log_folder=LOG_FOLDER,           # path where logs to be stored. (Default: None)
            config_log=False,                # enable/disable configuration capture log (Default:True)
            exec_log=False,                  # enable/disable script execution log (Default:True)
            exec_display=True,               # enable/disable script execution on screen display (Default:True)
        )
        CFG.apply()

        # --------------------------------------------


-----

.. important::
    
    **Parameters**

        * ``ip`` (str): device ip address or FQDN
        * ``auth`` (dict): authentication dicationary with 'un', 'pw'. 'en' keys.
        * ``conf_list`` (list, optional): configuration change list. Defaults to None. 
        * ``conf_file`` (str, optional): configuration change file. Defaults to None. conf_file will override conf_list if both are provided.
        * ``log_folder`` (str, optional): folder where logs to be stored. Defaults to None.
        * ``config_log`` (bool, optional): generate configuration log. Defaults to True.
        * ``exec_log`` (bool, optional): generate execution log. Defaults to True.
        * ``exec_display`` (bool, optional): on screen display execution log. Defaults to True.

        Providing dual config change input will require user interactive input to accept **conf_file** as configuration changes.



.. Warning::

    * Script doesn't validate any trueness of configuration. Make sure to provide correct configuration changes


-----------------------

Watch out terminal for errors.

Juniper devices requires exact commands without any spelling misses