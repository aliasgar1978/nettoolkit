
Nt Capture-it - Individual
==================================================================

.. warning::

    * for latest networkit version, i.e. >= 0.1.0, its integrated.
    * for older nettoolkt versions, i.e. < 0.1.0, install capture-it as separate project, and refer older documentation.


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.capture_it import capture_individual, LogSummary

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
        # Provide the dictionary of devices v/s commands as sample given below.
        devices = {
            '10.10.10.1': [show_cmd_1, show_cmd_2, ..],
            '10.10.10.2': [show_cmd_3, show_cmd_4, ..], 
            ('10.10.10.3', '10.10.10.4', '10.10.10.1'): [show_cmd_5, show_cmd_6, ..],
        }

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


        # --------------------------------------------
        #    Define Capture
        # --------------------------------------------
        captures = capture_individual(
            auth=auth,             ## Authentication parameters (dict)
            dev_cmd_dict=devices,  ## Dictionary of devices of list of commands ( see above sample )
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
        captures.append_capture = True  # default: False ( Options: True, False )
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
        #    Display failures
        # -----------------------------------------------------------------------------
        captures.show_failures

        # -----------------------------------------------------------------------------
        #    Log-Summary ( Modify/Enable keys as requires )
        # -----------------------------------------------------------------------------
        LogSummary(captures, 
            on_screen_display=True,                        ## display on screen. (default: False)
            write_to=f'{exec_log_folder}/cmds_log_summary.log', 
            # append_to=f'{exec_log_folder}/cmds_log_summary.log', 
        )

        # -----------------------------------------------------------------------------


----


.. important::
    
    **Parameters for capture**

    * ``dev_cmd_dict``  dictionary of devices of list of commands
    * ``auth``  authentication Parameters
    * ``capture_path``  output path for commands captures ( use "." for storing in same relative folder )
    * ``exec_log_path`` output path for execution logs ( use "." for storing in smae relative folder )
    * ``cumulative``  (Options: True, False, 'Both', None) defines how to store each command output. True=Save all output in a single file. False=Save all command output in individual file. 'Both'=will generate both kinds of output. None=will not save text log outout to any file, but display it on screen
    * ``forced_login``  (Options: True, False) (Default: False)  Forced login to device even if device ping doesn't succeded.
    * ``parsed_output``  (Options: True, False) (Default: False) Parse the command output and generates device database in excel file.  Each command output try to generate a pased detail tab.
    * ``max_connections``  (numeric) (Default: 100), change the number of simultaneous device connections as per link connection and your pc cpu processng performance.
    * ``mandatory_cmds_retries`` (numeric) (Default: 0), retry count for facts-finder require dcommands change the number to update behaviour
    * ``append_capture``  (Options: True, False) (Default: False)  
    * ``missing_captures_only``  (Options: True, False) (Default: False)  Instead of capturing all output again, capture only missing outputs from previous capture files.  Useful if there were any missed captures and need to recapture. Kindly Note: Enabling this key will enable **append_capture** as well automatically.

    **Parameters for LogSummary**

    * ``c`` (capture_individual): capture_individual object instance
    * ``on_screen_display`` (bool): displays result summary on screen. Defaults to False.
    * ``write_to`` (str): filename, writes result summary to file. Defaults to None (i.e. no file write out).
    * ``append_to`` (str): filename, appends result summary to file. Default to None (i.e. no file to append).


.. note::
    
    Since we are providing individual commands for each device, pay attention on device type  ``Cisco/Juniper/Arista`` and apply respective commands to the system appropriatly.


.. Tip::

    #. Multiple devices can be inserted as a tuple for dictionary keys.
    #. One device can appear on multiple keys ( as stated in above example: 10.10.10.1).  List of commands from both  entries will be clubbed together to form a single list.
    #. Grouping
        #. Create a separate group of commands based on device functionality (example: separate set of commands for each - access layers, core layers ). 
        #. Create group of devices as a tuple based on device functionality.  
        #. Using these above two - create a simple readable dictionary. 



-----------------------

Watch out for the terminal if any errors and see your output in given output path.



