"""cisco show version command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_version(command_output):
	op_dict = {}
	sw, bootfile, srno, model = '', '', '', ''
	for l in command_output:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		spl = l.strip().split()
		if l.find("Software, Version") > -1:
			sw = spl[-1]
		if l.startswith("System image file"):
			bootfile = spl[-1]
		if not srno and (l.startswith("System Serial") or l.startswith("Processor board ID")):
			srno = spl[-1]
		if l.startswith("Model Number"):
			model = spl[-1]
		if "processor" in spl: 
			model = spl[1]
	op_dict['ios_version'] = sw
	op_dict['bootvar'] = bootfile
	op_dict['serial'] = srno
	op_dict['hardware'] = model
	op_dict['model'] = model
	
	return {'system': op_dict }
# ------------------------------------------------------------------------------
