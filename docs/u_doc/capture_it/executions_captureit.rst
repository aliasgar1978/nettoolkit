NT Capture-it - Normal
=================================================

.. note::

    * for networking version >= 0.1.0, integrated.
    * for nettoolkig version < 0.1.0, install capture-it as separate project


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.capture_it import capture, quick_display, LogSummary
        from nettoolkit.nettoolkit import *
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
        op_path = './captures/'


        # --------------------------------------------
        #    Define Capture
        # --------------------------------------------
        c = capture(
            ip_list=devices,  # mandatory - list of devices
            auth=auth,        # mandatory - authentication parameters dictionary
            cmds=cmds,        # mandatory - dictionary of list of commands
            path=op_path,     # mandatory - output capture path (str)
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


.. note::

    * We provide, all commands at a time, for all model devices
    * Script identifies device type ``Cisco/Juniper/Arista`` and push appropriate list of commands to respective device.


-----------------------

Watch out terminal if any errors and see your output in given output path.
