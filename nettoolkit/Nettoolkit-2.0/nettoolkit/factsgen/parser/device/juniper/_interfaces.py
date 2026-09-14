"""juniper interface from config command output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line, interface_type, get_juniper_int_type
from nettoolkit.cmn.flist import create_and_add_to_list, add_to_list_if_missing
from nettoolkit.cmn.networking import get_vlans_juniper
from nettoolkit.addressing import get_subnet, get_v6_subnet, IPv6
from nettoolkit.crypt.jpw import doller9_dec
# ------------------------------------------------------------------------------

def parse_juniper_interfaces_single_pass(cmd_op):
    """
    Parses Juniper interface configurations in a single high-efficiency pass.
    Transforms the legacy flat layout into a modern, nested YAML data model.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    
    ports_dict = {}
    
    # Pre-extract voice vlans globally using your native logic
    voice_vlans = _extract_voice_vlans(raw_lines)
    
    # Phase 1: Track interface configurations and sub-modes contextually
    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
            
        spl = line.split()
        if not spl or spl[0] != "set":
            continue

        # --- PROCESS INTERFACE PROPERTY LINES ---
        if line.startswith("set interfaces ") and not line.startswith("set interfaces interface-range"):
            if len(spl) < 3:
                continue
                
            # Isolate the core parent interface identity token (e.g. ge-0/0/0 or ae1)
            raw_if_name = spl[2]
            
            # Determine the logical unit overlay structure context cleanly
            unit_id = None
            if "unit" in spl:
                try:
                    unit_id = spl[spl.index("unit") + 1]
                except IndexError:
                    pass
            
            # Determine the parent hardware group category name string (e.g. ethernet)
            filter_type = get_juniper_int_type(raw_if_name)
            
            # Initialize our standardized nested layout blocks safely on the fly
            if filter_type not in ports_dict:
                ports_dict[filter_type] = {}
            if raw_if_name not in ports_dict[filter_type]:
                ports_dict[filter_type][raw_if_name] = {}
                
            if unit_id is None:
                unit_dict = ports_dict[filter_type][raw_if_name]
            else:
                # Structuralize down into logical unit blocks to stop sub-interface data loss!
                if 'units' not in ports_dict[filter_type][raw_if_name]:
                    ports_dict[filter_type][raw_if_name]['units'] = {}

                if unit_id not in ports_dict[filter_type][raw_if_name]['units']:
                    ports_dict[filter_type][raw_if_name]['units'][unit_id] = {
                        'description': None,
                        # 'link_status': 'up',
                        'vrf': None,
                        'ipv4': {},
                        'ipv6': {},
                        'switchport': {},
                        'etherchannel': {},
                        'ospf': {}
                    }
                    
                unit_dict = ports_dict[filter_type][raw_if_name]['units'][unit_id]
            
            # Delegate line data collection contextually
            _parse_junos_metadata(unit_dict, line, spl)
            _parse_junos_ipv4(unit_dict, line, spl)
            _parse_junos_ipv6(unit_dict, line, spl)
            _parse_junos_switchport(unit_dict, line, spl, voice_vlans)
            _parse_junos_etherchannel(unit_dict, line, spl)

        # --- PROCESS ROUTING-INSTANCE ROUTER VRF BINDINGS DYNAMICALLY ---
        elif line.startswith("set routing-instances ") and "interface" in spl:
            try:
                vrf_name = spl[2]
                target_if_token = spl[-1]  # Contains full string name (e.g., 'ge-0/0/0.0')
                
                # Split the string down to isolate parent port name and logical unit id bounds
                if "." in target_if_token:
                    p_name, u_id = target_if_token.split(".", 1)
                else:
                    p_name, u_id = target_if_token, "0"
                    
                f_type = get_juniper_int_type(p_name)
                
                # Safely inject the VRF string straight into the matching nested unit block container
                if f_type in ports_dict and p_name in ports_dict[f_type]:
                    if u_id in ports_dict[f_type][p_name]['units']:
                        ports_dict[f_type][p_name]['units'][u_id]['vrf'] = vrf_name

            except Exception:
                pass

        # --- PROCESS IN-LINE PROTOCOL OSPF AUTHENTICATION DETAILS ---
        elif "protocols" in spl and "ospf" in spl and "interface" in spl:
            _parse_junos_ospf_auth(ports_dict, spl)

    # Cleanup and polish unpopulated placeholders before returning to guarantee tight formatting
    return _cleanup_juniper_interface_placeholders(ports_dict)


