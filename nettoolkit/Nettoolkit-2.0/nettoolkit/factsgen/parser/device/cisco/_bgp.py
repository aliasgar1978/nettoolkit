"""cisco running-config parser for bgp section output """

# ------------------------------------------------------------------------------
from nettoolkit.addressing import inet_address
from nettoolkit.crypt.cpw import type7_dec
# ------------------------------------------------------------------------------

def iterate_families_lines(bgp_lines):
    group_of_lines = split_families(bgp_lines)
    
    # Initialize the standardized Option B hierarchy database blueprint
    unified_bgp_database = {
        'global_bgp': {'router_id': None},
        'vrfs': {}
    }
    
    for af, lines in group_of_lines.items():
        # Determine the contextual VRF parent container name string dynamically
        # Raw formats: 'global bgp', 'ipv4 vrf PRODUCTION', 'ipv6 vrf DMZ'
        vrf_context = 'default'
        af_type = 'ipv4_unicast'  # Standard default assumption fallback
        
        if 'vrf' in af:
            try:
                spl_af = af.split()
                vrf_context = spl_af[spl_af.index('vrf') + 1]
            except (ValueError, IndexError):
                pass
                
        if 'ipv6' in af:
            af_type = 'ipv6_unicast'
            
        # Ensure our standardized nested VRF data blueprint container exists on the fly
        if vrf_context not in unified_bgp_database['vrfs']:
            unified_bgp_database['vrfs'][vrf_context] = {
                'router_id': None,
                'address_families': {
                    'ipv4_unicast': {
                        'networks': [], 'redistribute': [], 'aggregates': [],
                        'peer_groups': {}, 'neighbors': {}
                    },
                    'ipv6_unicast': {
                        'networks': [], 'redistribute': [], 'aggregates': [],
                        'peer_groups': {}, 'neighbors': {}
                    }
                }
            }

        # Initialize a clean, distinct layout for this specific routing block staging area
        staging_dict = {
            'router_id': None,
            'networks': [],
            'redistribute': [],
            'aggregates': [],
            'peer_groups': {},
            'neighbors': {}
        }
        
        # Extract standard identity metrics & routing policies cleanly
        # by passing the targeted root dictionary down
        for line in lines:
            spl = line.strip().split()
            if not spl: continue
            bgp_other_attributes(staging_dict, spl)

        # Pull peer groups and neighbors dynamically 
        # and merge their keys directly onto our root context layout
        peers_data = parse_all_bgp_peers(lines)
        staging_dict['peer_groups'] = peers_data['peer_groups']
        staging_dict['neighbors'] = peers_data['neighbors']
        
        # Map global top-level keys out contextually
        if staging_dict['router_id']:
            if vrf_context == 'default':
                unified_bgp_database['global_bgp']['router_id'] = staging_dict['router_id']
            else:
                unified_bgp_database['vrfs'][vrf_context]['router_id'] = staging_dict['router_id']

        # Pack the operational parameters directly into the clean nested address family sub-node
        target_af = unified_bgp_database['vrfs'][vrf_context]['address_families'][af_type]
        target_af['networks'] = staging_dict['networks']
        target_af['redistribute'] = staging_dict['redistribute']
        target_af['aggregates'] = staging_dict['aggregates']
        target_af['peer_groups'] = staging_dict['peer_groups']
        target_af['neighbors'] = staging_dict['neighbors']

    # Cleanup Empty Arrays before packaging to ensure clean YAML aesthetics
    return _cleanup_normalized_cisco_bgp(unified_bgp_database)


def _cleanup_normalized_cisco_bgp(db):
    """Trims unpopulated placeholders out to match our precise architectural aesthetics."""
    if not db['global_bgp']['router_id']:
        del db['global_bgp']
        
    for vrf_name, vrf_data in list(db['vrfs'].items()):
        if not vrf_data['router_id']:
            del vrf_data['router_id']
            
        for af_name, af_data in list(vrf_data['address_families'].items()):
            if not af_data['networks']: del af_data['networks']
            if not af_data['redistribute']: del af_data['redistribute']
            if not af_data['aggregates']: del af_data['aggregates']
            if not af_data['peer_groups']: del af_data['peer_groups']
            if not af_data['neighbors']: del af_data['neighbors']
            
            if not af_data:
                del vrf_data['address_families'][af_name]
        if not vrf_data['address_families']:
            del vrf_data['address_families']
        if not vrf_data:
            del db['vrfs'][vrf_name]
            
    return db


