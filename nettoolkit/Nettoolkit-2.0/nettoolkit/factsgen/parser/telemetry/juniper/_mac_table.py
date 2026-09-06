

from nettoolkit.cmn.fstr import blank_line, standardize_mac, mac_2digit_separated, mac_4digit_separated,if_standardize, get_juniper_int_type

def parse_juniper_mac_table(cmd_op):
    """Parses Juniper 'show ethernet-switching table' output into a normalized object list."""
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    mac_dict = {}
    
    for line in raw_lines:
        line = line.strip()
        if not line or any(line.startswith(x) for x in ["VLAN", "Ethernet", "Total", "---"]):
            continue
            
        spl = line.split()
        if len(spl) < 4:
            continue
            
        # Juniper layout: [VLAN_NAME, MAC, Type, Age, Interfaces]
        vlan_name = spl[0]
        raw_mac = spl[1]
        mac_type = spl[2].lower()
        intf_name = spl[-1]  # Grab trailing index to handle optional age token shifts safely

        filter = get_juniper_int_type(intf_name)
        if not filter: continue
        intf_name = if_standardize(intf_name)
        if not mac_dict.get(filter):
            mac_dict[filter] = {}
        int_type_dict = mac_dict[filter]

        if not int_type_dict.get(intf_name):
            int_type_dict[intf_name] = {'mac':[]}
        individual_intf_dict = int_type_dict[intf_name]['mac']

        individual_intf_dict.append ( {
            'mac_address': raw_mac.lower(),
            'vlan': vrf_clean_vlan_name(vlan_name),
            'type': 'dynamic' if mac_type == 'learn' else mac_type,
            # 'interface': intf_name
        })
        
    return mac_dict

# ==============================================================================
# HELPER UTILITIES
# ==============================================================================

def vrf_clean_vlan_name(vlan_raw_name):
    """Strips common textual naming wrappers from VLAN columns to return clear identifiers."""
    clean = vlan_raw_name.lower().replace('vlan', '')
    return int(clean) if clean.isdigit() else vlan_raw_name

# ==============================================================================
# PIPELINE REGISTRATION REGISTER HOOK ENGINES
# ==============================================================================

def get_mac_table(cmd_op):
    """Bridge interface matching task registers hook for MAC tables."""
    data = parse_juniper_mac_table(cmd_op)
    return {'op_dict':  data}
