"""juniper show version command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_version(cmd_op):
	op_dict = {}
	version, model = "", ""
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("#"): continue
		if l.startswith("Junos: "):  version = l.split()[-1]
		if l.startswith("Model: "): model = l.split()[-1]

	if not op_dict.get('junos_version'): op_dict['junos_version'] = version
	if not op_dict.get('model'): op_dict['model'] = model
	return {'system': op_dict}
# ------------------------------------------------------------------------------
