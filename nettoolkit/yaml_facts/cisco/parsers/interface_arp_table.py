"""cisco show arp table command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_arp_table(command_output):
	op_dict = {}
	start = False
	for l in command_output:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		if l.startswith("Protocol"): continue
		if l.find("Incomplete")>0: continue
		if l.strip().startswith("%") and l.endswith("does not exist."): continue
		spl = l.strip().split()
		try:
			p = STR.if_standardize(spl[-1])
			_mac = standardize_mac(spl[3])
			ip = spl[1]
		except:
			pass
		#
		int_filter = get_cisco_int_type(p)
		if not op_dict.get(int_filter):
			op_dict[int_filter] = {}
		int_filter_dict = op_dict[int_filter]
		if not int_filter_dict.get(p): 
			int_filter_dict[p] = {}
		port = int_filter_dict[p]
		#
		if not port.get(_mac): port[_mac] = set()
		port[_mac].add(ip)
	return {'interfaces': op_dict }

# ------------------------------------------------------------------------------
# NOT WORKING AS EXPECTED
# ------------------------------------------------------------------------------
