"""cisco show mac address-table command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line,standardize_mac, mac_4digit_separated, mac_2digit_separated, get_cisco_int_type, if_standardize
# ------------------------------------------------------------------------------

# def get_mac_table(cmd_op, *args):
# 	"""parser - show mac address-table command output

# 	Parsed Fields:
# 		* port/interface
# 		* neighbor mac
# 		* neighbor mac2
# 		* neighbor mac4

# 	Args:
# 		cmd_op (list, str): command output in list/multiline string.

# 	Returns:
# 		dict: output dictionary with parsed fields
# 	"""	
# 	op_dict = {}
# 	start = False
# 	for l in cmd_op:
# 		if blank_line(l): continue
# 		if l.strip().startswith("!"): continue
# 		if l.startswith("Multicast"): break
# 		spl = l.strip().split()
# 		try:
# 			if spl[2].upper() != 'DYNAMIC': continue
# 		except: continue
# 		p = spl[-1]
# 		if not op_dict.get(p): op_dict[p] = {}
# 		nbr = op_dict[p]
# 		if not nbr.get("mac"): nbr["mac"] = set()
# 		if not nbr.get("mac2"): nbr["mac2"] = set()
# 		if not nbr.get("mac4"): nbr["mac4"] = set()
# 		nbr["mac"].add(standardize_mac(spl[1]))
# 		nbr['mac2'].add(mac_2digit_separated(spl[1]))
# 		nbr['mac4'].add(mac_4digit_separated(spl[1]))

# 	return {'op_dict': op_dict }
# # ------------------------------------------------------------------------------
# # NOT WORKING AS EXPECTED
# # ------------------------------------------------------------------------------

# ==============================================================================
# 2. MAC ADDRESS TABLE PARSERS SUITE
# ==============================================================================

def parse_cisco_mac_table(cmd_op):
    """Parses Cisco 'show mac address-table' output into a normalized object list."""
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    mac_dict = {}
    
    for line in raw_lines:
        line = line.strip()
        if not line or any(line.startswith(x) for x in ["vlan", "----", "Total", "Mac"]):
            continue
            
        spl = line.split()
        if len(spl) < 4:
            continue
            
        # Cisco layout: [VLAN, MAC, Type, Ports/Interfaces]
        vlan_id = spl[0]
        raw_mac = spl[1]
        mac_type = spl[2].lower()
        intf_name = spl[3]
        
        # Filter CPU self-learned macro rows safely
        if intf_name.lower() in ['cpu', 'vlan', 'router']:
            continue
            
        clean_mac = mac_2digit_separated(raw_mac)

        filter = get_cisco_int_type(intf_name)
        if not filter: continue
        intf_name = if_standardize(intf_name)
        if not mac_dict.get(filter):
            mac_dict[filter] = {}
        int_type_dict = mac_dict[filter]

        if not int_type_dict.get(intf_name):
            int_type_dict[intf_name] = {'mac':[]}
        individual_intf_dict = int_type_dict[intf_name]['mac']

        individual_intf_dict.append({
            'mac_address': clean_mac,
            'vlan': int(vlan_id) if vlan_id.isdigit() else vlan_id,
            'type': mac_type,
        })
        
    return mac_dict

def get_mac_table(cmd_op):
    """Bridge interface matching task registers hook for MAC tables."""
    data = parse_cisco_mac_table(cmd_op)
    return {'op_dict': data}
