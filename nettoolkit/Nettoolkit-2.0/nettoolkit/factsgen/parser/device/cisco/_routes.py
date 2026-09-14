"""cisco running-config - ip routes output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line, if_standardize, is_interface
from nettoolkit.addressing import addressing, inet_address
# ------------------------------------------------------------------------------

def parse_static_routes_single_pass(cmd_op):
    routes_database = {}
    for line in cmd_op:
        line = line.strip()
        if not line or line.startswith("!"): 
            continue
        if not line.startswith("ip route ") and not line.startswith("ipv6 route "): 
            continue
        spl = line.strip().split()
        if spl[0] == 'ip': route_version = 'ipv4' 
        elif spl[0] == 'ipv6': route_version = 'ipv6'
        else: continue

        spl = spl[2:]
        vrf_name = None
        if spl[0] == 'vrf':
            vrf_name = spl[1]
            spl = spl[2:]

        if route_version == 'ipv4':
            prefix = inet_address(spl[0], spl[1])
            spl = spl[2:]
        elif route_version == 'ipv6':
            prefix = spl[0]
            spl = spl[1:]
        else: 
            continue

        try:
            nexthop_interface = ''
            if is_interface(spl[0]):
                nexthop_interface = spl[0]
                spl = spl[1:]
        except:
            pass

        nexthop = ''
        if len(spl)> 0:
            if spl[0].lower().startswith('null'):
                nexthop = spl[0]
                spl = spl[1:]
            else:
                try:
                    addressing(spl[0])
                    nexthop = spl[0]
                    spl = spl[1:]
                except:
                    pass

        if not nexthop and not nexthop_interface:
            print(f"[-] Invalid or no NextHop defined {line}. skipped")
            continue


        attributes_set = { 'tag', 'track', 'name' }
        attributes = {}
        for attribute in attributes_set:
            if attribute not in  spl: continue
            idx = spl.index(attribute)
            if idx+1 <= len(spl):
                attribute_value = spl[idx+1]
                attributes[attribute] = attribute_value
                spl.pop(idx+1)
                spl.pop(idx)

        if len(spl) > 0:
            if spl[0].isdigit():
                attributes['distance'] = int(spl[0])        

        subnet_dict = {
            'instance': vrf_name, 
            'prefix': prefix,
            'version': route_version,
            'nexthop_interface': nexthop_interface,
            'nexthop': nexthop,
        }
        subnet_dict.update(attributes)
        if vrf_name:
            subnet_dict.update( {'instance': vrf_name})
            

        if vrf_name:
            section = 'vrf_routes'
        else:
            section = 'global_routes'

        if not routes_database.get(section):
            routes_database[section] = {}
        if not routes_database[section].get(route_version):
            routes_database[section][route_version] = []
        routes_list = routes_database[section][route_version]
        routes_list.append(subnet_dict)

    return routes_database

# ==========================================================================================

def get_routes(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    return {'op_dict': parse_static_routes_single_pass(cmd_op)}