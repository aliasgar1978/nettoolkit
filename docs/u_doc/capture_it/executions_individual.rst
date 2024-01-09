
Nt Capture-it - Individual
==================================================================

.. note::

    * for networking version >= 0.1.0, integrated.
    * for nettoolkig version < 0.1.0, install capture-it as separate project


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
        op_path = './captures/'

        # --------------------------------------------
        #    Define Capture
        # --------------------------------------------
        c = capture_individual(
            auth=auth,             ## Authentication parameters (dict)
            dev_cmd_dict=devices,  ## Dictionary of devices of list of commands ( see above sample )
            path=op_path,          ## output path - to store the outputs. (optional, default =".")
        )

        # -------------------------------------------------------------------------
        #    Additional [optional] key settings ( Remove if do not want to change )
        # -------------------------------------------------------------------------
        c.cumulative = 'both'    # default: True ( options: True, False, 'both')
        c.forced_login = False   # default: True ( options: True, False )
        c.parsed_output = True   # default: False ( options: True, False )
        c.visual_progress = 9    # default: 3 ( Option range: 0 - 10 ) 
        c.max_connections = 1    # default: 100 ( Options: any number input ) ( define max concurrent connections, 1 for sequencial )
        c.log_type = 'common'    # default: None ( Options: 'common', individual', 'both', None )
        c.common_log_file = 'common-debug.log' # default: None ( provide filename if log_type is common )
        c.retry_mandatory_cmds_retries = 1     # default: 3

        # -----------------------------------------------------------------------------
        #    Additional [optional] run dynamic custom commands ( Remove if not needed )
        # -----------------------------------------------------------------------------
        c.dependent_cmds(custom_dynamic_cmd_class=BgpAdv)  # where BgpAdv is custom class imported above

        # -------------------------------------------------------------------------------
        #    Additional [optional] to generate Facts file ( Remove if not needed )
        #    provide CustomDeviceFactsClass, foreign_keys if want to customize Facts file
        # --------------------------------------------------------------------------------
        c.generate_facts(
            CustomDeviceFactsClass=CustomDeviceFacts,  # optional (provide if need, custom class imported above )
            foreign_keys=FOREIGN_KEYS,                 # optional (provide if need, custom variable imported above )
        )

        # -----------------------------------------------------------------------------
        #    Start Capture
        # -----------------------------------------------------------------------------
        c()


        # -----------------------------------------------------------------------------
        #    Log-Summary ( Modify/Enable keys as requires )
        # -----------------------------------------------------------------------------
        LogSummary(c, 
            print=True,                        ## display on screen. (default: False)
            # write_to='cmds_log_summary.log', ## create a fresh log summary file (default: None)
            # append_to='cmds_log_summary.log',## append to log summary file (default: None) 
        )

        # -----------------------------------------------------------------------------



.. important::
    
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



