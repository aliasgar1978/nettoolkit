"""cisco show interface description command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_interface_description(command_output):
	int_desc_dict = {}
	start = False
	for l in command_output:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		if l.startswith("Interface"): 
			desc_begin_at = l.find("Description")
			status_begin_at = l.find("Status")
			protocol_begin_at = l.find("Protocol")
			continue
		spl = l.strip().split()
		p = STR.if_standardize(spl[0])
		#
		int_filter = get_cisco_int_type(p)
		if not int_desc_dict.get(int_filter):
			int_desc_dict[int_filter] = {}
		int_filter_dict = int_desc_dict[int_filter]
		if not int_filter_dict.get(p): 
			int_filter_dict[p] = {}
		port = int_filter_dict[p]
		#
		port['description'] = get_string_trailing(l, desc_begin_at)
		#
		admin_status = l[status_begin_at:protocol_begin_at].strip()
		int_status = l[protocol_begin_at:desc_begin_at].strip()
		state = 'up'
		if admin_status in ('admin down', 'administratively down'):
			state = 'administratively down'
		elif int_status in ('down'):
			state = 'down'
		port['link_status'] = state
		#
		# if not (int_desc_dict.get('filter') and int_desc_dict['filter']):
		# 	port['filter'] = get_cisco_int_type(p)

	return {'interfaces': int_desc_dict }
# ------------------------------------------------------------------------------
