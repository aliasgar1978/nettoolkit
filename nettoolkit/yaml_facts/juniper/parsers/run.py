"""juniper set config initiator - parent """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

class Running():
	"""parent object for config parser

	Args:
		cmd_op (list, str): config output, either list of multiline string
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output
		"""    		    		
		self.cmd_op = cmd_op
		if self.cmd_op:	
			JS = JSet(input_list=cmd_op)
			JS.to_set
			self.set_cmd_op = verifid_output(JS.output)
		else:
			self.set_cmd_op = []
			raise Exception(f'Missing Configuration capture.. {cmd_op}, verify input')

# ------------------------------------------------------------------------------



# ==========================================================================
#  PROTOCOL / VRF SET LINES FILTER CLASS
# ==========================================================================

@dataclass
class PeerLines():
	bgp_peer_group_lines: list[str] = field(default_factory=[])
	peer: str = ''

	def __post_init__(self):
		self._set_peer_group_lines()

	def __iter__(self):
		for x in self.peer_group_lines:
			yield x

	@property
	def peer_group_lines(self):
		return self._peer_group_lines

	def _set_peer_group_lines(self):
		self._peer_group_lines = [line for line in self.bgp_peer_group_lines if line.find(f" protocols bgp group {self.peer} ") > 0]

@dataclass
class VrfLines():
	protocol: str = 'bgp'
	protocol_lines: list[str] = field(default_factory=[])
	vrf: str = ''

	def __post_init__(self):
		self._get_protocol_vrf_lines()
		self._bgp_peer_group_lines()
		self._bgp_other_lines()
		self._get_peer_groupnames()
		self()

	def __call__(self):
		if self.protocol == 'bgp':
			self._iterate_peer_groups()

	def __iter__(self):
		lines = self.bgp_peer_group_lines if self.protocol == 'bgp' else self.protocol_vrf_lines
		for x in lines:
			yield x

	def _get_protocol_vrf_lines(self):
		lns = []
		for line in self.protocol_lines:
			spl = line.split()
			if spl[1] == 'protocols':
				if self.vrf: continue
				lns.append(line)
				continue
			if spl[2] != self.vrf: continue
			lns.append(line)
		self._protocol_vrf_lines = lns

	@property
	def protocol_vrf_lines(self):
		return self._protocol_vrf_lines

	@property
	def bgp_peer_group_lines(self):
		return self._bgp_peer_group_lines

	@property
	def bgp_other_lines(self):
		return self._bgp_other_lines

	@property
	def peer_group_names(self):
		return self._peer_group_names

	def _bgp_peer_group_lines(self):
		if self.protocol != 'bgp': return []
		self._bgp_peer_group_lines = [ line for line in self.protocol_vrf_lines if line.find(" protocols bgp group ") > 0 ]

	def _bgp_other_lines(self):
		if self.protocol != 'bgp': return []
		self._bgp_other_lines = [ line for line in self.protocol_vrf_lines if line.find(" protocols bgp group ") == -1 ]

	def _get_peer_groupnames(self):
		self._peer_group_names = set()
		for line in self.bgp_peer_group_lines:
			self._peer_group_names.add( line.split(" protocols bgp group ")[-1].split()[0] )

	def _iterate_peer_groups(self):
		self.PEERs = {}
		for peer in self.peer_group_names:
			self.PEERs[peer] = PeerLines(self.bgp_peer_group_lines, peer)




@dataclass
class jProtocolLines():
	config_lines: list[str,] = field(default_factory=[])
	protocol: str = 'bgp'

	def __post_init__(self):
		self._get_protocol_set_commands()
		self._get_vrfs()
		self._iterate_vrfs()

	def __iter__(self):
		for x in self.protocol_lines:
			yield x

	def _get_protocol_set_commands(self):
		lns = []
		for line in self.config_lines:
			if blank_line(line): continue
			if line.strip().startswith("#"): continue
			# line = line.strip()
			if line.find(f' protocols {self.protocol} ') == -1: continue
			spl = line.split()
			proto_idx = spl.index('protocols')
			# if "prefix-list" in spl and spl.index('prefix-list') < proto_idx: continue
			lns.append(line)
		self.protocol_lines = lns

	def _get_vrfs(self):
		vrfs = {None,}
		for line in self.config_lines:
			spl = line.split()
			if spl[1] != 'routing-instances': continue
			vrfs.add(spl[2])
		self.vrfs = vrfs

	def _iterate_vrfs(self):
		self.VRFs = {}
		for vrf in self.vrfs:
			self.VRFs[vrf] = VrfLines(self.protocol, self.protocol_lines, vrf)

