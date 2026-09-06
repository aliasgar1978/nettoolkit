"""cisco show interface description command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line, if_standardize, get_string_trailing, get_cisco_int_type

# ------------------------------------------------------------------------------

def get_interface_description(cmd_op, *args):
	"""parser - show int descript command output

	Parsed Fields:
		* port/interface
		* description

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""
	
	int_desc_dict = {}
	start = False
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		if l.startswith("Interface"): 
			desc_begin_at = l.find("Description")
			status_begin_at = l.find("Status")
			protocol_begin_at = l.find("Protocol")
			continue
		spl = l.strip().split()
		p = if_standardize(spl[0])
		filter = get_cisco_int_type(p)
		if not int_desc_dict.get(filter):
			int_desc_dict[filter] = {}
		int_type_dict = int_desc_dict[filter]
		if not int_type_dict.get(p): 
			int_type_dict[p] = {}
		port = int_type_dict[p]
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

	return {'op_dict': int_desc_dict }
# ------------------------------------------------------------------------------
