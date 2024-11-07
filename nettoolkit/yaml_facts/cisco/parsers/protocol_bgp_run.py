"""cisco running-config parser for bgp section output """

# ------------------------------------------------------------------------------
from .common import *
from .protocols import ProtocolsConfig
# ------------------------------------------------------------------------------

@dataclass
class BGPConf(ProtocolsConfig):
	run_list: list[str] = field(default_factory=[])

	supported_af_types = ('ipv4', 'vpnv4', 'ipv6', 'vpnv6')

	def __post_init__(self):
		self.bgp_peer_dict = {}
		self.protocol_config_initialize(protocol='bgp')
		self._get_bgp_peer_informations()
		self._iterate_vrfs()
		self.remove_empty_vrfs(self.bgp_peer_dict)

	def _get_bgp_peer_informations(self):
		self._get_peer_group_names()
		self._get_peer_group_dict()

	def _get_peer_group_names(self):
		for vrf, vrf_dict in self.vrfs.items():
			vrf_peer_grps = set()
			remove_eligibles = set()
			if not vrf_dict.get('lines'): continue
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
			if not vrf_dict.get('vrf_peer_grps'): continue
			for peer_grp in vrf_dict['vrf_peer_grps']:
				other = None
				if not vrf_pg_dict[vrf].get('peers'):
					vrf_pg_dict[vrf]['peers'] = {}
				vrf_pg_dict[vrf]['peers'][peer_grp] = {}
				pg_dict = vrf_pg_dict[vrf]['peers'][peer_grp]
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
			if not pg_dict.get('peers'):
				pg_dict['peers'] = {}
			pg_dict['peers'].update( {spl[1]: {}} )

	# ---------------------------------------------------------------------- #

	def _iterate_vrfs(self):
		for vrf, vrf_dict in self.vrfs.items():
			if not vrf_dict.get('lines'): continue
			for line in vrf_dict['lines']:
				self._get_router_id(self.bgp_peer_dict[vrf], line)

	def _get_router_id(self, vrf_dict, line):
		if line.startswith("bgp router-id "):
			spl = line.strip().split()
			vrf_dict['router-id'] = spl[-1]

	# ---------------------------------------------------------------------- #

# ====================================================================================================

def get_bgp_running(command_output):
	BC = BGPConf(command_output)
	if BC.bgp_peer_dict:
		return {'protocols': {'bgp': {'instances': BC.bgp_peer_dict}} }
	else:
		return {'protocols': {}}


# ====================================================================================================













