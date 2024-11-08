"""cisco running-config parser for rip section output """

# ------------------------------------------------------------------------------
from .common import *
from .protocols import ProtocolsConfig, get_protocol_instance_dict
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#  RIP ATTR FUNCS
# ------------------------------------------------------------------------------

def _get_eigrp_asn(attr_dict, l, spl):
	pass



# ====================================================================================================
#  RIP Config extractor Class
# ====================================================================================================

@dataclass
class EIGRPConf(ProtocolsConfig):

	## RIP Supported AF types
	supported_af_types = ('ipv4', 'ipv6')

	attr_functions = [

	]

	def __post_init__(self):
		self.protocol_config_initialize(protocol='eigrp')
		self.eigrp_vrf_dict = self.protocol_vrf_dict
		self._iterate_vrfs()
		self.remove_empty_vrfs(self.eigrp_vrf_dict)

	def _iterate_vrfs(self):
		for instance, lines in self.vrfs.items():
			self.eigrp_vrf_dict[instance].update(self._get_attributes(lines))

# ====================================================================================================
#  RIP Config extractor function
# ====================================================================================================

def get_eigrp_running(command_output):
	EC = EIGRPConf(command_output)
	return get_protocol_instance_dict(protocol='eigrp', instances_dic=EC.eigrp_vrf_dict)

# ====================================================================================================













