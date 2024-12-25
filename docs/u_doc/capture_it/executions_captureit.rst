NT Capture-it - All devices same commands 
=================================================

.. warning::

    since version ***1.7.0*** ``capture-it`` has changed the implementation methods.
    Below explanation depicts latest implementation of capture-it. 
    Kindly refer to following documentation and co-relate changes as per your running version or update your copy with latest.


.. important::

    * Use the below explained method if you have list of devices where, you want to capture the same show commands output from all of devices.
    * Use the next Excel method if you have multiple groups of devices, where you want to run a particuar set of show commands for each groups.


#. **Execution Steps**

    Step by step boiler plate code with explanation. Modify it as per your need.

    .. code-block:: python

        # --------------------------------------------
        # 1. IMPORT NECESSARY PACKAGE/MODULES
        # --------------------------------------------
        from nettoolkit.capture_it import capture
        from nettoolkit import *
        from pathlib import *
        import sys, os
        import pandas as pd
        pd.set_option('mode.chained_assignment', None)          ## disabling pandas warning msgs


        # -------------------------------------------------------------------------------------------------------------
        # 2. Custom Project Imports (Optional/Additional), a sample project import mentioned as below. (modify as per own)
        # -------------------------------------------------------------------------------------------------------------
        from custom.custom_captureit.cisco_bgp import BgpAdv     ## **BgpAdv** class should have a **cmds** property to return custom show commands
        from custom.custom_factsgen import CustomDeviceFacts     ## **CustomDeviceFacts** class is to modify output excel database as per custom requirement.
        from custom.custom_factsgen import FOREIGN_KEYS          ## **FOREIGN_KEYS**, dictionary has custom columns example: {tab_name : [column names]} format.

        # --------------------------------------------
        # 3. INPUT: Credentials
        # --------------------------------------------
        auth = {
            'un':'provide username' , 
            'pw':'provide login password', 
            'en':'provide enable password'  
        }

        # --------------------------------------------
        #  4. INPUT: List of devices
        # --------------------------------------------
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
        cmds = {
            'cisco_ios'  : CISCO_IOS_CMDS,
            'juniper_junos': JUNIPER_JUNOS_CMDS, 
        }
        # Use: ``arista_eos`` for the Arista switch commands list.

        # --------------------------------------------
        #  7. INPUT: Provide Output paths
        # --------------------------------------------
        capture_path     = './captures/'
        exec_log_path    = './logs/'

        # --------------------------------------------
        # 8. Define capture Object as cap
        # --------------------------------------------
        cap = capture(
            ip_list=devices,
            auth=auth,
            cmds=cmds,
            capture_path=capture_path,
            exec_log_path=exec_log_path,
        )

        # -------------------------------------------------------------------------
        # 9. Optional: capture keys modifications
        # -------------------------------------------------------------------------
        cap.cumulative = 'both'    # default: True ( options: True, False, 'both')
        cap.forced_login = False   # default: True ( options: True, False )
        cap.parsed_output = True   # default: False ( options: True, False )
        cap.standard_output = True   # default: False ( options: True, False )
        cap.max_connections = 500    # default: 100 ( Options: number input ) ( Use 1 for sequencial )
        cap.append_capture = True  # default: False ( Options: True, False )
        cap.missing_captures_only = True # default: False ( Options: True, False )
        cap.tablefmt = 'outline' # default: 'pretty' ( Options: see below** )

        # -----------------------------------------------------------------------------
        # 10. Optional dynamic custom commands.
        #     Remove if not importing custom captureit class in step 2
        # -----------------------------------------------------------------------------
        cap.dependent_cmds(custom_dynamic_cmd_class=BgpAdv)  # BgpAdv is custom class

        # -------------------------------------------------------------------------------
        # 11.Optional to generate Facts
        #    Remove arguments in generate_facts if not importing custom class in step 2
        # --------------------------------------------------------------------------------
        cap.generate_facts(
            CustomDeviceFactsClass=CustomDeviceFacts,  ## custom, optional
            foreign_keys=FOREIGN_KEYS,                 ## custom, optional
        )

        # -----------------------------------------------------------------------------
        # 12. Start Capture
        # -----------------------------------------------------------------------------
        cap()

        # -----------------------------------------------------------------------------
        # 13. Log-Summary ( Modify as require )
        # -----------------------------------------------------------------------------
        txt_log_file = exec_log_path + "/" + "summary_log.txt"
        xl_log_file  = exec_log_path + "/" + "summary_log.xlsx"
        cap.log_summary(
            on_screen_display=True,                   # on screen display
            to_file=txt_log_file,                     # to text file
            excel_report_file=xl_log_file,            # to excel file
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
    * ``standard_output``  (Options: True, False) (Default: False) capture to be done in capture it format or normal standard capture format.
    * ``max_connections``  (numeric) (Default: 100), change the number of simultaneous device connections as per link connection and your pc cpu processng performance.
    * ``mandatory_cmds_retries`` (numeric) (Default: 0), retry count for facts-finder require dcommands change the number to update behaviour
    * ``append_capture``  (Options: True, False) (Default: False)  
    * ``missing_captures_only``  (Options: True, False) (Default: False)  Instead of capturing all output again, capture only missing outputs from previous capture files.  Useful if there were any missed captures and need to recapture. Kindly Note: Enabling this key will enable **append_capture** as well automatically.
    * ``on_screen_display`` (bool): displays result summary on screen. Defaults to False.
    * ``to_file`` (str): text filename, writes summary result summary to text file. Defaults to None 
    * ``excel_report_file`` (str): excel filename, writes summary result summary to excel file. Default to None 
    * ``tablefmt`` ( Options:
        'rounded_outline', 'simple_outline', 'heavy_outline', 'mixed_outline', 'double_outline', 'fancy_outline',
        'presto', 'outline', 'pipe',
        'pretty',  'psql',  
        'orgtbl', 'jira', 'textile', 'html', 'latex' )



.. note::

    * We provide, all commands at a time, for all model devices
    * Script identifies device type ``Cisco/Juniper/Arista`` and push appropriate list of commands to respective device.


-----------------------

Watch out terminal if any errors and see your output in given output path.

