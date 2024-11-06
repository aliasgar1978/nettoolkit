"""cisco show running-config parser for ospf section output """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

class OSPF():
	"""parent object for OSPF running config parser

	Args:
		cmd_op (list, str): running config output, either list of multiline string
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the running config output
		"""    		    		
		self.cmd_op = cmd_op
		self.op_dict = {}

	def ospf_read(self, func):
		"""directive function to get the various ospf level output

		Args:
			func (method): method to be executed on ospf config line

		Returns:
			dict: parsed output dictionary
		"""    		
		toggle, af, update_dict = False, False, ""
		op_dicts = {'instances':{}}
		op_dict = op_dicts['instances']
		for l in self.cmd_op:
			spl = l.strip().split()
			if l.startswith("router ospf "):
				p = spl[2]
				vrf = spl[4] if len(spl) > 3 and spl[3] == 'vrf' else ""
				if not op_dict.get(p): op_dict[p] = {}
				vrf_op_dict = op_dict[p]
				vrf_op_dict['vrf']= vrf
				toggle = True
				continue
			if l.startswith("!"): toggle = False
			if toggle:
				func(vrf_op_dict, l, spl)

		return op_dicts



	def router_id(self):
		"""update the router-id details
		"""    		
		merge_dict(self.op_dict, self.ospf_read(self.get_router_id))

	@staticmethod
	def get_router_id(vrf_op_dict, l, spl):
		"""parser function to get router-id details

		Args:
			vrf_op_dict (dict): dictionary with a vrf info
			l (str): string line to parse
			spl (list): splitted line to parse

		Returns:
			None: None
		"""

		if len(spl)>0 and spl[0] == 'router-id':
			vrf_op_dict['router_id'] = spl[-1]


	def active_interfaces(self):
		"""update the active interfaces
		"""    		
		merge_dict(self.op_dict, self.ospf_read(self.get_active_interfaces))

	@staticmethod
	def get_active_interfaces(vrf_op_dict, l, spl):
		"""parser function to get active interfaces

		Args:
			vrf_op_dict (dict): dictionary with a vrf info
			l (str): string line to parse
			spl (list): splitted line to parse

		Returns:
			None: None
		"""
		if len(spl)>1 and spl[0] == 'no' and spl[1] == 'passive-interface':
			append_attribute(vrf_op_dict, 'active_interfaces', spl[-1])			


	def networks(self):
		"""update the networks
		"""    		
		merge_dict(self.op_dict, self.ospf_read(self.get_networks))

	@staticmethod
	def get_networks(vrf_op_dict, l, spl):
		"""parser function to get networks

		Args:
			vrf_op_dict (dict): dictionary with a vrf info
			l (str): string line to parse
			spl (list): splitted line to parse

		Returns:
			None: None
		"""
		if len(spl) > 0 and spl[0] == 'network':
			subnet = spl[1]
			mask = invmask_to_mask(spl[2])
			area = spl[4] if spl[3] == 'area' else ''
			network = str(addressing(subnet+"/"+str(mask)))
			if not vrf_op_dict.get('area'):
				vrf_op_dict['area'] = {}
			network_op_dict = vrf_op_dict['area']
			if not network_op_dict.get(area): network_op_dict[area] = {}
			append_attribute(network_op_dict[area], 'active_on_networks', network)


	def summaries(self):
		"""update the ospf area range summaries
		"""    		
		merge_dict(self.op_dict, self.ospf_read(self.get_summaries))

	@staticmethod
	def get_summaries(vrf_op_dict, l, spl):
		"""parser function to get ospf area range summaries

		Args:
			vrf_op_dict (dict): dictionary with a vrf info
			l (str): string line to parse
			spl (list): splitted line to parse

		Returns:
			None: None
		"""
		if len(spl)>3 and spl[0] == 'area' and spl[2] == 'range':
			area = spl[1]
			subnet = spl[3]
			mask = to_dec_mask(spl[4])
			prefix = str(addressing(subnet+"/"+str(mask)))
			if not vrf_op_dict.get('area'):
				vrf_op_dict['area'] = {}
			range_op_dict = vrf_op_dict['area']

			if not range_op_dict.get(area):
				range_op_dict[area] = {}
			append_attribute(range_op_dict[area], 'area-summaries', prefix)

		elif len(spl)>=3 and spl[0] == 'summary-address':
			subnet = spl[1]
			mask = to_dec_mask(spl[2])
			prefix = str(addressing(subnet+"/"+str(mask)))
			if not vrf_op_dict.get('external'):
				vrf_op_dict['external'] = {}
			ext_op_dict = vrf_op_dict['external']
			append_attribute(ext_op_dict, 'summaries', prefix)

	def _remove_empty_instances(self):
		for instance in list(self.op_dict.keys()):
			if not self.op_dict[instance]:
				del(self.op_dict[instance])


# ------------------------------------------------------------------------------

def get_ospf_running(command_output):
	"""defines set of methods executions. to get various ospf parameters.

	Args:
		command_output (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with ospf fields
	"""    	
	R  = OSPF(command_output)
	R.router_id()
	R.active_interfaces()
	R.networks()
	R.summaries()
	R._remove_empty_instances()
	
	if R.op_dict:
		return {'protocols': { 'ospf' : R.op_dict} }
	else:
		return {'protocols': {}}
