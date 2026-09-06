"""juniper show interfaces terse command output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line, get_juniper_int_type
# ------------------------------------------------------------------------------

def parse_juniper_interfaces_terse_single_pass(cmd_op):
    """
    Parses 'show interfaces terse' command matrix grids in a single high-efficiency pass.
    Extracts live operational 'protocol' carrier states to match our unified data model layout.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()
    
    terse_database = {}

    for line in raw_lines:
        line = line.strip()
        # Skip header rows and empty tracking comment blocks safely
        if not line or line.startswith("Interface") or line.startswith("#") or line.startswith("!"):
            continue
            
        spl = line.split()
        # A valid terse line must contain at least the Interface, Admin, and Link status tokens
        if len(spl) < 3:
            continue
            
        raw_if_name = spl[0]
        admin_state = spl[1].lower()  # 'up' or 'down'
        link_state = spl[2].lower()   # 'up' or 'down'

        # 1. Dynamic Hardware Category Discovery via your native library tool
        # Isolates the parent interface to find its correct dictionary classification node
        parent_port = raw_if_name.split(".")[0]
        filter_type = get_juniper_int_type(parent_port)

        # 2. Isolate Parent Port and Logical Unit IDs cleanly
        if "." in raw_if_name:
            p_name, u_id = raw_if_name.split(".", 1)
        else:
            p_name, u_id = raw_if_name, "0"

        # Initialize our structured multi-layered interface directory trees safely on the fly
        if filter_type not in terse_database:
            terse_database[filter_type] = {}
        if p_name not in terse_database[filter_type]:
            terse_database[filter_type][p_name] = {'units': {}}
        if u_id not in terse_database[filter_type][p_name]['units']:
            terse_database[filter_type][p_name]['units'][u_id] = {
                'state': {}
            }

        unit_state_dict = terse_database[filter_type][p_name]['units'][u_id]['state']

        # 3. Inject Symmetrical Operational Variables Side-by-Side
        # Maps configuration choices and true physical carrier states cleanly to the data model!
        unit_state_dict['admin'] = admin_state
        unit_state_dict['protocol'] = link_state

    return terse_database


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_interface_terse(cmd_op, *args):
    """
    Bridges with your master registry execution loop pipeline.
    Returns the parsed live dictionary block context ready for merging.
    """
    terse_data = parse_juniper_interfaces_terse_single_pass(cmd_op)
    return {'op_dict': terse_data}