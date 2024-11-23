"""Description: 
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from collections import OrderedDict
from dataclasses import dataclass, field
from nettoolkit.nettoolkit_common import *
from nettoolkit.addressing import *
from nettoolkit.pyNetCrypt import *

from nettoolkit.yaml_facts.common import *

# ==============================================================================================
#  Local Statics
# ==============================================================================================
merge_dict = DIC.merge_dict

CISCO_CMD_NTC_PARSER_FILE_MAP = {
	'show interfaces status':     'cisco_ios_show_interfaces_status.textfsm',
	'show cdp neighbors':         'cisco_ios_show_cdp_neighbors.textfsm',
	'show lldp neighbors':        'cisco_ios_show_lldp_neighbors.textfsm',
	'show mac address-table':     'cisco_ios_show_mac-address-table.textfsm',
	'show ip arp':                'cisco_ios_show_ip_arp.textfsm',
	'show version':               'cisco_ios_show_version.textfsm',
	'show interfaces description':'cisco_ios_show_interfaces_description.textfsm', 
}


# ==============================================================================================
#  Local Functions
# ==============================================================================================

def remove_remarks(command_output):
	return [line for line in command_output if not line.startswith("!")]

def update_port_on_int_type(p):
	if p.lower().startswith("vlan"):           p = int(p[4:])
	elif p.lower().startswith("loopback"):     p = int(p[8:])
	elif p.lower().startswith("port-channel"): p = int(p[12:])
	elif p.lower().startswith("tunnel"):       p = int(p[6:])
	return p

def parse_to_list_using_ntc(cmd, command_output):
	return parse_to_list_cmd(cmd, remove_remarks(command_output), CISCO_CMD_NTC_PARSER_FILE_MAP)

def parse_to_dict_using_ntc(cmd, command_output):
	return parse_to_dict_cmd(cmd, remove_remarks(command_output), CISCO_CMD_NTC_PARSER_FILE_MAP)

def cisco_addressing_on_list(spl, ip_index, mask_index):
	mask = None if "/" in spl[ip_index] else spl[mask_index]
	return addressing(spl[ip_index], mask)



# ==============================================================================================
#  Classes
# ==============================================================================================



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
