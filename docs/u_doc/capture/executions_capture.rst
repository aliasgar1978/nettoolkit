NT Capture via JumpSSH - All devices same commands 
=====================================================

This method connects to a jump server first and from there it allows next connection to device to capture the outputs..
Follow below sample steps in order to do the same using Script.

Dynamic custom command addition is not added for this version. it will be added in upcoming version.

* Server login authentication is supported by providing password as well as PSK (Pre-Shared-Keys). 
* Any one input is sufficient.
* PSK will be prefered over provided password if both provided.


You can also refer to a new GUI Tab added under Capture-IT section. 


#. **Execution Steps**

    Step by step boiler plate code. Modify it as per your need.

    .. code-block:: python

        # --------------------------------------------
        # 1. IMPORT NECESSARY FUNCTION
        # --------------------------------------------
        from nettoolkit.capture import capture_by_jump_server_login

        # --------------------------------------------
        # 3. INPUT: Credentials
        # --------------------------------------------
        server_login_username = 'server_login'
        server_login_password = 'server_login_password'
        psk_file = 'public_key_file/shared_with_server/to_use_PSK_method'
        #
        devices_auth = {
            'un':'provide username' , 
            'pw':'provide login password', 
            'en':'provide enable password'  
        }

        # --------------------------------------------
        #  4. INPUT: List of devices & Jump Server
        # --------------------------------------------
        server = '172.20.16.5'
        devices = [
            '192.168.1.1',
            '10.10.10.1',
        ]

        # --------------------------------------------------
        #  5. INPUT: List of COMMANDS (cisco/juniper) each
        #      -- leave it blank for default commands --
        # --------------------------------------------------
        CISCO_IOS_CMDS = [
            'sh run',  
            'sh int status',
            'sh lldp nei', 
        ]
        JUNIPER_JUNOS_CMDS = [
            'show configuration', 
            'show lldp neighbors', 
            'show interfaces descriptions', 
        ]

        # --------------------------------------------------
        #  6. INPUT: Create Dictionary of List of COMMANDS
        # --------------------------------------------------
        cmds_list_dict = {
            'cisco'  : CISCO_IOS_CMDS,      ## Notice: differences in key usage between Capture & Capture-IT modules 
            'juniper': JUNIPER_JUNOS_CMDS, 
        }

        # --------------------------------------------
        #  7. INPUT: Provide Output paths
        # --------------------------------------------
        output_path     = './captures/'


        # ----------------------------------------------
        #  8. INPUT: Optional - Options (modify as need)
        # ----------------------------------------------
        append = True
        missing_only = True
        interactive_cmd_report = False
        cumulative = False
        max_connections = 50
        failed_retry_count = 3
        tablefmt = 'rounded_outline'

        # ------------------------------------------------
        # 8. Call function with all necessary parameters
        # ------------------------------------------------
        capture_by_jump_server_login(
            # // Mandatory: Sever Parameters // #
            server=server, 
            server_login_username=server_login_username, 
            # Either one way of pw
            server_private_key_file = psk_file,       ## Prefered over password
            server_login_password = server_login_password,   

            # // Mandatory: Device Parameters // #
            devices=devices, devices_auth=devices_auth,

            # // Mandatory: Commands dictionary // #
            cmds_list_dict=cmds_list_dict,

            # // Mandatory: Output path // #
            output_path=output_path,

            # // Optional - see below for default values // #
            append = append,
            missing_only = missing_only,
            cumulative = cumulative,
            max_connections = max_connections,
            tablefmt = tablefmt,
            failed_retry_count = failed_retry_count,
            interactive_cmd_report = interactive_cmd_report,
        )

        # -----------------------------------------------------------------------------


-----

.. important::
    
    **Parameters for capture**

    * ``server`` Jump Server IP Address 
    * ``server_login_username`` Jump Server Login User name, 
    * ``server_private_key_file`` Jump Server Login Authentication Method1: (prefered). Provide Preshared key public file.
    * ``server_login_password`` Jump Server Login Authentication Method2: Static password
    * ``devices`` List of devices to be login from Jump Server to capture outputs.
    * ``devices_auth`` Authentication / Credentials for devices (dictionary: format see above example).
    * ``cmds_list_dict`` List of commands for each device types (dictionary: format see above example).
    * ``output_path`` Output path where capture to be stored.
    * ``append`` (optional) (default: False ) appends capture to an existing file if exist if set to True
    * ``missing_only`` (optional) (default: False) captures only command outputs which are missing the existing capture file if set to True
    * ``cumulative`` (optional) (default: True ) create a separate file for each command output if set to False. (++ 'both' option will create both files, clubbed as well as separated.)
    * ``max_connections`` (optional) (default: 100) define Parallel device connections from Jump server (Tip: set 1 for sequencial processing)
    * ``tablefmt`` (optional) (default: *pretty*) summary table format (choose one from various option mentioned below)
    * ``failed_retry_count`` (optional) (default: 2) retry command output capture, if output missed (increase value if bad connections and need more retries)
    * ``interactive_cmd_report`` (optional) (default: False) displays the execution of each commands if set to True

    *   **tablefmt options**:(
        'rounded_outline', 'simple_outline', 'heavy_outline', 'mixed_outline', 'double_outline', 'fancy_outline',
        'presto', 'outline', 'pipe',
        'pretty',  'psql',  
        'orgtbl', 'jira', 'textile', 'html', 'latex' )



.. note::

    * We provide, all commands at a time, for all model devices
    * Script identifies device type ``cisco / juniper`` and push appropriate list of commands to respective device.


-----------------------

Watch out terminal if any errors and see your output in given output path.

