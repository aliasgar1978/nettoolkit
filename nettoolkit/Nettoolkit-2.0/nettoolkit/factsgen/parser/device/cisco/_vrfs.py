"""cisco show running-config parser for vrf level outputs """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.networking import get_vrf_cisco
# ------------------------------------------------------------------------------

def parse_vrfs_single_pass(cmd_op):
    """
    Parses Cisco VRF definitions in a single pass to maximize performance.
    Guards context boundaries strictly to prevent interface variables from bleeding into VRF definitions.
    """
    vrfs_dict = {}
    port_dict = None
    in_vrf_context = False  # Critical state guard to protect boundary blocks
    
    for line in cmd_op:
        raw_line = line
        line = line.strip()
        if not line:
            continue
            
        # 1. Detect entering a distinct top-level VRF definition context block
        if line.startswith("vrf definition ") or line.startswith("ip vrf ") or line.startswith("vrf "):
            p = get_vrf_cisco(raw_line)
            if not p:
                port_dict = None
                in_vrf_context = False
                continue
                
            if p not in vrfs_dict:
                vrfs_dict[p] = {
                    'description': None,
                    'route_distinguisher': None,
                    'route_targets': {
                        'import': [],
                        'export': []
                    },
                    'address_families': []
                }
            port_dict = vrfs_dict[p]
            in_vrf_context = True  # Explicitly lock execution inside a VRF block context
            continue

        # 2. Track Context Exits: An unindented line or standalone bang means the VRF section is over
        if in_vrf_context:
            if raw_line.startswith("!") or (raw_line and not raw_line.startswith(" ")):
                # If a line doesn't start with whitespace, we have stepped completely out of the VRF context
                # Except if it's an internal sub-mode keyword like exit-address-family which we skip
                if not line.startswith("exit-"):
                    port_dict = None
                    in_vrf_context = False
                    continue

        # 3. Extract configuration statements strictly inside the active VRF context area
        if in_vrf_context and port_dict is not None:
            
            # Handle Descriptions safely (Will never capture interface text anymore!)
            if line.startswith("description "):
                port_dict['description'] = line[12:].strip()
                
            # Handle Route Distinguishers (RD)
            elif line.startswith("rd "):
                port_dict['route_distinguisher'] = line.split(" ", 1)[-1].strip()
                
            # Handle Route Target Imports & Exports
            elif line.startswith("route-target "):
                spl = line.split()
                if len(spl) >= 3:
                    direction = spl[1]          # 'import' or 'export' or 'both'
                    rt_value = spl[2].strip()   # Full '65000:10' string
                    
                    if direction in ['import', 'both']:
                        if rt_value not in port_dict['route_targets']['import']:
                            port_dict['route_targets']['import'].append(rt_value)
                    if direction in ['export', 'both']:
                        if rt_value not in port_dict['route_targets']['export']:
                            port_dict['route_targets']['export'].append(rt_value)
                            
            # Handle Address-Family activations precisely
            elif line.startswith("address-family "):
                af_type = line.split()[-1]
                if af_type not in port_dict['address_families']:
                    port_dict['address_families'].append(af_type)

    # 4. Post-parsing cleanup: Remove unpopulated tracking nodes
    for vrf_name, attr in list(vrfs_dict.items()):
        if not attr['description']: del attr['description']
        if not attr['route_distinguisher']: del attr['route_distinguisher']
        if not attr['address_families']: del attr['address_families']
        
        if not attr['route_targets']['import']: del attr['route_targets']['import']
        if not attr['route_targets']['export']: del attr['route_targets']['export']
        if not attr['route_targets']: del attr['route_targets']
        
    return vrfs_dict

def get_vrfs(cmd_op, *args):
    vrf_result_dict = parse_vrfs_single_pass(cmd_op)
    if not vrf_result_dict:
        vrf_result_dict['dummy_vrf'] = ""
    return {'op_dict': vrf_result_dict}