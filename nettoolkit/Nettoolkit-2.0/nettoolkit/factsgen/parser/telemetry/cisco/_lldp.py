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
		except KeyError:
			remote_if = ''
		remote_hn = line[:20].strip()
		if dsr: remote_hn = remove_domain(remote_hn)
		#
		filter = get_cisco_int_type(local_if)
		if not nbr_d.get(filter):
			nbr_d[filter] = {}
		port_type_dict = nbr_d[filter]
		
		# SET / RESET
		port_type_dict[local_if] = {
			'neighbor': {
				'hostname': remote_hn.strip(),
				'interface': remote_if.strip()
			}
		}
		remote_hn, remote_if, local_if = "", "", ""

	return {'op_dict': nbr_d }
# ------------------------------------------------------------------------------
