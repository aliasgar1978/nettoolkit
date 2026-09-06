"""cisco running-config - ip routes output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.addressing import addressing, inet_address
# ------------------------------------------------------------------------------

def parse_static_routes_single_pass(cmd_op):
    """
    Parses Cisco static routes (IPv4 & IPv6) in a single high-efficiency pass.
    Organizes pathways contextually by VRF instance to match our unified data model layout.
    """
    # Initialize our dynamic master routing template layout structure
    routes_database = {
        'global_routes': {'ipv4': [], 'ipv6': []},
        'vrf_routes': {}
    }
    
    for line in cmd_op:
        line = line.strip()
        if not line or line.startswith("!"): 
            continue
        if not line.startswith("ip route ") and not line.startswith("ipv6 route "): 
            continue
            
        spl = line.split()
        if not spl: 
            continue
            
        # 1. Isolate Core Address Version & Base Tracking Offset Metrics
        version = 4 if spl[0] == 'ip' else 6
        idx_offset = 0
        vrf_context = None
        
        # 2. Capture VRF Context Boundaries dynamically
        if spl[2] == 'vrf':
            vrf_context = spl[3]
            idx_offset += 2  # Adjust index calculation space forward over VRF tokens
            
        # 3. Dynamic Prefix and Next-Hop Extraction Block
        prefix = ""
        next_hop = ""
        
        try:
            if version == 4:
                network_ip = spl[idx_offset + 2]
                subnet_mask = spl[idx_offset + 3]
                prefix = inet_address(network_ip, subnet_mask)
                
                # Next-Hop can be an IP address string or an Interface egress tag (e.g. Null0 / Gi1)
                potential_nh = spl[idx_offset + 4]
                next_hop = potential_nh
                if potential_nh != "Null0":
                    idx_offset += 1
            else:
                # IPv6 route statements omit subnet mask fields natively
                prefix = spl[idx_offset + 2]
                potential_nh = spl[idx_offset + 3]
                next_hop = potential_nh
                idx_offset -= 1
        except IndexError:
            continue  # Guard against malformed or clipped configuration string layers
            
        # 4. Map Attributes Contextually into a Clean Dictionary Block Object
        route_entry = {
            'prefix': prefix,
            'next_hop': next_hop,
            'administrative_distance': get_singel_idx_item('Null0', spl) if 'Null0' in spl else get_administrative_dist(spl, next_hop, idx_offset),
            'tag': int(get_singel_idx_item('tag', spl)) if get_singel_idx_item('tag', spl) else None,
            'track': int(get_singel_idx_item('track', spl)) if get_singel_idx_item('track', spl) else None,
            'remark': get_multi_idx_item('name', spl)
        }
        
        # Cleanup unpopulated optional internal variables to keep final YAML tight
        if not route_entry['administrative_distance']: del route_entry['administrative_distance']
        if route_entry['tag'] is None: del route_entry['tag']
        if route_entry['track'] is None: del route_entry['track']
        if not route_entry['remark']: del route_entry['remark']

        # 5. Allocate the parsed object block into the safe nested directory hierarchy paths
        af_key = 'ipv4' if version == 4 else 'ipv6'
        
        if vrf_context:
            if vrf_context not in routes_database['vrf_routes']:
                routes_database['vrf_routes'][vrf_context] = {'ipv4': [], 'ipv6': []}
            routes_database['vrf_routes'][vrf_context][af_key].append(route_entry)
        else:
            routes_database['global_routes'][af_key].append(route_entry)
            
    # Remove unpopulated placeholders to maintain perfect block-style aesthetics
    return _cleanup_route_placeholders(routes_database)


def _cleanup_route_placeholders(d):
    """Strips unpopulated routing instances blocks out to guarantee crisp YAML formatting."""
    if not d['global_routes']['ipv4']: del d['global_routes']['ipv4']
    if not d['global_routes']['ipv6']: del d['global_routes']['ipv6']
    if not d['global_routes']: del d['global_routes']
    if not d['vrf_routes']: del d['vrf_routes']
    return d


# ==============================================================================
# Your Helper Utility Slicing Methods Preserved Exactly as Intended
# ==============================================================================

def index_of(item, lst):
    if item in lst: return lst.index(item)
    return ""

def get_singel_idx_item(item, lst):
    idx = index_of(item, lst)
    if idx and idx + 1 < len(lst): return lst[idx+1]
    return ""

def get_multi_idx_item(item, lst):
    candidates = {'vrf', 'Null0', 'tag', 'name', 'track'}
    my_idx = index_of(item, lst)
    if not my_idx: return ""
    max_idx = len(lst)
    others_idx = {index_of(c, lst):c for c in candidates if index_of(c, lst)}
    for k in sorted(others_idx.keys()):
        if k > my_idx:
            max_idx = k
            break
    return " ".join(lst[my_idx+1:max_idx])

def get_administrative_dist(spl, next_hop, idx_distance):
    if len(spl) >= idx_distance + 5 and spl[idx_distance+4].isnumeric():
        return spl[idx_distance+4]
    return ''

def get_routes(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    return {'op_dict': parse_static_routes_single_pass(cmd_op)}