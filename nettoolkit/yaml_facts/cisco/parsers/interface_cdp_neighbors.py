"""cisco show cdp neighbour command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_cdp_neighbour(command_output):
	nbr_d, remote_hn, prev_line = {}, "", ""
	nbr_table_start = False
	for i, line in enumerate(command_output):

		if line.startswith("Device ID"): 
			hdr_idx = STR.header_indexes_using_splitby(line)
			nbr_table_start = True
			continue
		if not nbr_table_start: continue
		if not line.strip(): continue				# Blank lines
		if line.startswith("Total "): continue		# Summary line
		if line.startswith("!"): continue			# Remarked line

		### NBR TABLE PROCESS ###
		if len(line.strip().split()) == 1:  
			remote_hn = line[hdr_idx['Device ID'][0]:]
			prev_line = True
			continue
		else:
			if not prev_line: remote_hn = line[hdr_idx['Device ID'][0]:hdr_idx['Device ID'][-1]]
			local_if = line[hdr_idx['Local Intrfce'][0]:hdr_idx['Local Intrfce'][-1]].strip()
			try:
				local_if = STR.if_standardize(local_if)
			except:
				pass
			remote_if = line[hdr_idx['Port ID'][0]:hdr_idx['Port ID'][-1]].strip()
			try:
				remote_if = STR.if_standardize(remote_if)
			except:
				pass
			remote_plateform = line[hdr_idx['Platform'][0]:hdr_idx['Platform'][-1]]
			prev_line = False

		if remote_hn: remote_hn = remove_domain(remote_hn)

		# SET / RESET
		nbr_d[local_if] = {'neighbor': {}}
		nbr = nbr_d[local_if]['neighbor']
		nbr['hostname'] = remote_hn.strip()
		nbr['interface'] = remote_if.strip()
		nbr['plateform'] = remote_plateform.strip()
		remote_hn, remote_if, remote_plateform = "", "", ""

	return {'interfaces': {'physical': nbr_d} }
# ------------------------------------------------------------------------------
