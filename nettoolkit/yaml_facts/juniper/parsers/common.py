"""Description: 
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from dataclasses import dataclass, field
from collections import OrderedDict
from nettoolkit.nettoolkit_common import *
from nettoolkit.nettoolkit_common.gpl import *
from nettoolkit.addressing import to_dec_mask, invmask_to_mask, addressing, shrink
from nettoolkit.pyNetCrypt import juniper_decrypt
from nettoolkit.pyJuniper import JSet

from nettoolkit.facts_finder.generators.commons import *
from nettoolkit.facts_finder.generators.juniper.common import *

from nettoolkit.yaml_facts.common import *

# ==============================================================================================
#  Local Statics
# ==============================================================================================
merge_dict = DIC.merge_dict

JUNIPER_CMD_NTC_PARSER_FILE_MAP = {
	'show chassis hardware' : 'juniper_junos_show_chassis_hardware.textfsm',
	'show lldp neighbors'   : 'juniper_junos_show_lldp_neighbors.textfsm'  ,
	# 'show version'          : 'juniper_junos_show_version.textfsm',        # NIU, chassis info wrong
}


# ==============================================================================================
#  Local Functions
# ==============================================================================================

def remove_remarks(command_output):
	return [line for line in command_output if not line.startswith("#")]

def get_int_port_dict(op_dict, port):
	int_filter = get_juniper_int_type(port).lower()
	if not op_dict.get(int_filter):
		op_dict[int_filter] = {}
	int_filter_dict = op_dict[int_filter]
	#
	if port.startswith("irb."): 
		port=int(port[4:])
	elif port.startswith("ae") or port.startswith("lo"): 
		port=port[2:]
	#
	if not int_filter_dict.get(port): 
		int_filter_dict[port] = {}
	return int_filter_dict[port]

def parse_to_list_using_ntc(cmd, command_output):
	return parse_to_list_cmd(cmd, remove_remarks(command_output), JUNIPER_CMD_NTC_PARSER_FILE_MAP)

def parse_to_dict_using_ntc(cmd, command_output):
	return parse_to_dict_cmd(cmd, remove_remarks(command_output), JUNIPER_CMD_NTC_PARSER_FILE_MAP)


# ==============================================================================================
#  Classes
# ==============================================================================================



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
