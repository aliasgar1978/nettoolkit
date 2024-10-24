"""Description: Cisco Parser
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from dataclasses import dataclass, field
from collections import OrderedDict
from nettoolkit.yaml_facts.common import CommonParser
from nettoolkit.yaml_facts.juniper.parsers import *

# ==============================================================================================
#  Local Statics
# ==============================================================================================
JUNIPER_CMD_PARSER_MAP = OrderedDict([
	('show interfaces descriptions', (get_interface_description, )),
	('show lldp neighbors', (get_lldp_neighbour,)),
	('show configuration', (
			get_interfaces_running, 
			get_system_running, 
			get_bgp_running,    
			get_system_running_routes, 
			get_system_running_prefix_lists
	# 	)
	)),
	('show version', (get_version, )),
	('show chassis hardware', (
		get_chassis_hardware, 
		get_chassis_serial,
	)),
	('show arp', (get_arp_table,)),
	# 'show interfaces terse', (),
	# 'show bgp summary', (),

])


# ==============================================================================================
#  Local Functions
# ==============================================================================================



# ==============================================================================================
#  Classes
# ==============================================================================================
@dataclass
class JuniperParser(CommonParser):
	captures: any
	output_folder: str=''

	cmd_fn_parser_map = JUNIPER_CMD_PARSER_MAP

# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
