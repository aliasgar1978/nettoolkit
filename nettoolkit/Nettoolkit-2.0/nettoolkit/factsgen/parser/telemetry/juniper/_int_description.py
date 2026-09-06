"""juniper interface description command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line, get_string_trailing, get_juniper_int_type
# ------------------------------------------------------------------------------


def get_int_description(cmd_op, *args):
	"""parser - show interfaces description command output

	Parsed Fields:
		* port/interface 
		* description

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""
	op_dict = {}

	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("#"): continue
		if l.startswith("Interface"): 
			desc_begin_at = l.find("Description")
			link_desc_begin_at = l.find("Admin")
			continue
		spl = l.strip().split()
		p = spl[0]
		int_type = get_juniper_int_type(p)
		if not op_dict.get(int_type):
			op_dict[int_type] = {}
		int_type_dict = op_dict[int_type]
		if not int_type_dict.get(p): int_type_dict[p] = {}
		port = int_type_dict[p]
		if not (port.get('description') and port['description']):
			port['description'] = get_string_trailing(l, desc_begin_at)
		port['link_status'] = l[link_desc_begin_at:link_desc_begin_at+5].strip()

	return {'op_dict': op_dict}
# ------------------------------------------------------------------------------
