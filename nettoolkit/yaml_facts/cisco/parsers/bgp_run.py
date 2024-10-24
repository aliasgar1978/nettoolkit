"""cisco running-config parser for bgp section output """

# ------------------------------------------------------------------------------
from dataclasses import dataclass, field
from .common import *
# ------------------------------------------------------------------------------




@dataclass
class BGPConf():
	run_list: list[str] = field(default_factory=[])

	def __post_init__(self):
		self.bgp_list = self._iterate_running()
		self.vrfs = self._get_instances()
		self._get_instances_lists_dict()
		self._get_peer_group_names()
		self._get_peer_group_dict()

	def _iterate_running(self):
		start = False
		lst = []
		for line in self.run_list:
			start = start or line.startswith("router bgp ")
			if start and line[0] == "!": break
			if not start: continue
			lst.append(line)
		return lst

	def _get_instances(self):
		vrfs = { }
		for line in self.bgp_list:
			if not line[1:].startswith("address-family"): continue
			spl = line.strip().split()
			if not 'vrf' in spl: continue
			if not vrfs.get(spl[-1]):
				vrfs[spl[-1]] = {}
			if spl[1] in ('ipv4', 'vpnv4', 'ipv6', 'vpnv6'):
				if not vrfs[spl[-1]].get('type'):
					vrfs[spl[-1]]['type'] = set()
				vrfs[spl[-1]]['type'].add(spl[1])
		vrfs[None] = {}
		return vrfs

	def _get_instances_lists_dict(self):
		for vrf, vrf_dict in self.vrfs.items():
			if vrf == None: continue
			start = False
			lst = []
			for line in self.bgp_list:
				if line.strip().startswith("address-family") and line.strip().endswith(f"vrf {vrf}"):
					start = True
					spl = line.strip().split()
					vrf_type = ''
					if spl[1] in ('ipv4', 'vpnv4', 'ipv6', 'vpnv6'): vrf_type = spl[1]
					if not vrf_dict.get('lines'):
						vrf_dict['lines'] = []
				if line.strip() == 'exit-address-family': start = False
				if not start: continue
				vrf_dict['lines'].append(line.strip())
		for vrf, vrf_dict in self.vrfs.items():
			if vrf : continue
			lst = []
			for line in self.bgp_list:
				if line.strip().startswith("address-family"):
					break
				if not vrf_dict.get('lines'):
					vrf_dict['lines'] = []
				vrf_dict['lines'].append(line.strip())

	def _get_peer_group_names(self):
		for vrf, vrf_dict in self.vrfs.items():
			vrf_peer_grps = set()
			remove_eligibles = set()
			for line in vrf_dict['lines']:
				if not line.startswith("neighbor"): continue
				spl = line.split()
				vrf_peer_grps.add(spl[1])
				if len(spl) > 3 and spl[2] == 'peer-group' and spl[3] in vrf_peer_grps:
					remove_eligibles.add(spl[1])
			vrf_dict['vrf_peer_grps'] = vrf_peer_grps - remove_eligibles

	def _get_peer_group_dict(self):
		vrf_pg_dict = {}
		for vrf, vrf_dict in self.vrfs.items():
			vrf_pg_dict[vrf] = {}			
			for peer_grp in vrf_dict['vrf_peer_grps']:
				other = None
				vrf_pg_dict[vrf][peer_grp] = {}
				pg_dict = vrf_pg_dict[vrf][peer_grp]
				for line in vrf_dict['lines']:
					if not line.startswith("neighbor"): continue
					spl = line.split()
					valid_line = spl[1] == peer_grp or other in spl
					if not valid_line:
						if peer_grp in spl and spl[-1] == peer_grp:
							other = spl[1]
							valid_line = True
						else:
							other = None
							valid_line = False
					if not valid_line: continue
					self._get_local_as(peer_grp, pg_dict, line, spl)
					self._get_remote_as(peer_grp, pg_dict, line, spl)
					self._get_description(peer_grp, pg_dict, line, spl)
					self._get_password(peer_grp, pg_dict, line, spl)
					self._get_update_source(peer_grp, pg_dict, line, spl)
					self._get_peers(peer_grp, pg_dict, line, spl)
		self.bgp_peer_dict = vrf_pg_dict


	def _get_local_as(self, peer_grp, pg_dict, line, spl):
		if spl[2] == 'description':
			if spl[1] == peer_grp:
				pg_dict['description'] = " ".join(spl[3:])
			else:
				pg_dict['peers'][spl[1]]['description'] = " ".join(spl[3:])

	def _get_remote_as(self, peer_grp, pg_dict, line, spl):
		if spl[2] == 'remote-as': 
			pg_dict['peer_as'] = spl[3]

	def _get_description(self, peer_grp, pg_dict, line, spl):
		if spl[2] == 'local-as': 
			pg_dict['local_as'] = spl[3]

	def _get_password(self, peer_grp, pg_dict, line, spl):
		if spl[2] == 'password': 
			pg_dict['password'] = decrypt_type7(spl[-1]) if spl[3] == "7" else spl[-1]

	def _get_update_source(self, peer_grp, pg_dict, line, spl):
		if spl[2] == 'update-source': 
			pg_dict['update_source'] = spl[3]

	def _get_peers(self, peer_grp, pg_dict, line, spl):
		if len(spl)<4: return
		if spl[2] == 'peer-group' and spl[3] == peer_grp: 
			pg_dict['peers'] = {spl[1]: {}}