def split_families(bgp_lines):
    group_of_lines = {}
    group_name = None
    in_bgp_context = False    
    for line in bgp_lines:
        raw_line = line
        line = line.strip()
        if not line or line == "!":
            continue        
        if line.startswith('router bgp '):
            group_name = 'global bgp'
            in_bgp_context = True
        elif line.startswith("address-family "):
            group_name = line.split('address-family ')[-1]
            in_bgp_context = False
        elif line.startswith("exit-address-family"):
            group_name = None

        if not group_name: continue

        # 2. Dynamic Exit Intercept: Stop processing line-by-line if the BGP block concludes
        if in_bgp_context and raw_line.rstrip() == "!":
                break  # Stops processing entirely, ignoring all subsequent configuration lines

        if group_name not in group_of_lines:
            group_of_lines[group_name] = []
        active_group = group_of_lines[group_name]
        active_group.append(line)
    return group_of_lines


def parse_all_bgp_peers(lines):
    """
    Parses a block of lines and extracts BOTH peer groups and standard neighbors,
    automatically categorizing them and keeping their attributes separate.
    """
    peers_data = {
        'peer_groups': {},
        'neighbors': {}
    }
    
    # First pass: Identify which names are actually peer groups
    # This prevents the state-machine ordering issue entirely.
    known_peer_groups = set()
    for line in lines:
        spl = line.strip().split()
        if len(spl) == 3 and spl[0] == 'neighbor' and spl[2] == 'peer-group':
            known_peer_groups.add(spl[1])
            peers_data['peer_groups'][spl[1]] = {}

    # Second pass: Extract properties safely
    for line in lines:
        spl = line.strip().split()
        if not spl or spl[0] != 'neighbor' or len(spl) < 3:
            continue
            
        target_name = spl[1]
        
        # Determine whether we are writing attributes to a Peer-Group or a real Neighbor IP
        if target_name in known_peer_groups:
            # Skip the initial structural definition line 'neighbor X peer-group'
            if len(spl) == 3 and spl[2] == 'peer-group':
                continue
            bgp_peer_attributes(peers_data['peer_groups'][target_name], spl)
        else:
            if target_name not in peers_data['neighbors']:
                peers_data['neighbors'][target_name] = {'peer_ip': target_name}
            bgp_peer_attributes(peers_data['neighbors'][target_name], spl)
            
    return peers_data



def bgp_peer_attributes(op_dict, spl=[]):
    """parser function to update bgp neighbor attribute details

    Args:
        port_dict (dict): dictionary with a bgp neighbour info
        spl (list): splitted line to parse

    Returns:
        None: None
    """
    if not spl or len(spl) < 3:
        return 
    identifiers = {
        'remote-as': ('peer_as', int),
        'update-source': ('update_source', str),
        'ebgp-multihop': ('ebgp_multihop', int),          
        'local-as': ('local_as', int),
        'peer-group': ('peergrp', str),
        'next-hop-self': ('next_hop_self', bool),      # Captures true if present
        'send-community': ('send_community', str),     # Captures 'both', 'extended', etc.
    }
    for keyword, (yaml_key, data_type) in identifiers.items():
        if keyword in spl:
            try:
                value_idx = spl.index(keyword) + 1
                
                # Safeguard: Skip the initial peer-group structural line 
                # (e.g., 'neighbor PG_NAME peer-group' where keyword is at the end)
                if keyword == 'peer-group' and value_idx == len(spl):
                    continue

                if value_idx < len(spl):
                    raw_value = spl[value_idx]
                    op_dict[yaml_key] = data_type(raw_value)
            except (ValueError, TypeError):
                pass
                
    # ==========================================
    # 2. Context-Heavy / Multi-Word Attributes
    # ==========================================

    # Handle Descriptions (handles multi-word strings with spaces)
    if "description" in spl:
        desc_idx = spl.index("description") + 1
        if desc_idx < len(spl):
            op_dict['peer_description'] = " ".join(spl[desc_idx:])

    # ==========================================================
    # Dynamic Routing Policy Extraction Loop (No String Formatting)
    # ==========================================================
    # Format: keyword: (base_yaml_key_suffix, directional_bool)
    policy_identifiers = {
        'route-map': ('_route_map', True),
        'prefix-list': ('_prefix_list', True),
        'unsuppress-map': ('unsuppress_map', False)
    }

    for keyword, (key_suffix, is_directional) in policy_identifiers.items():
        if keyword in spl:
            try:
                kw_idx = spl.index(keyword)
                if kw_idx + 1 < len(spl):
                    map_name = spl[kw_idx + 1]
                    
                    # 1. Initialize the policies sub-dictionary
                    if 'policies' not in op_dict:
                        op_dict['policies'] = {}
                    
                    # 2. exact storage key cleanly
                    if is_directional:
                        dir_mod = spl[-1] if spl[-1] in ["in", "out"] else "in"
                        # Result Example: "inbound_route_map" or "outbound_route_map"
                        target_key = f"{'inbound' if dir_mod == 'in' else 'outbound'}{key_suffix}"
                    else:
                        target_key = key_suffix
                    
                    # 3. Save the property
                    op_dict['policies'][target_key] = map_name
            except (ValueError, IndexError):
                pass

    # ==========================================================
    # Handle Passwords (safely strips out Type 7 encryption flags)
    # ==========================================================
    if "password" in spl:
        pass_idx = spl.index("password") + 1
        if pass_idx < len(spl):
            if spl[pass_idx] == "7" and pass_idx + 1 < len(spl):
                op_dict["peer_password"] = type7_dec(spl[pass_idx + 1])
            else:
                op_dict["peer_password"] = spl[pass_idx]


