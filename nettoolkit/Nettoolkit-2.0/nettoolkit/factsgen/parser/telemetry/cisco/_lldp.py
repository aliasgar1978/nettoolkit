"""cisco show lldp neighbour command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import if_standardize, remove_domain, get_cisco_int_type
# ------------------------------------------------------------------------------

def get_lldp_neighbour(cmd_op, *args, dsr=True):
    """parser - show lldp neigh command output

    Parsed Fields:
        * port/interface
        * neighbor interface
        * neighbor hostname

    Args:
        cmd_op (list, str): command output in list/multiline string.
        dsr (bool, optional): DOMAIN SUFFIX REMOVAL. Defaults to True.

    Returns:
        dict: output dictionary with parsed fields
    """
    nbr_d, remote_hn = {}, ""
    nbr_table_start = False
    for i, line in enumerate(cmd_op):
        line = line.strip()
        dbl_spl = line.split("  ")
        if line.startswith("Device ID"): 
            nbr_table_start = True
            continue
        if not nbr_table_start: continue
        if not line.strip(): continue				# Blank lines
        if line.startswith("Total "): break  		# Summary line
        if line.startswith("!"): continue			# Remarked line

        ### NBR TABLE PROCESS ###

        # // LOCAL/NBR INTERFACE, NBR PLATFORM //
        # // NBR HOSTNAME //
        local_if = if_standardize(line[20:31].strip().replace(" ", ""))
        try:
            remote_if = if_standardize(dbl_spl[-1].strip())
        except (IndexError, KeyError):
            remote_if = ''
        remote_hn = line[:20].strip()
        if dsr: remote_hn = remove_domain(remote_hn)
        #
        filter = get_cisco_int_type(local_if)
        if not nbr_d.get(filter):
            nbr_d[filter] = {}
        port_type_dict = nbr_d[filter]
        
        # SET / RESET
        if not port_type_dict.get(local_if):
            port_type_dict[local_if] = {}
        port_type_dict[local_if] = {
        	'neighbor': {
        		'hostname': remote_hn.strip(),
        		'interface': remote_if.strip()
        	}
        }

        ## diabled - multiple neighbors on sinlge interface ##
        add_neighbor_info(
            port_type_dict[local_if], 
			hostname=remote_hn.strip(), 
            interface=remote_if.strip(), 
        )

        remote_hn, remote_if, local_if = "", "", ""

    return {'op_dict': nbr_d }
# ------------------------------------------------------------------------------

# def add_neighbor_info(unit_target, remote_hn, remote_if):
#     if not unit_target.get('neighbors'):
#         unit_target['neighbors'] = {'hostname': remote_hn, 'interface': remote_if}
#     elif isinstance(unit_target['neighbors'], list):
#         match = False
#         for item in unit_target['neighbors']:
#             if item.get('hostname') == remote_hn and item.get('interface') == remote_if:
#                 match = True
#         if not match:
#             unit_target['neighbors'].append({'hostname': remote_hn, 'interface': remote_if})
#     elif isinstance(unit_target['neighbors'], dict) and (unit_target['neighbors'].get('hostname') != remote_hn or unit_target['neighbors'].get('interface') != remote_if):
#         old_entry = unit_target['neighbors']
#         unit_target['neighbors'] = [old_entry, {'hostname': remote_hn, 'interface': remote_if}]

def add_neighbor_info(unit_target, **kwards):
    if not unit_target.get('neighbors'):
        unit_target['neighbors'] = []
    unit_target['neighbors'].append(kwards)

