"""juniper show chassis hardware command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_chassis_hardware(cmd_op):
	op_dict = {}
	toggle = False
	JCH = JuniperChassisHardware(cmd_op)
	for p in  JCH.ports:
		sfp = JCH.get_sfp(p)
		if not sfp: continue
		op_dict[p] = sfp

	return {'interfaces': {'media_type': op_dict}}


class JuniperChassisHardware():
	"""read the show chassis hardware output from juniper and returns port type(sfp)

	Args:
		output (list): show chassis hardware output in list
	"""

	def __init__(self, output):
		"""initialize and read output
		"""    		
		self.fpc, self.pic = '', ''
		self.port = ''
		self.ports = {}
		self._read(output)

	def _read(self, output):
		"""read the output and adds line to port info

		Args:
			output (list): show chassis hardware command output in list
		"""		
		for l in output:
			if not l.strip(): continue
			self._add(l)

	def _add(self, line):
		"""adds port info from line 

		Args:
			line (str): line outout
		"""		
		# if line.upper().find("BUILTIN") > 0: return         # Some of juniper output are incosistent so removed.
		spl = line.strip().split()
		if not spl[0].upper() in ("FPC", "PIC", "XCVR"): return
		if spl[0].upper() in ("FPC"):
			self.fpc = spl[1]
			self.pic = ''
		elif spl[0].upper() in ("PIC"):
			self.pic = self.fpc + "/" + spl[1]
		elif spl[0].upper() in ('XCVR',):
			self.port = self.pic + "/" + spl[1]
			self.ports[self.port] = spl[-1]
			self.port=''

	def get_sfp(self, port):
		"""get the SFP details for given port

		Args:
			port (str): port number only (port type to be excluded)

		Returns:
			str: SFP type
		"""    		
		for p, sfp in self.ports.items():
			spl_port = port.split("-")
			if spl_port[-1] == p:
				return sfp
		return ""

