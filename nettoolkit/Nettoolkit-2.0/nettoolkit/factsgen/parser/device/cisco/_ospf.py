"""cisco show running-config parser for ospf section output """

# ------------------------------------------------------------------------------
from nettoolkit.addressing import addressing, invmask_to_mask, to_dec_mask
# ------------------------------------------------------------------------------

"""cisco show running-config parser for ospf section output """

# ------------------------------------------------------------------------------
# from nettoolkit.cmn.fdict import get_appeneded_value, merge_dict
from nettoolkit.addressing import addressing, invmask_to_mask, to_dec_mask
# ------------------------------------------------------------------------------

def parse_ospf_configuration(cmd_op):
    """
    Parses OSPF configurations in a single pass to maximize performance.
    Captures complete advanced routing parameters, including comprehensive 
    redistribution parameters, path tags, metric overrides, and area boundaries.
    """
    ospf_data = {}
    active_process = None
    
    for line in cmd_op:
        raw_line = line
        line = line.strip()
        if not line:
            continue
            
        # 1. Detect entering OSPF Router process context
        if line.startswith("router ospf "):
            spl = line.split()
            process_id = spl[2]
            
            # Safely capture VRF association regardless of token length shifts
            vrf_name = spl[spl.index("vrf") + 1] if "vrf" in spl else ""
            
            if process_id not in ospf_data:
                ospf_data[process_id] = {
                    'ospf_vrf': vrf_name,
                    'router_id': None,
                    'passive_interface_default': False,
                    'active_interfaces': [],
                    'passive_interfaces': [],
                    'redistribute': [],            # <-- Initialized container for protocols
                    'areas': {}
                }
            active_process = ospf_data[process_id]
            continue
            
        # 2. Detect top level configuration context exits
        if active_process is not None and (line == "!" or not raw_line.startswith(" ")):
            active_process = None
            continue
            
        # 3. Process parameters inside an active OSPF block
        if active_process is not None:
            spl = line.split()
            if not spl:
                continue
                
            # Handle Router ID
            if spl[0] == 'router-id':
                active_process['router_id'] = spl[-1]
                
            # Handle Passive-Interface Profiles completely
            elif "passive-interface" in spl:
                if "default" in spl:
                    active_process['passive_interface_default'] = True
                elif spl[0] == "no":
                    active_process['active_interfaces'].append(spl[-1])
                else:
                    active_process['passive_interfaces'].append(spl[-1])
                    
            # OSPF Redistribution
            elif spl[0] == "redistribute":
                redis_entry = {
                    'protocol': None,
                    'subnets': 'subnets' in spl,          # Crucial Cisco classless boolean indicator
                    'nssa_only': 'nssa-only' in spl,      # Limits route injection inside NSSA areas
                    'route_map': None,
                    'metric': None,
                    'metric_type': None,
                    'tag': None
                }
                
                # Dynamically isolate the source protocol string block (e.g., 'bgp 65000' or 'static')
                # Scans for where parameters start to end the protocol grouping index safely
                param_keywords = ['subnets', 'route-map', 'metric', 'metric-type', 'tag', 'nssa-only']
                protocol_end_idx = len(spl)
                for kw in param_keywords:
                    if kw in spl:
                        protocol_end_idx = min(protocol_end_idx, spl.index(kw))
                
                redis_entry['protocol'] = " ".join(spl[1:protocol_end_idx])
                
                # Match policy filters and target structural identifiers dynamically
                if "route-map" in spl:
                    try:
                        rm_idx = spl.index("route-map") + 1
                        if rm_idx < len(spl): redis_entry['route_map'] = spl[rm_idx]
                    except ValueError: pass
                    
                if "metric" in spl and "metric-type" not in spl:
                    try:
                        m_idx = spl.index("metric") + 1
                        if m_idx < len(spl): redis_entry['metric'] = int(spl[m_idx])
                    except (ValueError, IndexError): pass
                    
                if "metric-type" in spl:
                    try:
                        mt_idx = spl.index("metric-type") + 1
                        if mt_idx < len(spl): redis_entry['metric_type'] = int(spl[mt_idx]) # Capture E1 vs E2 metric pathing
                    except (ValueError, IndexError): pass
                    
                if "tag" in spl:
                    try:
                        t_idx = spl.index("tag") + 1
                        if t_idx < len(spl): redis_entry['tag'] = int(spl[t_idx])
                    except (ValueError, IndexError): pass
                    
                active_process['redistribute'].append(redis_entry)
                    
            # 1. Handle Network statement area mapping cleanly
            elif spl[0] == 'network':
                try:
                    subnet = spl[1]
                    mask = invmask_to_mask(spl[2])
                    area_id = spl[spl.index('area') + 1]
                    network_cidr = str(addressing(f"{subnet}/{mask}"))
                    
                    # Elegant single-line initialization protection
                    area_entry = active_process['areas'].setdefault(area_id, {'authentication': 'none', 'networks': [], 'range_summaries': []})
                    area_entry['networks'].append(network_cidr)
                except (ValueError, IndexError):
                    pass
                    
            # 2. Handle Area Summary Ranges
            elif spl[0] == 'area' and 'range' in spl:
                try:
                    area_id = spl[1]
                    subnet = spl[3]
                    mask = to_dec_mask(spl[4])
                    prefix_cidr = str(addressing(f"{subnet}/{mask}"))
                    
                    area_entry = active_process['areas'].setdefault(area_id, {'authentication': 'none', 'networks': [], 'range_summaries': []})
                    area_entry['range_summaries'].append(prefix_cidr)
                except (ValueError, IndexError):
                    pass

            # 3. Handle Area Authentication Status Tracking (Updates the key instead of rebuilding the dict)
            elif spl[0] == 'area' and 'authentication' in spl:
                try:
                    area_id = spl[1]
                    area_entry = active_process['areas'].setdefault(area_id, {'authentication': 'none', 'networks': [], 'range_summaries': []})
                    
                    # We mutate ONLY the specific authentication parameter string, leaving networks/summaries completely untouched
                    area_entry['authentication'] = 'message-digest' if 'message-digest' in spl else 'cleartext'
                except (ValueError, IndexError):
                    pass


    # Clean up unpopulated tracking elements before outputting to ensure clean YAML aesthetics
    for pid, attr in list(ospf_data.items()):
        if not attr['passive_interfaces']: del attr['passive_interfaces']
        if not attr['active_interfaces']: del attr['active_interfaces']
        if not attr['redistribute']: del attr['redistribute']
        if not attr['router_id']: del attr['router_id']
        
        for area_id, area_data in list(attr['areas'].items()):
            if not area_data['networks']: 
                del area_data['networks']
            if not area_data['range_summaries']: 
                del area_data['range_summaries']
            if area_data['authentication'] == 'none' and len(area_data) == 1:
                del attr['areas'][area_id]
            if not area_data: 
                del attr['areas'][area_id]
        if not attr['areas']: 
            del attr['areas']

    return ospf_data

def get_ospf(cmd_op, *args):
    return {'op_dict': {'ospf': parse_ospf_configuration(cmd_op)}}

