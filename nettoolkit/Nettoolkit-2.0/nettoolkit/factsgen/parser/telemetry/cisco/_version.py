"""cisco show version command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line
# ------------------------------------------------------------------------------

def get_version(cmd_op, *args):
	"""parser - show version command output

	Parsed Fields:
		* software
		* bootfile
		* serial
		* model

	Args:
		cmd_op (list, str): command output in list/multiline string.

	Returns:
		dict: output dictionary with parsed fields
	"""	
	op_dict = {}
	sw, bootfile, srno, model = '', '', '', ''
	for l in cmd_op:
		if blank_line(l): continue
		if l.strip().startswith("!"): continue
		spl = l.strip().split()
		if l.find("Software, Version") > -1:
			sw = spl[-1].rstrip(',')
		elif l.startswith("System image file"):
			bootfile = spl[-1].strip('"')
		elif not srno and (l.startswith("System Serial") or l.startswith("Processor board ID")):
			srno = spl[-1]
		elif l.startswith("Model Number"):
			model = spl[-1]
		elif "processor" in spl: 
			try:
				# Isolate the token right before the word 'processor' dynamically
				p_idx = spl.index("processor")
				if p_idx > 1:
					model = spl[p_idx - 1]
			except ValueError:
				pass

	# --- MAP VARIABLES DIRECTLY TO THE NESTED DATA MODEL ---
	op_dict['software'] = {
		'version': sw,
		'boot_file': bootfile
	}

	# Resolves redundancy completely by nesting physical identifiers together
	op_dict['hardware'] = {
		'model': model,
		'serial_number': srno
	}	
	return {'op_dict': op_dict }
# ------------------------------------------------------------------------------
