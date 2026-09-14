"""juniper bgp protocol routing instances parsing from set config  """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.flist import add_to_list_if_missing
from nettoolkit.crypt.jpw import doller9_dec
# ------------------------------------------------------------------------------

def parse_juniper_bgp_single_pass(cmd_op):
    """
    Parses Juniper BGP settings in a single pass to maximize performance.
    Extracts networks, redistribution policies, aggregates, and routing filters
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()

    bgp_database = {
        'global_bgp': {'router_id': None},
        'vrfs': {}
    }

    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
            
        spl = line.split()
        if not spl or spl[0] != "set":
            continue

        # ======================================================================
        # 1. PARSE ROUTING-OPTIONS (Router-ID & Aggregate Routes)
        # ======================================================================
        if "routing-options" in spl:
            try:
                # Discover context VRF inside a routing-instance block
                vrf_context = 'default'
                if "routing-instances" in spl:
                    vrf_context = spl[spl.index("routing-instances") + 1]
                
                _ensure_vrf_exists(bgp_database, vrf_context)
                af_block = bgp_database['vrfs'][vrf_context]['address_families']['ipv4_unicast']

                # --- Capture BGP Router-ID ---
                if "router-id" in spl:
                    rid = spl[spl.index("router-id") + 1]
                    if vrf_context == 'default':
                        bgp_database['global_bgp']['router_id'] = rid
                    else:
                        bgp_database['vrfs'][vrf_context]['router_id'] = rid

                # --- Capture Aggregates (`aggregate route X.X.X.X/X`) ---
                elif "aggregate" in spl and "route" in spl:
                    agg_idx = spl.index("route") + 1
                    agg_prefix = spl[agg_idx]
                    
                    # Prevent duplicate aggregate tracking registrations
                    agg_entry = next(
                        (
                            item
                            for item in af_block['aggregates']
                            if item['prefix'] == agg_prefix
                        ),
                        None,
                    )

                    if agg_entry is None:
                        agg_entry = {'prefix': agg_prefix}
                        af_block['aggregates'].append(agg_entry)

                    if 'discard' in spl:
                        agg_entry['discard'] = True

                    if 'as-set' in spl:
                        agg_entry['as_set'] = True

                    if 'policy' in spl:
                        policy_idx = spl.index('policy') + 1
                        if policy_idx < len(spl):
                            agg_entry['route_map'] = spl[policy_idx]

            except IndexError:
                pass
            continue

        # ======================================================================
        # 2. PARSE BGP PROTOCOLS LAYER (Groups, Neighbors, & Filters)
        # ======================================================================
        if 'protocols' not in spl or 'bgp' not in spl or 'group' not in spl:
            continue
            
        proto_idx = spl.index('protocols')
        if "prefix-list" in spl and spl.index('prefix-list') < proto_idx:
            continue
        if len(spl) <= proto_idx + 3 or spl[proto_idx+1] != 'bgp' or spl[proto_idx+2] != 'group':
            continue

        # Dynamic VRF Context Discovery for BGP lines
        vrf_context = 'default'
        if proto_idx > 1 and spl[proto_idx-2] == 'routing-instances':
            vrf_context = spl[proto_idx-1]

        _ensure_vrf_exists(bgp_database, vrf_context)
        af_block = bgp_database['vrfs'][vrf_context]['address_families']

        # Isolate Group Name and Neighbor IP
        group_name = spl[proto_idx+3]
        is_neighbor_line = 'neighbor' in spl and spl.index('neighbor') > proto_idx + 3
        
        if is_neighbor_line:
            nbr_idx = spl.index('neighbor') + 1
            if nbr_idx >= len(spl): continue
            peer_ip = spl[nbr_idx]

            af_name = (
                'ipv6_unicast'
                if is_neighbor_line and ":" in peer_ip
                else 'ipv4_unicast'
            )
            af_block = af_block[af_name]
            
            if peer_ip not in af_block['neighbors']:
                af_block['neighbors'][peer_ip] = {'peergrp': group_name}
            target_dict = af_block['neighbors'][peer_ip]
            attr_start_idx = nbr_idx + 1
        else:
            af_block = af_block['ipv4_unicast']
            if group_name not in af_block['peer_groups']:
                af_block['peer_groups'][group_name] = {}
            target_dict = af_block['peer_groups'][group_name]
            attr_start_idx = proto_idx + 4

        # Extract statements dynamically into our targeted container layout
        if attr_start_idx < len(spl):
            keyword = spl[attr_start_idx]
            
            if keyword == 'description':
                desc = " ".join(spl[attr_start_idx+1:]).strip('"')
                target_dict['peer_description'] = desc
                
            elif keyword == 'authentication-key':
                pw = " ".join(spl[attr_start_idx+1:]).strip().split("##")[0].strip('"')
                # try:
                #     pw = doller9_dec(pw)
                # except Exception:
                #     pass
                target_dict['peer_password'] = pw
                
            elif keyword == 'peer-as':
                target_dict['peer_as'] = int(spl[attr_start_idx+1]) if spl[attr_start_idx+1].isdigit() else spl[attr_start_idx+1]
                
            elif keyword == 'local-as':
                target_dict['local_as'] = int(spl[attr_start_idx+1]) if spl[attr_start_idx+1].isdigit() else spl[attr_start_idx+1]
                
            elif keyword == 'multihop':
                ttl = 255

                if (
                    attr_start_idx + 2 < len(spl)
                    and spl[attr_start_idx + 1] == 'ttl'
                    and spl[attr_start_idx + 2].isdigit()
                ):
                    ttl = int(spl[attr_start_idx + 2])

                target_dict['ebgp_multihop'] = ttl                

            # --- NEW: Extract Inbound/Outbound Policies (Route-Maps / Prefix-Lists) ---
            elif keyword in ['import', 'export']:
                policy_name = spl[attr_start_idx+1].strip('"')
                
                if 'policies' not in target_dict:
                    target_dict['policies'] = {}
                
                # Standardize directional policy naming keys to align with Cisco's formatting
                target_key = f"inbound_route_map" if keyword == 'import' else "outbound_route_map"
                if not target_dict['policies'].get(target_key):
                    target_dict['policies'][target_key] = policy_name
                else:
                    target_dict['policies'][target_key] = add_to_list_if_missing(target_dict['policies'][target_key], policy_name)

    # ======================================================================
    # 3. PHASE 2: INFER NETWORKS & REDISTRIBUTION FROM JUNOS POLICY-STATEMENTS
    # ======================================================================
    # Because Juniper manages advertisements via centralized policy terms, we parse 
    # your policy lines to match Cisco's direct 'network' and 'redistribute' variables list
    _parse_junos_policies_for_bgp(raw_lines, bgp_database)

    # 4. Post-parsing cleanup: Remove empty array placeholders
    return _cleanup_bgp_database(bgp_database)


def _parse_junos_policies_for_bgp(raw_lines, db):
    """
    Parses 'set policy-options policy-statement' blocks dynamically.
    Translates Junos terms into Cisco-matching 'networks' and 'redistribute' structures.
    """
    active_policy = None
    policy_map = {}

    # Extract all policy definitions from the configuration text first
    for line in raw_lines:
        line = line.strip()
        if not line.startswith("set policy-options policy-statement"):
            continue
        spl = line.split()
        if len(spl) < 4:
            continue
            
        p_name = spl[3]
        if p_name not in policy_map:
            policy_map[p_name] = {'protocols': set(), 'prefixes': set()}
            
        # Track routing components inside policy terms
        if "route-filter" in spl:
            rf_idx = spl.index("route-filter") + 1
            policy_map[p_name]['prefixes'].add(spl[rf_idx])
        elif "protocol" in spl:
            proto_idx = spl.index("protocol") + 1
            policy_map[p_name]['protocols'].add(spl[proto_idx])

    # Cross-reference extracted policies against our active VRF export statements
    for vrf_name, vrf_data in db['vrfs'].items():
        af_block = vrf_data['address_families']['ipv4_unicast']
        
        # Gather all policy names actively tied to this BGP instance
        active_exports = []
        for g_data in af_block['peer_groups'].values():
            if 'policies' in g_data and 'outbound_route_map' in g_data['policies']:
                policy_obj = g_data['policies']['outbound_route_map']
                if isinstance(policy_obj, list):
                    active_exports.extend(policy_obj)
                else:
                    active_exports.append(policy_obj)
        for n_data in af_block['neighbors'].values():
            if 'policies' in n_data and 'outbound_route_map' in n_data['policies']:
                policy_obj = n_data['policies']['outbound_route_map']
                if isinstance(policy_obj, list):
                    active_exports.extend(policy_obj)
                else:
                    active_exports.append(policy_obj)

        for p_name in active_exports:
            if p_name in policy_map:
                # Rule A: If the policy explicitly matches 'protocol static/direct', it maps to 'networks'
                if any(pr in policy_map[p_name]['protocols'] for pr in ['static', 'direct']):
                    for pfx in policy_map[p_name]['prefixes']:
                        if pfx not in af_block['networks']:
                            af_block['networks'].append(pfx)
                            
                # Rule B: If the policy matches foreign internal dynamic layers (like 'ospf'), it maps to 'redistribute'
                for foreign_proto in policy_map[p_name]['protocols']:
                    if foreign_proto in ['ospf', 'rip', 'isis', 'connected']:
                        existing_redis = [r['protocol'] for r in af_block['redistribute']]
                        if foreign_proto not in existing_redis:
                            af_block['redistribute'].append({
                                'protocol': foreign_proto,
                                'route_map': p_name
                            })


def _ensure_vrf_exists(db, vrf_name):
    """Initializes the multi-layered dynamic nested dictionary schema structure."""
    if vrf_name not in db['vrfs']:
        db['vrfs'][vrf_name] = {
            'router_id': None,
            'address_families': {
                'ipv4_unicast': {
                    'networks': [],
                    'redistribute': [],
                    'aggregates': [],
                    'peer_groups': {},
                    'neighbors': {}
                },
                'ipv6_unicast': {
                    'networks': [],
                    'redistribute': [],
                    'aggregates': [],
                    'peer_groups': {},
                    'neighbors': {}
                }
            }
        }


def _cleanup_bgp_database(db):
    """Trims empty dictionary layers out to guarantee crisp YAML formatting."""
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


def get_bgps(cmd_op, *args):
    # This matches the final signature hook layout you defined
    bgp_data = parse_juniper_bgp_single_pass(cmd_op)
    return {'op_dict': {"bgp": bgp_data}}

