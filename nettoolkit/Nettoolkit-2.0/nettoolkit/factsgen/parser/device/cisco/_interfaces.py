"""cisco show running-config parser for interface section outputs """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line, interface_type
from nettoolkit.cmn.flist import create_and_add_to_list
from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.networking import get_interface_cisco, get_vlans_cisco
from nettoolkit.addressing import get_subnet, get_inet_address, get_secondary_inet_address, get_v6_subnet, get_inetv6_address, IPv6
from nettoolkit.crypt.cpw import type7_dec
# ------------------------------------------------------------------------------

def parse_interfaces_single_pass(cmd_op):
    """
    Parses Cisco interface configurations in a single pass.
    Delegates extraction to small, modular sub-handlers.
    """
    ports_dict = {}
    port_dict = None
    
    for line in cmd_op:
        raw_line = line
        line = line.strip()
        if not line or line == "!":
            continue
            
        # 1. Detect entering an individual Interface Configuration Block
        if line.startswith("interface "):
            p = get_interface_cisco(raw_line)
            if not p:
                port_dict = None
                continue
                
            # Tuple unwrapping fix applied ([0])
            filter_type = interface_type(line.split("interface ")[-1])[0].lower()
            
            if filter_type not in ports_dict:
                ports_dict[filter_type] = {}
            if p not in ports_dict[filter_type]:
                ports_dict[filter_type][p] = {
                    'description': None, 'link_status': 'up', 'vrf': None,
                    'ipv4': {}, 'ipv6': {}, 'switchport': {},
                    'etherchannel': {}, 'ospf': {}, 'udld': None
                }
                
            port_dict = ports_dict[filter_type][p]
            continue

        # 2. Delegate parsing to targeted helper functions if context is active
        if port_dict is not None:
            _parse_global_metadata(port_dict, line)
            _parse_ipv4_params(port_dict, line, raw_line)
            _parse_ipv6_params(port_dict, line, raw_line)
            _parse_switchport_params(port_dict, line)
            _parse_etherchannel_params(port_dict, line)
            _parse_routing_policies(port_dict, line)

    # 3. Post-parsing cleanup: Remove unpopulated block placeholders
    return _cleanup_empty_placeholders(ports_dict)


# ==============================================================================
# Helper Sub-Handlers for Clean, Precise Code Separation
# ==============================================================================

def _parse_global_metadata(port_dict, line):
    """Parses top-level interface metadata like descriptions and VRFs."""
    if line.startswith("description "):
        port_dict['description'] = line[12:].strip()
    elif line == "shutdown":
        port_dict['link_status'] = 'administratively down'
    elif line.startswith("vrf forwarding ") or line.startswith("ip vrf forwarding "):
        port_dict['vrf'] = line.split()[-1]
    elif line.startswith("udld port "):
        port_dict['udld'] = line[10:].strip()


def _parse_ipv4_params(port_dict, line, raw_line):
    """Parses standard IPv4 addresses and helpers contextually."""
    if line.startswith("ip address "):
        address = get_inet_address(raw_line)
        secondary_address = get_secondary_inet_address(raw_line)
        if address: 
            port_dict['ipv4']['subnet'] = get_subnet(address)
        if secondary_address: 
            port_dict['ipv4']['subnet_secondary'] = get_subnet(secondary_address)
            
    elif line.startswith("ip helper-address "):
        helper = line.split()[-1]
        if 'helpers' not in port_dict['ipv4']:
            port_dict['ipv4']['helpers'] = []
        create_and_add_to_list(port_dict['ipv4']['helpers'], helper)


def _parse_ipv6_params(port_dict, line, raw_line):
    """Parses standard IPv6 infrastructure parameters safely."""
    if line.startswith("ipv6 address ") and "anycast" not in line and "link-local" not in line:
        address = get_inetv6_address(raw_line, link_local=False)
        if address:
            try:
                port_dict['ipv6']['subnet'] = get_v6_subnet(address)
                port_dict['h4_block'] = IPv6(address).getHext(4)
            except Exception:
                pass
                
    elif line.startswith("ipv6 dhcp relay destination "):
        helper = line.split()[-1]
        if 'helpers' not in port_dict['ipv6']:
            port_dict['ipv6']['helpers'] = []
        create_and_add_to_list(port_dict['ipv6']['helpers'], helper)


def _parse_switchport_params(port_dict, line):
    """Parses Layer-2 VLAN allocations and modes."""
    if line.startswith("switchport mode "):
        port_dict['switchport']['mode'] = line.split()[-1]
        
    elif "switchport access vlan" in line or "switchport trunk allowed vlan" in line:
        vlans = get_vlans_cisco(line)
        if vlans:
            for k, v in vlans.items():
                if v:
                    clean_key = k.replace('interface_', '')
                    if port_dict['switchport'].get(clean_key):
                        port_dict['switchport'][clean_key] = f"{port_dict['switchport'][clean_key]},{v}"
                    else:
                        port_dict['switchport'][clean_key] = str(v)


def _parse_etherchannel_params(port_dict, line):
    """Parses Port-channel attachments and modes."""
    if line.startswith("channel-group "):
        spl = line.split()
        if len(spl) >= 3:
            po_id = spl[1]
            port_dict['etherchannel'] = {
                'id': int(po_id),
                'interface': f"Port-channel{po_id}",
                'mode': spl[-1]
            }


def _parse_routing_policies(port_dict, line):
    """Parses link-level OSPF configurations."""
    if line.startswith("ip ospf authentication-key "):
        raw_key = line.split()[-1]
        try:
            port_dict['ospf']['authentication_key'] = type7_dec(raw_key)
        except Exception:
            port_dict['ospf']['authentication_key'] = raw_key
            
    elif line.startswith("ip ospf network "):
        port_dict['ospf']['network_type'] = line.split()[-1]


def _cleanup_empty_placeholders(ports_dict):
    """Trims empty initialization dictionaries out to keep the final YAML clean."""
    for filter_type, interfaces in list(ports_dict.items()):
        for p, attr in list(interfaces.items()):
            if not attr['description']: del attr['description']
            if not attr['vrf']: del attr['vrf']
            if not attr['udld']: del attr['udld']
            if not attr['ipv4']: del attr['ipv4']
            if not attr['ipv6']: del attr['ipv6']
            if not attr['switchport']: del attr['switchport']
            if not attr['etherchannel']: del attr['etherchannel']
            if not attr['ospf']: del attr['ospf']
    return ports_dict


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_interfaces(cmd_op, *args):
    interfaces_dict = parse_interfaces_single_pass(cmd_op)
    if not interfaces_dict:
        interfaces_dict['dummy_int'] = ""
    return {'op_dict': interfaces_dict}