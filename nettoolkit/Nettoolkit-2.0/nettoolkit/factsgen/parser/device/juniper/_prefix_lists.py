"""juniper policy-options prefix-list output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
# ------------------------------------------------------------------------------

def parse_juniper_prefix_lists_single_pass(cmd_op):
    """
    Parses Juniper prefix lists in a single pass to maximize performance.
    Strips away redundant 'action: permit' boilerplate keys to ensure a lean YAML model.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()

    pfx_database = {
        'ipv4': {},
        'ipv6': {}
    }
    
    sequence_tracker = {}

    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if not line.startswith("set policy-options prefix-list "):
            continue
            
        spl = line.split()
        if len(spl) < 5:
            continue
            
        pfx_list_name = spl[3]
        prefix_network = spl[4].strip('"')

        # 1. Capture dynamic apply-path macros cleanly
        if "apply-path" in spl:
            macro_idx = spl.index("apply-path") + 1
            if macro_idx < len(spl):
                macro_string = " ".join(spl[macro_idx:]).strip('"')
                version_key = 'ipv4'
                pfx_database[version_key].setdefault(pfx_list_name, {})
                pfx_database[version_key][pfx_list_name]['apply_path'] = macro_string
                continue

        # 2. Isolate Core Address Version Namespace
        version_key = 'ipv6' if ':' in prefix_network else 'ipv4'

        # 3. Auto-Generate Sequential Sequence IDs
        if pfx_list_name not in sequence_tracker:
            sequence_tracker[pfx_list_name] = 10
            
        seq_num = sequence_tracker[pfx_list_name]
        
        # 4. Initialize list name block context safely
        if pfx_list_name not in pfx_database[version_key]:
            pfx_database[version_key][pfx_list_name] = {}
            
        # FIX: Store strictly the prefix string without the redundant 'action: permit' nested layer!
        pfx_database[version_key][pfx_list_name][seq_num] = prefix_network
        
        sequence_tracker[pfx_list_name] += 10

    if not pfx_database['ipv4']: del pfx_database['ipv4']
    if not pfx_database['ipv6']: del pfx_database['ipv6']
    
    return pfx_database


def get_prefix_lists(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    prefix_results = parse_juniper_prefix_lists_single_pass(cmd_op) or {}        
    return {'op_dict': prefix_results}
