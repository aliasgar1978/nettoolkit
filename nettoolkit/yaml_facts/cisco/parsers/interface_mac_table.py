"""cisco show mac address-table command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_mac_address_table(command_output):
	op_dict = {}
	start = False
	for l in command_output:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		if l.startswith("Multicast"): break
		spl = l.strip().split()
		try:
			if spl[2].upper() != 'DYNAMIC': continue
		except: continue
		p = spl[-1]
		#
		int_filter = get_cisco_int_type(p)
		if not op_dict.get(int_filter):
			op_dict[int_filter] = {}
		int_filter_dict = op_dict[int_filter]
		if not int_filter_dict.get(p): 
			int_filter_dict[p] = {}
		nbr = int_filter_dict[p]
		#
		if not nbr.get("mac"): nbr["mac"] = set()
		if not nbr.get("mac2"): nbr["mac2"] = set()
		if not nbr.get("mac4"): nbr["mac4"] = set()
		nbr["mac"].add(standardize_mac(spl[1]))
		nbr['mac2'].add(mac_2digit_separated(spl[1]))
		nbr['mac4'].add(mac_4digit_separated(spl[1]))

	return {'interfaces': op_dict }
# ------------------------------------------------------------------------------
# NOT WORKING AS EXPECTED
# ------------------------------------------------------------------------------
