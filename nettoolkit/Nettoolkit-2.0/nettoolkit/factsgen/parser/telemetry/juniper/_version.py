"""juniper show version command output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
# ------------------------------------------------------------------------------

def get_version(cmd_op, *args):
    """
    Parser - show version command output for Juniper Junos.
    Nests software and hardware variables to match the exact schema 
    pattern we designed for Cisco systems.
    """
    op_dict = {}
    version, model = "", ""
    
    for l in cmd_op:
        if blank_line(l): continue
        if l.strip().startswith("#"): continue
        
        # FIX: Split context by the separator string itself instead of index slicing from the back.
        # This completely guards your version numbers from getting truncated if trailing words exist!
        if l.startswith("Junos: "):  
            version = l.split("Junos:")[-1].strip()
        if l.startswith("Model: "): 
            model = l.split("Model:")[-1].strip().upper()

    # ==========================================================
    # UPDATED FOR NESTED YAML OUTPUT (Matches Cisco Schema)
    # ==========================================================
    op_dict['software'] = {
        'version': version,
    }
    
    op_dict['hardware'] = {
        'model': model,
    }
    
    return {'op_dict': op_dict}
# ------------------------------------------------------------------------------