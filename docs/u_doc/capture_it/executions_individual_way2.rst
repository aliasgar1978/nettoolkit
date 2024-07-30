
Nt Capture-it - Individual - option 2
==================================================================

.. note::

    This feature made available from nettoolkit version 1.6.7 onwards.


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.capture_it import capture_by_excel

        # --------------------------------------------
        #    INPUT: Credentials
        # --------------------------------------------
        auth = {
            'un':'provide username' , 
            'pw':'provide login password', 
            'en':'provide enable password'  
        }
        ## Make sure to use static passwords. Refrain using OTP, as ID may get locked due to multiple simultaneous login.

        # --------------------------------------------
        #    INPUT: necessary devices, commands
        # --------------------------------------------
        # Provide the devices and commands details in excel format (sample template excel attached at end of page)
        dev_cmd_xl_file = f'devices_cmds.xlsx'

        # -------------------------------------------------------------------------------------------------------------
        # Custom Project Imports (Optional/Additional), a sample project import mentioned as below. (modify as per own)
        # -------------------------------------------------------------------------------------------------------------
        from custom.custom_captureit.cisco_bgp import BgpAdv   ## Where BgpAdv is a class which has a cmds property to return show commands for specific neighbours advertising route
        from custom.custom_factsgen import CustomDeviceFacts     ## CustomDeviceFacts is a class to modify output database as per custom requirement.
        from custom.custom_factsgen import FOREIGN_KEYS          ## FOREIGN_KEYS, define dictionary with additional custom columns require in output databse {tab_name : [column names]} format.

        # --------------------------------------------
        #    Output: provide output path
        # --------------------------------------------
        capture_path = './captures/'
        exec_log_path = './exec_logs/'
        txt_log_file = "./exec_logs/log_summary.txt" 
        xl_log_file = "./exec_logs/log_summary.xlsx"


        # --------------------------------------------
        #    Define Capture
        # --------------------------------------------
        captures = capture_by_excel(
            auth=auth,                     ## Authentication parameters (dict)
            input_file=dev_cmd_xl_file,    ## input excel file (str)
            capture_path=capture_path,     # output capture path (str)
            exec_log_path=exec_log_path,   # execution logs output path (str)
        )

        # -------------------------------------------------------------------------
        #    Additional [optional] key settings ( Remove if do not want to change )
        # -------------------------------------------------------------------------
        captures.cumulative = 'both'    # default: True ( options: True, False, 'both')
        captures.forced_login = False   # default: True ( options: True, False )
        captures.parsed_output = True   # default: False ( options: True, False )
        captures.max_connections = 1    # default: 100 ( Options: any number input ) ( define max concurrent connections, 1 for sequencial )
        captures.missing_captures_only = True # default: False ( Options: True, False )
        captures.log_type = 'common'    # default: None ( Options: 'common', individual', 'both', None )
        captures.common_log_file = 'common-debug.log' # default: None ( provide filename if log_type is common )

        # -----------------------------------------------------------------------------
        #    Additional [optional] run dynamic custom commands ( Remove if not needed )
        # -----------------------------------------------------------------------------
        captures.dependent_cmds(custom_dynamic_cmd_class=BgpAdv)  # where BgpAdv is custom class imported above

        # -------------------------------------------------------------------------------
        #    Additional [optional] to generate Facts file ( Remove if not needed )
        #    provide CustomDeviceFactsClass, foreign_keys if want to customize Facts file
        # --------------------------------------------------------------------------------
        captures.mandatory_cmds_retries = 2     # default: 0
        captures.generate_facts(
            CustomDeviceFactsClass=CustomDeviceFacts,  # optional (provide if need, custom class imported above )
            foreign_keys=FOREIGN_KEYS,                 # optional (provide if need, custom variable imported above )
        )

        # -----------------------------------------------------------------------------
        #    Start Capture
        # -----------------------------------------------------------------------------
        captures()

        # -----------------------------------------------------------------------------
        #    Log-Summary ( Modify/Enable keys as requires )
        # -----------------------------------------------------------------------------
        captures.log_summary(
            on_screen_display=True,                        ## display on screen. (default: False)
            to_file=txt_log_file,                     # summary to text file
            excel_report_file=xl_log_file,            # summary to excel file
        )

        # -----------------------------------------------------------------------------


----


.. important::
    
    **Parameters for capture_by_excel**

    * ``input_file``  excel file name which contains information on ips and their related commands to capture 
    * ``auth``  authentication Parameters
    * ``capture_path``  output path for commands captures ( use "." for storing in same relative folder )
    * ``exec_log_path`` output path for execution logs ( use "." for storing in smae relative folder )
    * ``cumulative``  (Options: True, False, 'Both', None) defines how to store each command output. True=Save all output in a single file. False=Save all command output in individual file. 'Both'=will generate both kinds of output. None=will not save text log outout to any file, but display it on screen
    * ``forced_login``  (Options: True, False) (Default: False)  Forced login to device even if device ping doesn't succeded.
    * ``parsed_output``  (Options: True, False) (Default: False) Parse the command output and generates device database in excel file.  Each command output try to generate a pased detail tab.
    * ``max_connections``  (numeric) (Default: 100), change the number of simultaneous device connections as per link connection and your pc cpu processng performance.
    * ``mandatory_cmds_retries`` (numeric) (Default: 0), retry count for facts-finder require dcommands change the number to update behaviour
    * ``missing_captures_only``  (Options: True, False) (Default: False)  Instead of capturing all output again, capture only missing outputs from previous capture files.  Useful if there were any missed captures and need to recapture. Kindly Note: Enabling this key will enable **append_capture** as well automatically.
    * ``on_screen_display`` (bool): displays result summary on screen. Defaults to False.
    * ``to_file`` (str): text filename, writes summary result summary to text file. Defaults to None 
    * ``excel_report_file`` (str): excel filename, writes summary result summary to excel file. Default to None 


.. note::
    
    * We provide, all device types commands column wise for all model devices
    * Script identifies device type ``Cisco/Juniper/Arista`` and push appropriate list of commands to respective device.
    * Imp: This methods always implement output captures in append mode. So beware of capture locations if any already contains previous captures.



.. Tip::

    #. Multiple devices can be inserted on a single excel tab.
    #. A device can appear on multiple tabs as well. Respective all tab commands will be captured one by one.
    #. Grouping
        #. Create separate group of commands based on device functionality (as mentioned in sample template attached). 
        #. Add group of devices to each necessary tabs based on device functionality.  



-----------------------

Watch out for the terminal if any errors and see your output in given output path.



