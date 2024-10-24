"""juniper show chassis hardware command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_chassis_serial(cmd_op):
	op_dict = {}
	toggle = False
	for l in cmd_op:
		if not l.startswith('Chassis'): continue
		spl = l.split()
		op_dict.update({'serial': spl[-2]})

	return {'system': op_dict}
