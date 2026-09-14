"""juniper ospf parsing from set config  """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.flist import add_to_list_if_missing
# ------------------------------------------------------------------------------

def parse_juniper_ospf_single_pass(cmd_op):
    """
    Parses Juniper OSPF configurations in a single high-efficiency pass.
    Transforms legacy flat tracking metrics into a unified, cross-vendor nested data model.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    
    ospf_database = {}

    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
            
        # Isolate the routing context boundary cleanly
        ospf_spl = line.split(" protocols ospf ")
        if len(ospf_spl) != 2: 
            continue
            
        spl = ospf_spl[-1].split()
        if not spl: 
            continue
            
        # Identify Process/VRF ID: Default to '1' if global 'set', otherwise extract VRF name string
        p_id = "1" if ospf_spl[0] == 'set' else ospf_spl[0].split()[-1]
        
        # Initialize our standardized cross-vendor database layout safely on the fly
        if p_id not in ospf_database:
            ospf_database[p_id] = {
                'ospf_vrf': "" if p_id == "1" else p_id,
                'areas': {}
            }
            
        vrf_block = ospf_database[p_id]

        # In Junos, OSPF parameters always exist under an explicit area token (e.g. area 0.0.0.0)
        if len(spl) >= 2 and spl[0] == 'area':
            area_id = spl[1]
            
            if area_id not in vrf_block['areas']:
                vrf_block['areas'][area_id] = {
                    'range': {},
                    'interfaces': {}
                }
                
            area_block = vrf_block['areas'][area_id]

            # --- Extract Area Range Summaries ---
            if "area-range" in spl:
                try:
                    pfx_idx = spl.index("area-range") + 1
                    if pfx_idx < len(spl):
                        prefix = spl[pfx_idx]
                        if prefix not in area_block['range']:
                            area_block['range'][prefix] = {
                                'summary_only': 'advertise' not in spl  # 'advertise' flag handles suppression context
                            }
                except ValueError:
                    pass

            # --- Extract Interface Specific Parameters ---
            elif "interface" in spl:
                try:
                    intf_idx = spl.index("interface") + 1
                    if intf_idx < len(spl):
                        interface_name = spl[intf_idx]
                        
                        if interface_name not in area_block['interfaces']:
                            area_block['interfaces'][interface_name] = {
                                'passive': False,
                                'network_type': None,
                                'authentication_key': None
                            }
                            
                        intf_block = area_block['interfaces'][interface_name]

                        # Handle Passive Interfaces
                        if spl[-1] == 'passive':
                            intf_block['passive'] = True
                            
                        # Handle OSPF Interface Types (Network Links Type)
                        elif "interface-type" in spl:
                            intf_block['network_type'] = spl[spl.index("interface-type") + 1]
                            
                        # Handle Authentication Credentials
                        elif "authentication" in spl:
                            try:
                                auth_idx = spl.index("authentication")
                                if 'key' in spl:
                                    auth_idx = spl.index("key")
                                intf_block['authentication_key'] = spl[auth_idx + 1]
                            except Exception:
                                pass
                except ValueError:
                    pass

    # Post-parsing cleanup: Remove empty array/dictionary placeholders to ensure clean formatting
    return _cleanup_juniper_ospf_placeholders(ospf_database)


def _cleanup_juniper_ospf_placeholders(db):
    """Trims empty initialization fields out to guarantee crisp YAML formatting."""
    for p_id, vrf_data in list(db.items()):
        for area_id, area_data in list(vrf_data['areas'].items()):
            if not area_data['range']: del area_data['range']
            
            # Clean up optional fields within interfaces inside this area
            for intf_name, intf_data in list(area_data['interfaces'].items()):
                if intf_data['passive'] is False: del intf_data['passive']
                if intf_data['network_type'] is None: del intf_data['network_type']
                if intf_data['authentication_key'] is None: del intf_data['authentication_key']
                if not intf_data: del area_data['interfaces'][intf_name]
                
            if not area_data['interfaces']: del area_data['interfaces']
            if not area_data: del vrf_data['areas'][area_id]
        if not vrf_data['areas']: del db[p_id]
    return db


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_ospfs(cmd_op, *args):
    """Bridges cleanly with your master centralized orchestration execution registers loop pipeline."""
    ospf_data = parse_juniper_ospf_single_pass(cmd_op)
    # Wraps the layout inside an explicit "ospf" key to match our data protection strategy
    return {'op_dict': {"ospf": ospf_data}}
