"""juniper prefix list parsing from set config  """

# ------------------------------------------------------------------------------
# from nettoolkit.addressing import addressing
from .common import *
from .run import Running
# ------------------------------------------------------------------------------

class RunningPrefixLists(Running):
	"""object for prefix list level config parser
	"""    	

	def __init__(self, cmd_op):
		"""initialize the object by providing the  config output

		Args:
			cmd_op (list, str): config output, either list of multiline string
		""" 
		self.n = 0   		    		
		super().__init__(cmd_op)
		self.pl_dict = {}

	# ----------------------------------------------------------------------------- #
	def pl_read(self, func, v=4):
		"""directive function to get the various static prefix list level output

		Args:
			func (method): method to be executed on set commands

		Returns:
			dict: parsed output dictionary
		"""
		_str = 'set policy-options prefix-list '
		ports_dict = {}
		for l in self.set_cmd_op:
			if blank_line(l): continue
			if l.strip().startswith("#"): continue
			if not l.startswith(_str): continue
			spl = l.split()
			pl_name = spl[3]
			if not ports_dict.get(pl_name):
				ports_dict[pl_name] = []
			rdict = ports_dict[pl_name]
			func(rdict,  l, spl)
		return ports_dict

	# ----------------------------------------------------------------------------- #

	def pfxlst_dict(self):
		"""update the prefix list details
		"""
		func = self.get_pl_dict
		merge_dict(self.pl_dict, self.pl_read(func, 4))

	@staticmethod
	def get_pl_dict(dic, l, spl):
		"""parser function to update prefix list details

		Args:
			dic (dict): blank dictionary to update a prefix list info
			l (str): line to parse

		Returns:
			None: None
		"""
		if len(spl) > 4: pfx = spl[4]
		try:
			if pfx: p = addressing(pfx)
		except:
			return None
		dic.append(pfx)




	# # Add more static route related methods as needed.


# ------------------------------------------------------------------------------


def get_system_running_prefix_lists(cmd_op):
	"""defines set of methods executions. to get various instance of prefix list parameters.
	uses RunningPrefixLists in order to get all.

	Args:
		cmd_op (list, str): running config output, either list of multiline string

	Returns:
		dict: output dictionary with parsed with system fields
	"""    	
	R  = RunningPrefixLists(cmd_op)
	R.pfxlst_dict()

	return {'prefix-lists': R.pl_dict}



# ------------------------------------------------------------------------------

