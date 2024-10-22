"""cisco show lldp neighbour command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_lldp_neighbour(command_output):
	nbr_d, remote_hn = {}, ""
	nbr_table_start = False
	for i, line in enumerate(command_output):
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
		local_if = STR.if_standardize(line[20:31].strip().replace(" ", ""))
		try:
			remote_if = STR.if_standardize(dbl_spl[-1].strip())
		except KeyError:
			remote_if = ''
		remote_hn = line[:20].strip()
		remote_hn = remove_domain(remote_hn)

		# SET / RESET
		nbr_d[local_if] = {'neighbor':{}}
		nbr = nbr_d[local_if]['neighbor']
		nbr['hostname'] = remote_hn
		nbr['interface'] = remote_if
		remote_hn, remote_if, local_if = "", "", ""

		# -- not yet implemented , enable if error of blank key due to lldp neighbor.
		# if not (nbr_d.get('filter') and nbr_d['filter']):
		# 	nbr['filter'] = get_cisco_int_type(local_if)

	return {'interfaces': {'physical': nbr_d} }
# ------------------------------------------------------------------------------