# ==============================================================================
# Helper Sub-Handlers for Clean, Precise Code Separation
# ==============================================================================

def _parse_junos_metadata(unit_dict, line, spl):
    """Parses descriptions and active administrative states cleanly without redundancy."""
    # Initialize the standardized state dictionary on the fly if it hasn't been set
    if 'state' not in unit_dict:
        unit_dict['state'] = {
            'admin': 'up',       # Default configuration state assumption
            # 'protocol': 'up'     # Default protocol state assumption
        }

    if "description" in spl:
        desc_idx = spl.index("description") + 1
        if desc_idx < len(spl):
            unit_dict['description'] = " ".join(spl[desc_idx:]).strip('"')
            
    # In Junos 'set' configs, if a port is shut down, it appends the trailing keyword 'disable'
    elif "disable" in spl:
        unit_dict['state']['admin'] = 'down'
        # unit_dict['state']['protocol'] = 'down'


def _parse_junos_ipv4(unit_dict, line, spl):
    """Parses standard family inet parameters."""
    if "family" in spl and "inet" in spl and "address" in spl:
        try:
            addr_idx = spl.index("address") + 1
            if addr_idx < len(spl):
                if not unit_dict['ipv4'].get('subnet'):
                    unit_dict['ipv4']['subnet'] = spl[addr_idx]
                else:
                    unit_dict['ipv4']['subnet'] = add_to_list_if_missing(unit_dict['ipv4']['subnet'], spl[addr_idx])
                    
        except ValueError:
            pass


def _parse_junos_ipv6(unit_dict, line, spl):
    """Parses standard family inet6 network infrastructure layers."""
    if "family" in spl and "inet6" in spl and "address" in spl:
        try:
            addr_idx = spl.index("address") + 1
            if addr_idx < len(spl):
                v6_addr = spl[addr_idx]
                # Exclude link-local fe80:: blocks safely from standard variable captures
                if not v6_addr.lower().startswith("fe80:"):
                    if not unit_dict['ipv6'].get('subnet'):
                        unit_dict['ipv6']['subnet'] = v6_addr
                    else:
                        unit_dict['ipv6']['subnet'] = add_to_list_if_missing(unit_dict['ipv6']['subnet'], v6_addr)
                    # if "/" in v6_addr:
                    #     unit_dict['ipv6']['h4_block'] = v6_addr.split(":")
        except ValueError:
            pass


def _parse_junos_switchport(unit_dict, line, spl, voice_vlans):
    """Parses layer-2 interface switching metrics, trunks, and access allocations."""
    if "interface-mode" in spl or "port-mode" in spl:
        mode_keyword = "interface-mode" if "interface-mode" in spl else "port-mode"
        unit_dict['switchport']['mode'] = spl[spl.index(mode_keyword) + 1]
        
    if "vlan" in spl and "members" in spl:
        vlans = get_vlans_juniper(spl, "s")
        if vlans:
            vlan_str = ",".join(vlans)
            mode = unit_dict['switchport'].get('mode', 'access')
            key = 'vlan_members' if mode == 'trunk' else 'access_vlan'
            
            if unit_dict['switchport'].get(key):
                unit_dict['switchport'][key] = f"{unit_dict['switchport'][key]},{vlan_str}"
            else:
                unit_dict['switchport'][key] = vlan_str
                
            for vlan in vlans:
                if vlan in voice_vlans:
                    unit_dict['switchport']['voice_vlan'] = vlan


