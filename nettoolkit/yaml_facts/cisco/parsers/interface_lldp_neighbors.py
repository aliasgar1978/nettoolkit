"""cisco show lldp neighbour command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------
def get_lldp_neighbour(command_output):
	nbr_d = {}
	parsed_data = parse_to_list_using_ntc('show lldp neighbors', command_output)
	#
	for spl in parsed_data:
		local_if = STR.if_standardize(spl[1])
		nbr_d[local_if] = {'neighbor': {}}
		nbr = nbr_d[local_if]['neighbor']
		nbr['hostname'] = spl[0]
		nbr['interface'] = STR.if_standardize(spl[3])

	return {'interfaces': {'physical': nbr_d} }

# ------------------------------------------------------------------------------
