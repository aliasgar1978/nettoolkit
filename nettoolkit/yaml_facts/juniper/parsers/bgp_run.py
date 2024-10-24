"""juniper bgp protocol routing instances parsing from set config  """

# ------------------------------------------------------------------------------
from .common import *
from .run import Running, jProtocolLines, VrfLines, PeerLines
# ------------------------------------------------------------------------------


class BGPPeers(Running):

	def __call__(self):
		self.jPtObj = jProtocolLines(self.set_cmd_op, 'bgp')
		self.instance_dict = self._iterate_over_vrfs()
		self.instance_vrf_dict =  self._iterate_over_vrfs_for_instance()

	def _iterate_over_vrfs(self):
		instance_dict = {}
		for vrf in self.jPtObj.VRFs.keys():
			VRF = self.jPtObj.VRFs[vrf]
			vd = self._iterate_over_vrf_peers(peers=VRF.PEERs, vrf=vrf)
			if vd: instance_dict[vrf] = vd
		return instance_dict

	def _iterate_over_vrf_peers(self, peers, vrf):
		peers_dict = {}
		for peer in peers.keys():
			psd = self._iterate_peer_lines(peers, peer)
			if psd: peers_dict[peer] = psd
		return peers_dict

	def _iterate_peer_lines(self, peers, peer):
		peer_dict = {}
		for line in peers[peer]:
			spl = line.split()
			proto_idx = spl.index('protocols')
			spl = spl[proto_idx:]
			self.get_bgp_grp_info(peer_dict, line, spl)
		return peer_dict


	def get_bgp_grp_info(self, peer_dict, line, spl):

		## --- peer/neighbors ---
		if 'neighbor' in spl:
			if not peer_dict.get('peers'):
				peer_dict['peers'] = {}
			peer_dict['peers'][spl[5]] = {}


		## --- description and vrf ---
		if len(spl)>4 and spl[4] == 'description':
			desc = " ".join(spl[5:]).strip()
			if desc[0] == '"': desc = desc[1:]
			if desc[-1] == '"': desc = desc[:-1]
			peer_dict['description'] = desc
		elif len(spl)>6 and spl[6] == 'description':
			desc = " ".join(spl[7:]).strip()
			if desc[0] == '"': desc = desc[1:]
			if desc[-1] == '"': desc = desc[:-1]
			peer_dict['peers'][spl[5]]['description'] = desc


		## --- auth key - peer group ---
		if len(spl)>4 and spl[4] == 'authentication-key':
			pw = " ".join(spl[5:]).strip().split("##")[0].strip()
			if pw[0] == '"': pw = pw[1:]
			if pw[-1] == '"': pw = pw[:-1]
			try:
				pw = juniper_decrypt(pw)
			except: pass
			peer_dict['password'] = pw
		## --- auth key - peer ---
		elif len(spl)>6 and spl[6] == 'authentication-key':
			pw = " ".join(spl[7:]).strip().split("##")[0].strip()
			if pw[0] == '"': pw = pw[1:]
			if pw[-1] == '"': pw = pw[:-1]
			try:
				pw = juniper_decrypt(pw)
			except: pass
			peer_dict['peers'][spl[5]]['password'] = pw

		## --- peer-as - peer group ---
		if len(spl)>4 and spl[4] == 'peer-as':
			peer_dict['peer_as'] = spl[5]
		## --- peer-as - peer ---
		if len(spl)>6 and spl[6] == 'peer-as':
			peer_dict['peers'][spl[5]]['peer_as'] = spl[7]

		## --- local-as - peer group ---
		if len(spl)>4 and spl[4] == 'local-as':
			peer_dict['local_as'] = spl[5]
		## --- local-as - peer ---
		if len(spl)>6 and spl[6] == 'local-as':
			peer_dict['peers'][spl[5]]['local_as'] = spl[7]

		## --- ebgp multihops ---
		if len(spl)>5 and spl[4] == 'multihop':
			peer_dict['ebgp_multihops'] = spl[-1]

		return peer_dict

	# ============================================================================ 

	def _iterate_over_vrfs_for_instance(self):
		instance_dict = {}
		for vrf in self.jPtObj.VRFs.keys():
			VRF = self.jPtObj.VRFs[vrf]
			vd = self.vrf_instance_read(vrf, VRF)
			if vd: instance_dict[vrf] = vd
		return instance_dict

	def vrf_instance_read(self, vrf, VRF):
		vrf_dict = {}
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if not l.startswith(f"set routing-instances {vrf} "): continue
			if l in VRF.bgp_peer_group_lines: continue
			if l in VRF.bgp_other_lines: continue
			spl = l.split()
			self.add_vrf_route_target(vrf_dict, l, spl)
			self.add_vrf_description(vrf_dict, l, spl)
			self.add_vrf_rd(vrf_dict, l, spl)
		return vrf_dict

	def add_vrf_route_target(self, vrf_dict, l, spl):
		if spl[3] == 'route-distinguisher':
			vrf_dict['default_rd'] = spl[-1].strip().split(":")[-1]

	def add_vrf_description(self, vrf_dict, l, spl):
		if spl[3] == 'description':
			desc = " ".join(spl[4:]).strip()
			if desc[0] == '"': desc = desc[1:]
			if desc[-1] == '"': desc = desc[:-1]
			vrf_dict['description'] = desc

	def add_vrf_rd(self, vrf_dict, l, spl):
		if spl[3] == 'vrf-target':
			if not vrf_dict.get(f"{spl[4]} target"):
				vrf_dict[f"{spl[4]} target"] = set()
			rd = ":".join(spl[-1].split(":")[-2:])
			vrf_dict[f"{spl[4]} target"].add( rd )


# =====================================================================================

def get_bgp_running(cmd_op):
	"""defines set of methods executions. to get various instance parameters.
	uses RunningIntanceBGP in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = BGPPeers(cmd_op)
	R()

	return {
	  'protocols': {'bgp': {'instances': R.instance_dict}},
	  'vrf': R.instance_vrf_dict,

	}

# =====================================================================================