def _parse_junos_etherchannel(unit_dict, line, spl):
    """Parses 802.3ad link aggregation / aggregated Ethernet attachments."""
    if "802.3ad" in spl:
        try:
            ae_idx = spl.index("802.3ad") + 1
            if ae_idx < len(spl):
                ae_intf = spl[ae_idx]  # e.g., 'ae1'
                ae_id = ae_intf.replace('ae', '')
                unit_dict['etherchannel'] = {
                    'id': int(ae_id) if ae_id.isdigit() else ae_id,
                    'interface': ae_intf,
                    'mode': 'active'
                }
        except ValueError:
            pass


def _parse_junos_ospf_auth(ports_dict, spl):
    """Parses OSPF network type and credentials directly out of routing protocol lines."""
    try:
        if "interface" in spl:
            if_idx = spl.index("interface") + 1
            if if_idx < len(spl):
                target_if = spl[if_idx]
                if "." in target_if:
                    p_name, u_id = target_if.split(".", 1)
                else:
                    p_name, u_id = target_if, "0"
                    
                f_type = get_juniper_int_type(p_name)
                
                if f_type in ports_dict and p_name in ports_dict[f_type]:
                    if u_id in ports_dict[f_type][p_name]['units']:
                        unit_ospf = ports_dict[f_type][p_name]['units'][u_id]['ospf']
                        
                        if "interface-type" in spl:
                            unit_ospf['network_type'] = spl[spl.index("interface-type") + 1]
                        if "authentication" in spl:
                            raw_key = " ".join(spl[spl.index("authentication") + 1:]).strip('"')
                            # try:
                            #     unit_ospf['authentication_key'] = doller9_dec(raw_key)
                            # except Exception:
                            unit_ospf['authentication_key'] = raw_key
    except Exception:
        pass

# def _get_clean_filter_type(if_name):
#     """Safely categorizes the parent hardware filter key name."""
#     if if_name.startswith("ge-") or if_name.startswith("xe-") or if_name.startswith("et-"):
#         return 'ethernet'
#     elif if_name.startswith("ae"):
#         return 'aggregated'
#     elif if_name.startswith("lo"):
#         return 'loopback'
#     elif if_name.startswith("irb") or if_name.startswith("vlan"):
#         return 'vlan'
#     return 'other'


def _extract_voice_vlans(raw_lines):
    """Gathers set of VoIP voice VLAN IDs from global switch options."""
    voice_vlans = set()
    for l in raw_lines:
        if "set switch-options voip interface" in l and "vlan" in l:
            spl = l.split()
            if spl[-2] == 'vlan':
                voice_vlans.add(spl[-1])
    return voice_vlans


def _cleanup_juniper_interface_placeholders(ports_dict):
    """Trims empty dictionary namespaces to keep output YAML compact."""
    for filter_type, interfaces in list(ports_dict.items()):
        for p, parent_attr in list(interfaces.items()):
            if 'units' in parent_attr:
                for unit_id, attr in list(parent_attr['units'].items()):
                    if not attr['description']: del attr['description']
                    if not attr['vrf']: del attr['vrf']
                    if not attr['ipv4']: del attr['ipv4']
                    if not attr['ipv6']: del attr['ipv6']
                    if not attr['switchport']: del attr['switchport']
                    if not attr['etherchannel']: del attr['etherchannel']
                    if not attr['ospf']: del attr['ospf']

                    # Clean out the initialized state dictionary if it didn't deviate from standard up/up
                    # (This keeps active, standard functional interfaces exceptionally tiny and tidy!)
                    if attr.get('state') == {'admin': 'up'}:
                        del attr['state']
                                            
                # If all logical units are cleaned out, drop the units dictionary
                if not parent_attr['units']: del parent_attr['units']
            if not parent_attr: del interfaces[p]
        if not interfaces: del ports_dict[filter_type]
    return ports_dict


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_interfaces(cmd_op, *args):
    interfaces_dict = parse_juniper_interfaces_single_pass(cmd_op) or {}
    return {'op_dict': interfaces_dict}