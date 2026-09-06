"""juniper routing instances parsing from set config  """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.flist import add_to_list_if_missing
# ------------------------------------------------------------------------------

def parse_juniper_instances_single_pass(cmd_op):
    """
    Parses Juniper routing instances in a single high-efficiency pass.
    Transforms legacy flat Excel variables into our unified nested VRF schema layout.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    instances_database = {}

    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if not line.startswith("set routing-instances "):
            continue
            
        spl = line.split()
        if len(spl) < 4:
            continue
            
        vrf_name = spl[2]
        
        # Initialize our standardized cross-vendor nested layout blocks safely on the fly
        if vrf_name not in instances_database:
            instances_database[vrf_name] = {
                'description': None,
                'route_distinguisher': None,
                'route_targets': {
                    'import': [],
                    'export': []
                }
            }
            
        vrf_block = instances_database[vrf_name]
        keyword = spl[3]

        # --- 1. Extract Descriptions Safely ---
        if keyword == 'description':
            desc = " ".join(spl[4:]).strip()
            if desc.startswith('"') and desc.endswith('"'):
                desc = desc[1:-1]
            vrf_block['description'] = desc

        # --- 2. Extract Route Distinguishers (Preserves full context string!) ---
        elif keyword == 'route-distinguisher':
            vrf_block['route_distinguisher'] = spl[-1].strip().strip('"')

        # --- 3. Extract Route Targets (Handles Target: formats, imports, and exports) ---
        elif keyword == 'vrf-target':
            # Junos format can be standalone or directional:
            # set routing-instances X vrf-target target:65000:10 (both)
            # set routing-instances X vrf-target import target:65000:10 (import only)
            try:
                if 'import' in spl or 'export' in spl:
                    direction = 'import' if 'import' in spl else 'export'
                    target_val = spl[-1].split('target:')[-1].strip().strip('"')
                    add_to_list_if_missing(vrf_block['route_targets'][direction], target_val)
                else:
                    # Global target line sets both import and export rules simultaneously
                    target_val = spl[-1].split('target:')[-1].strip().strip('"')
                    add_to_list_if_missing(vrf_block['route_targets']['import'], target_val)
                    add_to_list_if_missing(vrf_block['route_targets']['export'], target_val)
            except (ValueError, IndexError):
                pass

    # Post-parsing cleanup: Remove empty array placeholders to ensure clean formatting
    return _cleanup_juniper_instances(instances_database)


def _cleanup_juniper_instances(db):
    """Trims empty initialization fields out to guarantee clean block-style YAML formatting."""
    for vrf_name, attr in list(db.items()):
        if not attr['description']: del attr['description']
        if not attr['route_distinguisher']: del attr['route_distinguisher']
        
        # Clean up route targets if no values were ever populated
        if not attr['route_targets']['import']: del attr['route_targets']['import']
        if not attr['route_targets']['export']: del attr['route_targets']['export']
        if not attr['route_targets']: del attr['route_targets']
        
        # If the entire VRF object becomes completely empty, remove the root node container
        if not db[vrf_name]:
            del db[vrf_name]
            
    return db


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_instances(cmd_op, *args):
    # Synchronizes perfectly with your main context-aware 'main()' registers map pipeline loop
    vrf_data = parse_juniper_instances_single_pass(cmd_op)
    if not vrf_data:
        vrf_data['dummy_instance'] = ''
    return {'op_dict': vrf_data}
