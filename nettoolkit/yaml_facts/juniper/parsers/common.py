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
	'show arp'              : 'juniper_junos_show_arp.textfsm',

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
	return get_numbered_port_dict(int_filter_dict, port)

def get_numbered_port_dict(op_dict, port):
	if port.startswith("irb."): 
		port=int(port[4:])
	elif port.startswith("ae") or port.startswith("lo"): 
		port=port[2:]
	return add_blankdict_key(op_dict, port)

def parse_to_list_using_ntc(cmd, command_output):
	return parse_to_list_cmd(cmd, remove_remarks(command_output), JUNIPER_CMD_NTC_PARSER_FILE_MAP)

def parse_to_dict_using_ntc(cmd, command_output):
	return parse_to_dict_cmd(cmd, remove_remarks(command_output), JUNIPER_CMD_NTC_PARSER_FILE_MAP)


# ==============================================================================================

def get_pw(spl, key):
	pw = spl[spl.index(key)+1]
	if pw[0] == '"': pw = pw[1:]
	if pw[-1] == '"': pw = pw[:-1]
	return juniper_decrypt( pw )

def get_instance_parameter_for_items(dic, line, spl, items, unique=False):
	for item in items:
		_get_instance_parameter(dic, line, spl, item, unique)

def _get_instance_parameter(dic, line, spl, item, unique=False):
	if item not in spl: return
	append_attribute(dic, attribute=item, value=spl[spl.index(item)+1], remove_duplicate=unique)

def update_true_instance_items(dic, line, spl, items):
	for item in items:
		_update_true_instance(dic, line, spl, item)

def _update_true_instance(dic, line, spl, item):
	if item not in spl: return
	dic[item]=True

def get_nest_attributes(input_dict, line, spl, nest_attrs, next_attr=True, unique=False):
	if isinstance(nest_attrs, dict):
		for k, v in nest_attrs.items():
			if not v: continue
			if k not in spl: continue
			dic = add_blankdict_key(input_dict, k)
			get_nest_attributes(dic, line, spl, v, next_attr, unique)

	elif isinstance(nest_attrs, (list, tuple, set)):
		if next_attr:
			get_instance_parameter_for_items(input_dict, line, spl, nest_attrs, unique)
		else:
			update_true_instance_items(input_dict, line, spl, nest_attrs)

	else:
		print(f"Unidentified attribute type: {type(nest_attrs)}, {nest_attrs}")



# ==============================================================================================
#  Classes
# ==============================================================================================



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
