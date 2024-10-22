"""cisco running-config parser for bgp section output """

# ------------------------------------------------------------------------------
# from nettoolkit.facts_finder.generators.commons import *
from .common import *

# merge_dict = DIC.merge_dict
# ------------------------------------------------------------------------------

def filter_bgp_lines_cisco(command_output):
	bgp_lines, toggle = [], False
	for l in command_output:
		if blank_line(l): continue
		spl = l.strip().split()
		if l.startswith("router bgp "):
			toggle = True
		if toggle and l.startswith("!"):
			toggle = False
			break
		if not toggle: continue
		bgp_lines.append(l)
	return bgp_lines

def differenciate_af_lines(bgp_filtered_command_output):
	af_lines_dict = {}
	for l in bgp_filtered_command_output:
		if blank_line(l): continue
		spl = l.strip().split()
		if spl[0] == "!":continue
		if l.startswith("router bgp "): 
			af_type = ''
			af_name = ''
			afl = [ ]
		if l.startswith(" address-family ") and spl[-2] == "vrf": 
			afn = l.split(" address-family ")[-1].split(" vrf ")
			af_type = afn[0]
			af_name = afn[-1]
			afl = [ ]
		if l.startswith(" exit-address-family"):
			if not af_lines_dict.get(af_type):
				 af_lines_dict[af_type] = {}
			af_lines_dict[af_type][af_name] = afl
			af_type = ''
			af_name = ''
			continue
		afl.append(l)

	return af_lines_dict

# ====================================================================================================

class BGP():

	def __init__(self, af_lines):
		self.af_lines = af_lines
		self.op_dict = {}

	def bgp_read(self, func):
		toggle, af, update_dict = False, False, ""
		op_dict = {'peers': {}}
		for l in self.af_lines:
			if blank_line(l): continue
			spl = l.strip().split()
			if l.startswith("router bgp "):
				op_dict['asn'] = spl[-1]
			if l.startswith(" address-family ") and spl[-2] == "vrf": 
				op_dict['type'] = spl[1]
				continue
			if spl[0] == "router-id" or spl[1] == "router-id": 
				op_dict['router_id'] = spl[-1]
				continue
			if spl[0] != "neighbor" : continue			# continue except neighbour statements
			nbr = spl[1]
			if not op_dict['peers'].get(nbr):
				op_dict['peers'][nbr] = {}
				nbr_dict = op_dict['peers'][nbr]
			func(nbr_dict, l, spl)

		return op_dict

	def bgp_nbr_attributes(self):
		"""update the bgp neighbor attribute details
		"""    		
		func = self.get_nbr_attributes
		merge_dict(self.op_dict, self.bgp_read(func))

	@staticmethod
	def get_nbr_attributes(op_dict, line, spl):
		"""parser function to update bgp neighbor attribute details

		Args:
			port_dict (dict): dictionary with a bgp neighbour info
			line (str): string line to parse
			spl (list): splitted line to parse

		Returns:
			None: None
		"""    		
		if spl[2] == "remote-as": op_dict['bgp_peer_as'] = spl[-1]
		if spl[2] == "update-source": op_dict['update-source'] = spl[-1]
		if spl[2] == "ebgp-multihop": op_dict['ebgp-multihop'] = spl[-1]
		if spl[2] == "unsuppress-map" : op_dict["unsuppress-map"] = spl[-1]
		if spl[-2] == "peer-group": 
			op_dict["bgp_peergrp"] = spl[-1]
			op_dict["bgp_peer_ip"] = spl[1]
		if spl[-1] == "peer-group": 
			op_dict["bgp_peergrp"] = spl[1]

		if spl[2] == "password":
			op_dict["bgp_peer_password"] = decrypt_type7(spl[-1]) if spl[3] == "7" else spl[-1]

		if spl[2] == "route-map" and spl[-1] == "in": op_dict["route-map in"] = spl[-2]
		if spl[2] == "route-map" and spl[-1] == "out": op_dict["route-map out"] = spl[-2]

		if spl[2] == "local-as": op_dict['local-as'] = spl[3]
		if spl[2] == "description": op_dict['bgp_peer_description'] = " ".join(spl[3:])
		## add more as necessary ##
		return op_dict

# ====================================================================================================

def get_bgp_running(command_output):
	bgp_filtered_command_output = filter_bgp_lines_cisco(command_output)
	af_lines_dict = differenciate_af_lines(bgp_filtered_command_output)
	af_dict, bgp_dict = {}, {}
	for af_type, dic in af_lines_dict.items():
		for af_name, af_lines in dic.items():
			R  = BGP(af_lines)
			R.bgp_nbr_attributes()
			if af_type and af_name:
				if not af_dict.get(af_type):
					af_dict[af_type] = {}
				af_dict[af_type][af_name] = R.op_dict
			elif not af_type and not af_name:
				bgp_dict = R.op_dict
	merge_dict(bgp_dict, {'instances': af_dict})

	return {'protocols': {'bgp': bgp_dict} }


# ====================================================================================================