def get_bgp_running(command_output):
	BC = BGPConf(command_output)

	return {'protocols': {'bgp': {'instances': BC.bgp_peer_dict}} }







# def filter_bgp_lines_cisco(command_output):
# 	bgp_lines, toggle = [], False
# 	for l in command_output:
# 		if blank_line(l): continue
# 		spl = l.strip().split()
# 		if l.startswith("router bgp "):
# 			toggle = True
# 		if toggle and l.startswith("!"):
# 			toggle = False
# 			break
# 		if not toggle: continue
# 		bgp_lines.append(l)
# 	return bgp_lines

# def differenciate_af_lines(bgp_filtered_command_output):
# 	af_lines_dict = {}
# 	for l in bgp_filtered_command_output:
# 		if blank_line(l): continue
# 		spl = l.strip().split()
# 		if spl[0] == "!":continue
# 		if l.startswith("router bgp "): 
# 			af_type = ''
# 			af_name = ''
# 			afl = [ ]
# 		if l.startswith(" address-family ") and spl[-2] == "vrf": 
# 			afn = l.split(" address-family ")[-1].split(" vrf ")
# 			af_type = afn[0]
# 			af_name = afn[-1]
# 			afl = [ ]
# 		if l.startswith(" exit-address-family"):
# 			if not af_lines_dict.get(af_type):
# 				 af_lines_dict[af_type] = {}
# 			af_lines_dict[af_type][af_name] = afl
# 			af_type = ''
# 			af_name = ''
# 			continue
# 		afl.append(l)

# 	return af_lines_dict

# # ====================================================================================================

# class BGP():

# 	def __init__(self, af_lines):
# 		self.af_lines = af_lines
# 		self.op_dict = {}

# 	def bgp_read(self, func):
# 		toggle, af, update_dict = False, False, ""
# 		op_dict = {'peers': {}}
# 		for l in self.af_lines:
# 			if blank_line(l): continue
# 			spl = l.strip().split()
# 			if l.startswith("router bgp "):
# 				op_dict['asn'] = spl[-1]
# 			if l.startswith(" address-family ") and spl[-2] == "vrf": 
# 				op_dict['type'] = spl[1]
# 				continue
# 			if spl[0] == "router-id" or spl[1] == "router-id": 
# 				op_dict['router_id'] = spl[-1]
# 				continue
# 			if spl[0] != "neighbor" : continue			# continue except neighbour statements
# 			nbr = spl[1]
# 			if not op_dict['peers'].get(nbr):
# 				op_dict['peers'][nbr] = {}
# 				nbr_dict = op_dict['peers'][nbr]
# 			func(nbr_dict, l, spl)

# 		return op_dict

# 	def bgp_nbr_attributes(self):
# 		"""update the bgp neighbor attribute details
# 		"""    		
# 		func = self.get_nbr_attributes
# 		merge_dict(self.op_dict, self.bgp_read(func))

# 	@staticmethod
# 	def get_nbr_attributes(op_dict, line, spl):
# 		"""parser function to update bgp neighbor attribute details

# 		Args:
# 			port_dict (dict): dictionary with a bgp neighbour info
# 			line (str): string line to parse
# 			spl (list): splitted line to parse

# 		Returns:
# 			None: None
# 		"""    		
# 		if spl[2] == "remote-as": op_dict['bgp_peer_as'] = spl[-1]
# 		if spl[2] == "update-source": op_dict['update-source'] = spl[-1]
# 		if spl[2] == "ebgp-multihop": op_dict['ebgp-multihop'] = spl[-1]
# 		if spl[2] == "unsuppress-map" : op_dict["unsuppress-map"] = spl[-1]
# 		if spl[-2] == "peer-group": 
# 			op_dict["bgp_peergrp"] = spl[-1]
# 			op_dict["bgp_peer_ip"] = spl[1]
# 		if spl[-1] == "peer-group": 
# 			op_dict["bgp_peergrp"] = spl[1]

# 		if spl[2] == "password":
# 			op_dict["bgp_peer_password"] = decrypt_type7(spl[-1]) if spl[3] == "7" else spl[-1]

# 		if spl[2] == "route-map" and spl[-1] == "in": op_dict["route-map in"] = spl[-2]
# 		if spl[2] == "route-map" and spl[-1] == "out": op_dict["route-map out"] = spl[-2]

# 		if spl[2] == "local-as": op_dict['local-as'] = spl[3]
# 		if spl[2] == "description": op_dict['bgp_peer_description'] = " ".join(spl[3:])
# 		## add more as necessary ##
# 		return op_dict

# # ====================================================================================================

# def get_bgp_running(command_output):
# 	bgp_filtered_command_output = filter_bgp_lines_cisco(command_output)
# 	af_lines_dict = differenciate_af_lines(bgp_filtered_command_output)
# 	af_dict, bgp_dict = {}, {}
# 	for af_type, dic in af_lines_dict.items():
# 		for af_name, af_lines in dic.items():
# 			R  = BGP(af_lines)
# 			R.bgp_nbr_attributes()
# 			if af_type and af_name:
# 				if not af_dict.get(af_type):
# 					af_dict[af_type] = {}
# 				af_dict[af_type][af_name] = R.op_dict
# 			elif not af_type and not af_name:
# 				bgp_dict = R.op_dict
# 	merge_dict(bgp_dict, {'instances': af_dict})

# 	return {'protocols': {'bgp': bgp_dict} }


# # ====================================================================================================













