NT Capture-it - Normal
=================================================

.. warning::

    * for latest networkit version, i.e. >= 0.1.0, its integrated.
    * for older nettoolkt versions, i.e. < 0.1.0, install capture-it as separate project, and refer older documentation.


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.capture_it import capture, LogSummary
        from nettoolkit import *
        from pathlib import *
        import sys, os
        import pandas as pd
        pd.set_option('mode.chained_assignment', None)          ## disable pandas warning msgs


        # -------------------------------------------------------------------------------------------------------------
        # Custom Project Imports (Optional/Additional), a sample project import mentioned as below. (modify as per own)
        # -------------------------------------------------------------------------------------------------------------
        from custom.custom_captureit.cisco_bgp import BgpAdv   ## Where BgpAdv is a class which has a cmds property to return show commands for specific neighbours advertising route
        from custom.custom_factsgen import CustomDeviceFacts     ## CustomDeviceFacts is a class to modify output database as per custom requirement.
        from custom.custom_factsgen import FOREIGN_KEYS          ## FOREIGN_KEYS, define dictionary with additional custom columns require in output databse {tab_name : [column names]} format.

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
        devices = [
            '192.168.1.1',
            '10.10.10.1',
            #  list down all ip addresses for which output to be captured  
        ]
        CISCO_IOS_CMDS = ['sh run',  'sh int status','sh lldp nei', ]
        JUNIPER_JUNOS_CMDS = ['show configuration', 'show lldp neighbors', 'show interfaces descriptions', ]
        cmds = {
            'cisco_ios'  : CISCO_IOS_CMDS,
            'juniper_junos': JUNIPER_JUNOS_CMDS, 
        }
        # Note: ``arista_eos`` for the Arista switch commands list.

        # --------------------------------------------
        #    Output: provide output path
        # --------------------------------------------
        capture_path = './captures/'
        exec_log_path = './exec_logs/'

        # --------------------------------------------
        #    Define Capture
        # --------------------------------------------
        captures = capture(
            ip_list=devices,  # mandatory - list of devices
            auth=auth,        # mandatory - authentication parameters dictionary
            cmds=cmds,        # mandatory - dictionary of list of commands
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





#. **custom_dynamic_cmd_class**

    It Is possible to fork in **additional dynamic commands** which requires output *based* on some *previous show output capture*.   

      * Scenario: **show bgp summary** lists bgp neighbors. If we want to see advertised routes of selected neighbor of those.  Here *neighbor* is variable based on previous output. 
      * In above case, We can define a custom class which . 

        * First evaluates previous_output, based on device type
        * Get list of neighbors. 
        * Filter neighbors as needed. 
        * Creates a list of additinal show commands.
        * which can be called/returned  with `cmds` property of custom class.


#. **Sample of custom_dynamic_cmd_class**

    .. code-block:: python

        # some supportive functions

        def get_adv_route_string_cisco(nbr):
            return f'show ip bgp all nei {nbr} adv'

        def get_adv_route_string_juniper(nbr):
            return f'show route advertising-protocol bgp {nbr}'

        def get_bgp_peers_cisco(show_output):
            peers = []
            ## Do it Your Self to derive peer ip addresses from cisco show output
            return peers

        def get_bgp_peers_juniper(show_output):
            peers = []
            ## Do it Your Self to derive peer ip addresses from juniper show output
            return peers

        # Custom dynamic command class to get additional bgp advertising routes.

        class BgpAdv():

            def __init__(self, output_of_prev_show_cmd, dtype):
                self.peers = set()
                self.show_peer_adv_route_cmds = set()
                func_maps = {
                    'cisco_ios':{
                        'get_bgp_peers': get_bgp_peers_cisco,               # function to derive bgp peers from show output (cisco)
                        'get_adv_route_string': get_adv_route_string_cisco, # function to get string (cisco)
                    } ,
                    'juniper_junos':{
                        'get_bgp_peers': get_bgp_peers_juniper,               # function to derive bgp peers from show output (juniper)
                        'get_adv_route_string': get_adv_route_string_juniper, # function to get string (juniper)
                    } ,
                }
                #
                self.peers = func_maps[dtype]['get_bgp_peers'](output_of_prev_show_cmd)
                for peer in self.peers:
                    adv_routes = func_maps[dtype]['get_adv_route_string'](peer)
                    self.show_peer_adv_route_cmds.add(adv_routes)

            @property
            def cmds(self):
                return sorted(self.show_peer_adv_route_cmds)


-----

.. important::
    
    **Parameters for capture**

    * ``devices``  list of ip addresses
    * ``auth``  authentication Parameters
    * ``cmds``  dictionary of list of commands to be captred (cisco, juniper, arista).
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

    * We provide, all commands at a time, for all model devices
    * Script identifies device type ``Cisco/Juniper/Arista`` and push appropriate list of commands to respective device.


-----------------------

Watch out terminal if any errors and see your output in given output path.
