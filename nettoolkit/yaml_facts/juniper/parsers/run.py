"""juniper protocol related common classes - parent """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

# ==========================================================================
#  STANDARD CLASS GATHERING INFO ON SHOW CONFIGURATION
#  Initialize by converting standard config to set config
# ==========================================================================
@dataclass
class Running():
	cmd_op: list[str,] = field(default_factory=[])

	def __post_init__(self):
		if self.cmd_op:	
			JS = JSet(input_list=self.cmd_op)
			JS.to_set
			self.set_cmd_op = verifid_output(JS.output)
		else:
			self.set_cmd_op = []
			raise Exception(f'Missing Configuration capture.. {self.cmd_op}, verify input')

# ==========================================================================
#  STANDARD CLASS GATHERING BGP PEER COMMANDS
# ==========================================================================
@dataclass
class PeerLines():
	bgp_peer_group_lines: list[str] = field(default_factory=[])
	peer: str = ''

	def __post_init__(self):
		self._set_peer_group_lines()
		self._set_peer_group_lines_spl()

	def __iter__(self):
		for line, spl in zip(self.peer_group_lines, self.peer_group_lines_spl):
			yield (line, spl)

	@property
	def peer_group_lines(self):
		return self._peer_group_lines

	@property
	def peer_group_lines_spl(self):
		return self._peer_group_lines_spl

	def _set_peer_group_lines(self):
		self._peer_group_lines = [line for line in self.bgp_peer_group_lines if line.find(f" protocols bgp group {self.peer} ") > 0]

	def _set_peer_group_lines_spl(self):
		self._peer_group_lines_spl = [line.strip().split() for line in self.peer_group_lines ]

# ==========================================================================
#  STANDARD CLASS GATHERING INSTANCE LINES OF A PROTOCOL
# ==========================================================================
@dataclass
class VrfLines():
	protocol: str = 'bgp'
	vrf: str = ''
	protocol_lines: list[str] = field(default_factory=[])
	protocol_spl_lines: list[str] = field(default_factory=[])

	def __post_init__(self):
		self._get_protocol_vrf_lines()
		self._get_bgp_peer_group_lines()
		self._get_bgp_other_lines()
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
		for line, spl in zip(self.protocol_lines, self.protocol_spl_lines):
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

	def _get_bgp_peer_group_lines(self):
		if self.protocol != 'bgp': return []
		self._bgp_peer_group_lines = [ line for line in self.protocol_vrf_lines if line.find(" protocols bgp group ") > 0 ]

	def _get_bgp_other_lines(self):
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

# ==========================================================================
#  STANDARD CLASS GATHERING ALL PROTOCOLS LINES
# ==========================================================================
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
		spl_lns = []
		for line in self.config_lines:
			if blank_line(line): continue
			if line.strip().startswith("#"): continue
			# line = line.strip()
			if line.find(f' protocols {self.protocol} ') == -1: continue
			spl = line.strip().split()
			proto_idx = spl.index('protocols')
			# if "prefix-list" in spl and spl.index('prefix-list') < proto_idx: continue
			lns.append(line)
			spl_lns.append(spl)
		self.protocol_lines = lns
		self.protocol_spl_lines = spl_lns

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
			self.VRFs[vrf] = VrfLines(self.protocol, vrf, self.protocol_lines,  self.protocol_spl_lines)


# ==========================================================================
#  STANDARD PROTOCOL IMPLEMENTATION
#  CLASS RETURNING AN INITIALIZED PROTOCOL OBJECT
#  INHERIT TO UTILIZE ITS FUNCTIONALITY
# ==========================================================================
@dataclass
class ProtocolObject(Running):
	cmd_op: list[str,] = field(default_factory=[])

	def initialize(self, protocol):
		super().__post_init__()
		self.jPtObj = jProtocolLines(self.set_cmd_op, protocol)

# ==========================================================================
