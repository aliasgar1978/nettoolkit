"""juniper routes parsing from set config  """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
# ------------------------------------------------------------------------------

def parse_juniper_static_routes_single_pass(cmd_op):
    """
    Parses Juniper static routes (IPv4 & IPv6) in a single high-efficiency pass.
    Organizes pathways contextually to match our unified cross-vendor data model layout.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()

    # Initialize a clean database layout structure that mirrors our Cisco blueprint exactly
    routes_database = {
        'global_routes': {'ipv4': [], 'ipv6': []},
        'vrf_routes': {}
    }

    # Tracking dictionary dynamically aggregates multi-next-hop properties before list conversion
    # Key format: (vrf_name, version_key, prefix) -> route_object_dict
    route_staging_map = {}

    for line in raw_lines:
        raw_line = line
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if not line.startswith("set "):
            continue

        # 1. Determine IP Version and String Split Target dynamically
        version_key = None
        spl_str = None
        
        if ' routing-options static route ' in line:
            version_key = 'ipv4'
            spl_str = ' routing-options static route '
        elif ' routing-options rib ' in line and ' static route ' in line:
            version_key = 'ipv6'
            # Extracts dynamic rib name or matches your standard structure cleanly
            if 'blue.inet6.0' in line:
                spl_str = ' routing-options rib blue.inet6.0 static route '
            else:
                # Fallback guard to handle alternative IPv6 RIB naming variables
                try:
                    rib_idx = line.find(' routing-options rib ')
                    route_idx = line.find(' static route ')
                    spl_str = line[rib_idx : route_idx + 14]
                except ValueError:
                    continue

        if not spl_str or not version_key:
            continue

        # 2. Slice configuration segments relative to the anchor token
        vrf_spl_route = line.split(spl_str)
        vrf_spl_sect = vrf_spl_route[0].split()
        route_spl_sect = vrf_spl_route[-1].split()
        if not route_spl_sect:
            continue

        prefix = route_spl_sect[0]
        
        # 3. Dynamic VRF Context Discovery
        # If 'routing-instances' is present at index 1, extract instance string name
        vrf_context = 'default'
        if len(vrf_spl_sect) > 2 and vrf_spl_sect[1] == 'routing-instances':
            vrf_context = vrf_spl_sect[2]

        # Generate a distinct compound tracking tuple key for this specific subnet pathway
        staging_key = (vrf_context, version_key, prefix)

        if staging_key not in route_staging_map:
            # Initialize a cohesive, non-prefixed entry object
            route_staging_map[staging_key] = {
                'prefix': prefix,
                'next_hop': [],           # Initialized as a clean native list array!
                'administrative_distance': None,
                'tag': None,
                'remark': None,
                'resolve': None,
                'retain': None
            }
            
        route_entry = route_staging_map[staging_key]

        # 4. Extract trailing properties inline using your explicit logic matching parameters
        if len(route_spl_sect) > 2:
            keyword = route_spl_sect[1]
            
            if keyword == 'next-hop':
                next_hop_target = route_spl_sect[2]
                if next_hop_target not in route_entry['next_hop']:
                    route_entry['next_hop'].append(next_hop_target)
                    
            elif keyword == 'preference':
                route_entry['administrative_distance'] = int(route_spl_sect[2])
                
            elif keyword == 'tag':
                route_entry['tag'] = int(route_spl_sect[2])

        # Preserve your custom internal comment checks and metadata tags exactly
        if " ## comment: " in raw_line:
            route_entry['remark'] = raw_line.split(" ## comment: ")[-1].strip('"')
        if " resolve" in line:
            route_entry['resolve'] = True
        if " retain" in line:
            route_entry['retain'] = True

    # ==========================================================================
    # PHASE 2: ALLOCATE STAGED OBJECTS INTO UNIFIED HIERARCHY
    # ==========================================================================
    for (vrf_name, af_key, prefix), entry in route_staging_map.items():
        
        # Clean up unpopulated tracking elements before sorting into final blocks
        if not entry['next_hop']: 
            entry['next_hop'] = None
        elif len(entry['next_hop']) == 1:
            # Flatten to a single string value if only one target exists to match Cisco format
            entry['next_hop'] = entry['next_hop'][0]
            
        if entry['administrative_distance'] is None: del entry['administrative_distance']
        if entry['tag'] is None: del entry['tag']
        if entry['remark'] is None: del entry['remark']
        if entry['resolve'] is None: del entry['resolve']
        if entry['retain'] is None: del entry['retain']
        if entry['next_hop'] is None: del entry['next_hop']

        # Allocate metrics contextually to mirror the Cisco layout exactly
        if vrf_name == 'default':
            routes_database['global_routes'][af_key].append(entry)
        else:
            if vrf_name not in routes_database['vrf_routes']:
                routes_database['vrf_routes'][vrf_name] = {'ipv4': [], 'ipv6': []}
            routes_database['vrf_routes'][vrf_name][af_key].append(entry)

    # 5. Clean up unpopulated root namespaces before returning data
    return _cleanup_juniper_route_database(routes_database)


def _cleanup_juniper_route_database(d):
    """Strips unpopulated routing instances blocks out to guarantee crisp YAML formatting."""
    if not d['global_routes']['ipv4']: del d['global_routes']['ipv4']
    if not d['global_routes']['ipv6']: del d['global_routes']['ipv6']
    if not d['global_routes']: del d['global_routes']
    if not d['vrf_routes']: del d['vrf_routes']
    return d


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_routes(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    routes_data = parse_juniper_static_routes_single_pass(cmd_op)
    return {'op_dict': {'static': routes_data}}
