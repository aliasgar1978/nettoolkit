"""juniper lldp neighbour command output parser """

# ------------------------------------------------------------------------------
from nettoolkit.facts_finder.generators.commons import *
from .common import *

# ------------------------------------------------------------------------------

def get_lldp_neighbour(cmd_op):
	nbr_d, remote_hn = {}, ""
	nbr_table_start = False
	for i, line in enumerate(cmd_op):
		line = line.strip()
		spl = line.split()
		if line.startswith("Local Interface"): 
			nbr_table_start = True
			continue
		if not nbr_table_start: continue
		if not line.strip(): continue				# Blank lines
		if line.startswith("Total "): continue		# Summary line
		if line.startswith("#"): continue			# Remarked line

		### NBR TABLE PROCESS ###

		# // LOCAL/NBR INTERFACE, NBR HOSTNAME //
		local_if = spl[0]
		remote_hn = spl[-1].strip()
		remote_hn = remove_domain(remote_hn)


		# SET / RESET
		port_dict = get_int_port_dict(op_dict=nbr_d, port=local_if)
		port_dict['neighbor'] = {}
		nbr = port_dict['neighbor']
		# nbr_d[local_if] = {}
		# nbr = nbr_d[local_if]
		#
		remote_device = get_device_manu(spl[-2].strip())
		if remote_device == 'cisco':
			remote_if = standardize_if(spl[-2].strip())
			nbr['interface'] = remote_if
			port_dict['int_udld'] = 'aggressive'
		else:
			remote_if = spl[-2].strip()
			nbr['interface'] = remote_if
			port_dict['int_udld'] = 'disable'
		#
		nbr['hostname'] = remote_hn
		local_if, remote_hn, remote_if = "", "", ""
	return {'interfaces': nbr_d}
# ------------------------------------------------------------------------------
