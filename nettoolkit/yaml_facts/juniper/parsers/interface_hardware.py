"""juniper show chassis hardware command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_chassis_hardware(cmd_op):
	op_dict = {}
	parsed_data_dict_list = parse_to_dict_using_ntc('show chassis hardware', cmd_op)
	parsed_data = parse_to_list_using_ntc('show chassis hardware', cmd_op)
	#
	for dic in parsed_data_dict_list:
		first_item_part_no = dic['PART']
		break
	#
	for spl in parsed_data:
		part_idx = spl.index(first_item_part_no)
		break
	#
	for spl in parsed_data:
		port = "/".join(LST.remove_empty_members(spl[:part_idx]))
		sfp_part_id = spl[part_idx]
		sfp_serial = spl[part_idx+1]
		sfp = spl[part_idx+2]
		if not op_dict.get(port):
			op_dict[port] = {}
		op_dict[port]['media_type'] = sfp 
		op_dict[port]['serial'] = sfp_serial
		op_dict[port]['part_id'] = sfp_part_id 

	return {'interfaces': {'physical_media': op_dict}}
# ------------------------------------------------------------------------------
