"""juniper arp table command output parser """

# ------------------------------------------------------------------------------
from collections import OrderedDict

from nettoolkit.cmn.fstr import blank_line, standardize_mac, mac_2digit_separated, mac_4digit_separated,if_standardize, get_juniper_int_type
# ------------------------------------------------------------------------------

# def get_arp_table(cmd_op, *args):
# 	"""parser - show arp command output

# 	Parsed Fields:
# 		* port/interface 
# 		* ip
# 		* mac, mac2, mac4
# 		* dns
# 		* vlan

# 	Args:
# 		cmd_op (list, str): command output in list/multiline string.

# 	Returns:
# 		dict: output dictionary with parsed fields
# 	"""
# 	op_dict = OrderedDict()

# 	nbr_d, remote_hn = {}, ""
# 	nbr_table_start = False
# 	for l in cmd_op:
# 		if blank_line(l): continue
# 		if l.strip().startswith("#"): continue
# 		spl = l.strip().split()
# 		_mac = standardize_mac(spl[0])
# 		ip = spl[1]
# 		dns = spl[2].split(".")[0]
# 		if dns.isdigit(): dns = spl[2]
# 		try:
# 			vlan = spl[3]	
# 			p = spl[4].replace("[","").replace("]","").split(".")[0]
# 			_add_arp(op_dict, p, _mac, ip, dns, vlan)
# 			_add_arp(op_dict, vlan, _mac, ip, dns, vlan)
# 		except: pass
# 		## add/modify for ae interface as well to add arp if need.

# 	return {'op_dict': op_dict}
# # ------------------------------------------------------------------------------
# def _add_arp(op_dict, p, _mac, ip, dns, vlan):
# 	"""add the detais to output dictionary

# 	Args:
# 		op_dict (dict): dicationary with/without info
# 		p (str): port
# 		_mac (str): mac address
# 		ip (str): ip address
# 		dns (str): dns name
# 		vlan (str): vlan number
# 	"""    	
# 	if not op_dict.get(p): op_dict[p] = {'neighbor': {}}
# 	nbr = op_dict[p]['neighbor']
# 	if not nbr.get("mac"): nbr["mac"] = set()
# 	if not nbr.get("mac2"): nbr["mac2"] = set()
# 	if not nbr.get("mac4"): nbr["mac4"] = set()
# 	if not nbr.get("ip"): nbr["ip"] = set()
# 	if not nbr.get("dns"): nbr["dns"] = set()
# 	if not nbr.get("vlan"): nbr["vlan"] = set()
# 	nbr["mac"].add(standardize_mac(_mac))
# 	nbr['mac2'].add(mac_2digit_separated(_mac))
# 	nbr['mac4'].add(mac_4digit_separated(_mac))
# 	nbr["ip"].add(ip)
# 	nbr["dns"].add(dns)
# 	nbr['vlan'].add(vlan.replace("irb.",""))
# # ------------------------------------------------------------------------------


def parse_juniper_arp_table(cmd_op):
    """Parses Juniper 'show arp' output into a normalized object list."""
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    arp_dict = {}
    
    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("MAC") or line.startswith("Total"):
            continue
            
        spl = line.split()
        if len(spl) < 4:
            continue

        for i, x in enumerate(spl):
            filter = get_juniper_int_type(x)
            if filter: break
        if not filter: 
            continue

        raw_mac = spl[0]
        ip_addr = spl[1]
        intf_name = spl[i]

        filter = get_juniper_int_type(intf_name)
        if not filter: continue
        intf_name = if_standardize(intf_name)
        if not arp_dict.get(filter):
            arp_dict[filter] = {}
        int_type_dict = arp_dict[filter]

        if not int_type_dict.get(intf_name):
            int_type_dict[intf_name] = {'arp':[]}
        individual_intf_dict = int_type_dict[intf_name]['arp']

        individual_intf_dict.append ( {
            'ip_address': ip_addr,
            'mac_address': raw_mac.lower(),
            # 'interface': intf_name,
            # 'age_mins': 0  # Junos 'show arp' doesn't explicitly track a minute timer column
        })

    return arp_dict

# ==============================================================================
# PIPELINE REGISTRATION REGISTER HOOK ENGINES
# ==============================================================================
def get_arp_table(cmd_op):
    """Bridge interface matching task registers hook for ARP tables."""
    data = parse_juniper_arp_table(cmd_op)
    return {'op_dict': data}

