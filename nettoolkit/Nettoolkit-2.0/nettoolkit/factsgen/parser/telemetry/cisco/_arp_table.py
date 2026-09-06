"""cisco show arp table command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line, if_standardize, standardize_mac, get_cisco_int_type, mac_2digit_separated
# ------------------------------------------------------------------------------

# def get_arp_table(cmd_op, *args):
#     """parser - show ip arp command output

#     Parsed Fields:
#         * port/interface 
#         * ip address
#         * mac address

#     Args:
#         cmd_op (list, str): command output in list/multiline string.

#     Returns:
#         dict: output dictionary with parsed fields
#     """    	
#     op_dict = {}
#     start = False
#     for l in cmd_op:
#         if blank_line(l): continue
#         if l.strip().startswith("!"): continue
#         if l.startswith("Protocol"): continue
#         if l.find("Incomplete")>0: continue
#         if l.strip().startswith("%") and l.endswith("does not exist."): continue
#         spl = l.strip().split()
#         p = None
#         try:
#             p = if_standardize(spl[-1])
#             _mac = standardize_mac(spl[3])
#             ip = spl[1]
#         except:
#             pass
#         if p:
#             filter = get_cisco_int_type(p)
#             if not op_dict.get(filter):
#                 op_dict[filter] = {}
#             int_type_dict = op_dict[filter]

#         if not int_type_dict.get(p): int_type_dict[p] = {}
#         port = int_type_dict[p]
#         if not port.get(_mac): port[_mac] = set()
#         port[_mac].add(ip)
#     return {'op_dict': op_dict }

# ------------------------------------------------------------------------------


"""cisco and juniper standalone arp/mac text table grid parsers """

import re

# ==============================================================================
# 1. ARP TABLE PARSERS SUITE
# ==============================================================================

def parse_cisco_arp_table(cmd_op):
    """Parses Cisco 'show ip arp' output into a normalized object list."""
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    
    arp_dict ={}
    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("Protocol") or line.startswith("-"):
            continue
            
        spl = line.split()
        if len(spl) < 6:
            continue
            
        # Cisco format index array layout positions:
        # [Protocol, IP, Age, MAC, Type, Interface]
        ip_addr = spl[1]
        age_val = spl[2]
        raw_mac = spl[3]
        intf_name = spl[5]
        
        if raw_mac == 'Incomplete' or raw_mac == '-':
            continue

        # Normalize Cisco dot-notation MACs (0011.22aa.bbcc) to clean standard colons
        clean_mac = mac_2digit_separated(raw_mac)

        filter = get_cisco_int_type(intf_name)
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
            'mac_address': clean_mac,
            'age_mins': 0 if age_val == '-' else int(age_val)
        })
        
    return arp_dict


# ==============================================================================
# HELPER UTILITIES
# ==============================================================================

# ==============================================================================
# PIPELINE REGISTRATION REGISTER HOOK ENGINES
# ==============================================================================
def get_arp_table(cmd_op):
    """Bridge interface matching task registers hook for ARP tables."""
    data = parse_cisco_arp_table(cmd_op)
    return {'op_dict': data}