def bgp_other_attributes(op_dict, spl):
    bgp_router_id(op_dict, spl)
    bgp_networks(op_dict, spl)
    bgp_redistribute(op_dict, spl)
    bgp_aggregates(op_dict, spl)


def bgp_router_id(op_dict, spl):
    if len(spl) >= 3 and spl[0] == "bgp" and spl[1] == 'router-id':
        op_dict['router_id'] = spl[-1]
def bgp_networks(op_dict, spl):
    if len(spl) >= 2 and spl[0] == "network":
        if 'networks' not in op_dict:
            op_dict['networks'] = []
            
        network_ip = spl[1]
        mask = None

        # clean CIDR string (e.g., '2001:db8::/64' or '10.1.1.0/24')
        if "/" in network_ip:
            op_dict['networks'].append(network_ip)
            return
        
        # standard statement with an explicit trailing mask
        if "mask" in spl:
            try:
                mask_idx = spl.index("mask") + 1
                if mask_idx < len(spl):
                    mask = spl[mask_idx]
            except (ValueError, IndexError):
                pass

        # explicit masks + classful fallbacks
        op_dict['networks'].append(inet_address(network_ip, mask))

def bgp_redistribute(op_dict, spl):
    if spl[0] == "redistribute":
        # Initialize the list container if it doesn't exist yet
        if 'redistribute' not in op_dict or not isinstance(op_dict['redistribute'], list):
            op_dict['redistribute'] = []
        # Create a dictionary for this specific redistribution rule
        redis_entry = {}
        route_map_keyword = "route-map"

        if route_map_keyword in spl:
            rm_idx = spl.index(route_map_keyword)
            # The protocol string is everything between 'redistribute' (index 0) and 'route-map'
            # e.g., ["redistribute", "ospf", "1", "route-map", "MY_MAP"] -> ["ospf", "1"]
            protocol_parts = spl[1:rm_idx]
            redis_entry['protocol'] = " ".join(protocol_parts)
            redis_entry['route_map'] = spl[rm_idx + 1]
            
        else:
            # 2. if no route-map is used
            # e.g., ["redistribute", "connected"] or ["redistribute", "ospf", "1"]
            redis_entry['protocol'] = " ".join(spl[1:])
            redis_entry['route_map'] = None
            
        # Optional: metrics if exist
        if "metric" in spl:
            metric_idx = spl.index("metric")
            redis_entry['metric'] = int(spl[metric_idx + 1])

        # Append this formatted block to our tracking list
        op_dict['redistribute'].append(redis_entry)

def bgp_aggregates(op_dict, spl):
    if spl[0] == "aggregate-address":
        # Ensure the tracking list exists so we append rather than overwrite
        if 'aggregates' not in op_dict or not isinstance(op_dict['aggregates'], list):
            op_dict['aggregates'] = []

        # clean CIDR string (e.g., '2001:db8::/64' or '10.1.1.0/24')
        if "/" in spl[1]:
            prefix_str = spl[1]
        else:
            # Parse the network prefix/mask into a single CIDR string or IP object
            # safely handling exceptions if index 1 or 2 are missing
            try:
                prefix_str = inet_address(spl[1], spl[2])
            except IndexError:
                return  # Malformed config line, skip processing
        # Create a clean dictionary for this specific aggregate path rule
        agg_entry = {
            'prefix': prefix_str,
            'summary_only': 'summary-only' in spl,
            'as_set': 'as-set' in spl
        }		
        target_maps  = ('route-map', 'attribute-map', 'advertise-map')
        for map_keyword  in target_maps :
            if map_keyword  in spl:
                rm_idx = spl.index(map_keyword) + 1
                agg_entry[map_keyword.replace('-', '_')] = spl[rm_idx]

        # Append this formatted block cleanly to your main output object
        op_dict['aggregates'].append(agg_entry)


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_bgp(cmd_op, *args):
    """defines set of methods executions. to get various bgp native parameters.
    uses BGP in order to get all.

    Args:
        cmd_op (list, str): running config output, either list of multiline string

    Returns:
        dict: output dictionary with parsed with system fields
    """    	
    af_nbr_attributes = iterate_families_lines(cmd_op)
    return {'op_dict': {'bgp': af_nbr_attributes}}