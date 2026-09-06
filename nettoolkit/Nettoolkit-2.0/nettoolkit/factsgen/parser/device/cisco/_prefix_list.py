
# # ------------------------------------------------------------------------------
"""cisco running-config - prefix list output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
# ------------------------------------------------------------------------------

def parse_prefix_lists_single_pass(cmd_op):
    """
    Parses Cisco prefix lists (IPv4 & IPv6) in a single pass to maximize performance.
    Groups statement sequences contextually to match our unified YAML layout.
    """
    pfx_database = {
        'ipv4': {},
        'ipv6': {}
    }
    
    for line in cmd_op:
        line = line.strip()
        if not line or line.startswith("!"): 
            continue
        if not line.startswith("ip prefix-list ") and not line.startswith("ipv6 prefix-list "): 
            continue
            
        spl = line.split()
        if not spl: 
            continue
            
        # 1. Isolate Core Address Version Namespace
        version_key = 'ipv4' if spl[0] == 'ip' else 'ipv6'
        pfx_list_name = spl[2]
        
        # 2. Extract or Default Sequence Identifiers safely
        seq_num = "10"  # Default fallback if sequence keyword is missing
        if "seq" in spl:
            try:
                seq_num = spl[spl.index("seq") + 1]
            except (ValueError, IndexError):
                pass
                
        # 3. Dynamic Action and Prefix Isolation
        # Scans for permit/deny anchors to locate fields regardless of token shifts
        action = "permit" if "permit" in spl else "deny"
        try:
            action_idx = spl.index(action)
            prefix_network = spl[action_idx + 1]
        except (ValueError, IndexError):
            continue  # Guard against malformed strings
            
        # 4. Dynamic Lookup Map for Variable Range Modifiers (ge / le)
        # Eliminates the static spl[7]/spl[8] index constraints completely!
        ge_value = None
        le_value = None
        
        if "ge" in spl:
            try:
                ge_value = int(spl[spl.index("ge") + 1])
            except (ValueError, IndexError):
                pass
        if "le" in spl:
            try:
                le_value = int(spl[spl.index("le") + 1])
            except (ValueError, IndexError):
                pass

        # 5. Build the Unified Nested Sequence Entry Object
        sequence_entry = {
            'action': action,
            'prefix': prefix_network,
            'ge': ge_value,
            'le': le_value
        }
        
        # Cleanup unpopulated optional indicators to ensure pristine YAML formatting
        if sequence_entry['ge'] is None: del sequence_entry['ge']
        if sequence_entry['le'] is None: del sequence_entry['le']

        # 6. Allocate context into the target database layout structure
        if pfx_list_name not in pfx_database[version_key]:
            pfx_database[version_key][pfx_list_name] = {}
            
        # Nest sequence lists directly inside the prefix list name context area
        pfx_database[version_key][pfx_list_name][int(seq_num)] = sequence_entry

    # Post-parsing cleanup: Remove unpopulated tracking nodes
    if not pfx_database['ipv4']: del pfx_database['ipv4']
    if not pfx_database['ipv6']: del pfx_database['ipv6']
    
    return pfx_database


def get_prefix_lists(cmd_op, *args):
    # Bridges with your main centralized orchestration execution registers loop pipeline smoothly
    prefix_results = parse_prefix_lists_single_pass(cmd_op)
    
    if not prefix_results:
        prefix_results['dummy_pl'] = ""
        
    return {'op_dict': prefix_results}