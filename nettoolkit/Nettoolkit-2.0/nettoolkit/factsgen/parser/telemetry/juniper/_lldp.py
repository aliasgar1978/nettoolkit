"""juniper lldp neighbour command output parser """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import remove_domain, get_device_manu, standardize_if, get_juniper_int_type
# ------------------------------------------------------------------------------

def get_lldp_neighbour(cmd_op, *args, dsr=True):
    """
    Parser - show lldp neighbor command output for Juniper Junos.
    Uses native library tools for interface classification and groups topology
    attributes inside a structured 'neighbor' block to match the nested YAML schema.
    """
    nbr_d = {}
    nbr_table_start = False
    
    for i, line in enumerate(cmd_op):
        line = line.strip()
        spl = line.split()
        if not line: continue
        if not spl: 
            continue
            
        if line.startswith("Local Interface"): 
            nbr_table_start = True
            continue
        if not nbr_table_start: continue
        if line.startswith("Total "): continue        # Summary line
        if line.startswith("#"): continue            # Remarked line

        ### NBR TABLE PROCESS ###

        # Extract local and remote identities cleanly from the split array tokens
        local_if = spl[0]
        remote_hn = spl[-1].strip()
        if dsr: 
            remote_hn = remove_domain(remote_hn)

        # FIX: Rely strictly on your native library tool without manual string checks or lower-casing
        filter_type = get_juniper_int_type(local_if)

        # Isolate parent port name and logical unit context safely
        # Juniper maps active LLDP neighbors at the parent port level or implicitly to unit 0
        if "." in local_if:
            p_name, u_id = local_if.split(".", 1)
        else:
            p_name, u_id = local_if, "0"


        # Initialize the multi-layered dictionary hierarchy safely on the fly
        if filter_type not in nbr_d:
            nbr_d[filter_type] = {}
        if p_name not in nbr_d[filter_type]:
            nbr_d[filter_type][p_name] = {'units': {}}
        if u_id not in nbr_d[filter_type][p_name]['units']:
            nbr_d[filter_type][p_name]['units'][u_id] = {}
            
        unit_target = nbr_d[filter_type][p_name]['units'][u_id]

        # Process remote vendor traits dynamically using your existing logic parameters
        remote_device = get_device_manu(spl[-2].strip())
        if remote_device == 'cisco':
            remote_if = standardize_if(spl[-2].strip())
            udld_state = 'aggressive'
        else:
            remote_if = spl[-2].strip()
            udld_state = 'disable'

        # ==========================================================
        # UPDATED FOR NESTED YAML OUTPUT (Original logic preserved)
        # ==========================================================
        unit_target['neighbor'] = {
            'hostname': remote_hn,
            'interface': remote_if,
            # 'platform': remote_device
        }
        
        # # Keep global hardware tags neatly grouped if your engine checks UDLD
        # if udld_state == 'aggressive':
        #     unit_target['udld'] = udld_state

    return {'op_dict': nbr_d}