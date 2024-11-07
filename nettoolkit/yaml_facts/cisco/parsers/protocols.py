"""cisco running-config parser for protocol xxx section output """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

@dataclass
class ProtocolsConfig():
	run_list: list[str] = field(default_factory=[])

	def protocol_config_initialize(self, protocol):
		self.routing_protocol_config_list = self._get_router_configurations(protocol)
		self.vrfs = self._get_instances()
		self._add_instances_lines_to_instance_dict()

	def _get_router_configurations(self, protocol):
		start = False
		lst = []
		for line in self.run_list:
			if not line.strip() : continue
			start = start or line.startswith(f"router {protocol}")
			if start and line[0] == "!": break
			if not start: continue
			lst.append(line)
		return lst

	def _get_instances(self):
		vrfs = { }
		for line in self.routing_protocol_config_list:
			if not line[1:].startswith("address-family"): continue
			spl = line.strip().split()
			if not 'vrf' in spl: continue
			if not vrfs.get(spl[-1]):
				vrfs[spl[-1]] = {}
			if spl[1] in self.supported_af_types:
				if not vrfs[spl[-1]].get('af_type'):
					vrfs[spl[-1]]['af_type'] = set()
				vrfs[spl[-1]]['af_type'].add(spl[1])
		vrfs[None] = {}
		return vrfs

	def _add_instances_lines_to_instance_dict(self):
		## config list for all appeared vrfs
		for vrf, vrf_dict in self.vrfs.items():
			if vrf == None: continue
			start = False
			lst = []
			for line in self.routing_protocol_config_list:
				if line.strip().startswith("address-family") and line.strip().endswith(f"vrf {vrf}"):
					start = True
					spl = line.strip().split()
					vrf_type = ''
					if spl[1] in self.supported_af_types: 
						vrf_type = spl[1]
					if not vrf_dict.get('lines'):
						vrf_dict['lines'] = []
				if line.strip() == 'exit-address-family': start = False
				if not start: continue
				vrf_dict['lines'].append(line.strip())

		## config list for global instance
		for vrf, vrf_dict in self.vrfs.items():
			if vrf : continue
			lst = []
			start = True
			for line in self.routing_protocol_config_list:
				if line.strip().startswith("!"): 
					continue
				if line.strip().startswith("address-family"):
					start = False
					continue
				if line.strip() == 'exit-address-family': 
					start = True
					continue
				if not start: 
					continue
				if not vrf_dict.get('lines'):
					vrf_dict['lines'] = []
				vrf_dict['lines'].append(line.strip())

	def remove_empty_vrfs(self, vrf_dict):
		for vrf in list(vrf_dict.keys()):
			if not vrf_dict[vrf]:
				del(vrf_dict[vrf])
