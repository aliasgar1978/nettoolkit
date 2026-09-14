"""juniper routes parsing from set config  """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.flist import add_to_list_if_missing
# ------------------------------------------------------------------------------

def parse_juniper_static_routes_single_pass(cmd_op):
    """
    Parses Juniper static routes (IPv4 & IPv6) in a single high-efficiency pass.
    Organizes pathways contextually to match our unified cross-vendor data model layout.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()

    routes_database = {}
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
        # spl_str = None

        if ' static route ' not in line:
            continue
        spl_route_str = line.split(' static route ') 
        rib_context = spl_route_str[0]
        version_key = (
            'ipv6'
            if ".inet6." in rib_context or "inet6.0" in rib_context
            else 'ipv4'
        )

        if len(spl_route_str) < 2: continue

        vrf_spl_sect = spl_route_str[0].split()
        route_spl_sect = spl_route_str[-1].split()
        if not route_spl_sect: continue
        vrf_context = 'default'
        if len(vrf_spl_sect) > 2 and vrf_spl_sect[1] == 'routing-instances':
            vrf_context = vrf_spl_sect[2]
        prefix = route_spl_sect[0]
        staging_key = (vrf_context, version_key, prefix)

        if staging_key not in route_staging_map:
            route_staging_map[staging_key] = {'prefix': prefix}
        route_entry = route_staging_map[staging_key]

        attributes_set = {'next-hop', 'qualified-next-hop', 'preference', 'tag'}
        for attribute in attributes_set:
            if attribute in  route_spl_sect:
                idx = route_spl_sect.index(attribute)
                attr_value = route_spl_sect[idx+1]
                if not route_entry.get(attribute):
                    route_entry[attribute] = attr_value
                else:
                    route_entry[attribute] = add_to_list_if_missing(route_entry[attribute], attr_value)


        # Preserve your custom internal comment checks and metadata tags exactly
        if " ## comment: " in raw_line:
            route_entry['remark'] = raw_line.split(" ## comment: ")[-1].strip('"')
        
        if "resolve" in route_spl_sect: route_entry['resolve'] = True
        if "retain" in route_spl_sect: route_entry['retain'] = True
        if  "discard" in route_spl_sect: route_entry['discard'] = True
        if  "reject" in route_spl_sect: route_entry['reject'] = True

    # ==========================================================================
    # PHASE 2: ALLOCATE STAGED OBJECTS INTO UNIFIED HIERARCHY
    # ==========================================================================
    for (vrf_name, af_key, prefix), entry in route_staging_map.items():

        if vrf_name == 'default':
            section = 'global_routes'
        else:
            section = 'vrf_routes'

        if not routes_database.get(section):
            routes_database[section] = {}
        if not routes_database[section].get(vrf_name):
            routes_database[section][vrf_name] = {}
        if not routes_database[section][vrf_name].get(af_key):
            routes_database[section][vrf_name][af_key] = []
        routes_list = routes_database[section][vrf_name][af_key]
        routes_list.append(entry)


    # 5. Clean up unpopulated root namespaces before returning data
    return routes_database

# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_routes(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    routes_data = parse_juniper_static_routes_single_pass(cmd_op)
    return {'op_dict': {'static': routes_data}}
