
# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
import os, yaml

# -----------------------------------------------------------------------------
#                    FILE OPERATIONS/ CONVERSIONS                             #
# -----------------------------------------------------------------------------

def copy_text_file(file):
	"""copy file.txt to file-copy.txt

	Args:
		file (str): file name
	"""	
	dst = file[:-4] + "-copy.txt"
	with open(file, 'r') as sf:
		with open(dst, 'w') as dt:
			dt.write(sf.read())


def file_list_for_time_stamp(hn, ts, folder, splitter="_@_" ):
	"""collection of files from given folder where hostname (hn) 
	and timestamp (ts) found in the file name.

	Args:
		hn (str): hostname
		ts (str): time-stamp
		folder (str): folder ptah
		splitter (str, optional): splitter. Defaults to "_@_".

	Returns:
		set: files from log files
	"""		
	files = set()
	for file in os.listdir(folder):
		if not splitter in file: continue
		if hn in file and ts in file:
			files.add(file)
	return files


def devices_on_log_files(folder, splitter="_@_"):
	"""collection of files from given folder where file extensions are .log

	Args:
		folder (str): folder path
		splitter (str, optional): splitter. Defaults to "_@_".

	Returns:
		set: devices names from log files
	"""		
	devices = set()
	for file in os.listdir(folder):
		if not splitter in file: continue
		hn = file.split(splitter)
		if hn[0][-4:] == '.log': hn[0] = hn[0][:-4]
		devices.add(hn[0])
	return devices


def timestamps_for_device(devname, folder, splitter="_@_"):
	"""collection of time stamps of files from given folder
	for given hostnames.

	Args:
		devname (str): hostname
		folder (str): folder path
		splitter (str, optional): splitter. Defaults to "_@_".

	Returns:
		set: time stampls from log files.
	"""		
	stamps = set()
	for file in os.listdir(folder):
		if not splitter in file: continue
		if devname in file:
			stamp = file.split(splitter)
			if stamp[-1][-4:] == '.log': stamp[-1] = stamp[-1][:-4]
			stamps.add(stamp[-1])
	return stamps


def file_to_str(file):
	"""Returns string output content of the provided file 

	Args:
		file (str): input file

	Returns:
		str: content of file
	"""		
	with open(file, 'r') as f: 
		s = f.read()
	return s


def file_to_list(file):
	"""Returns list output content of the provided file 

	Args:
		file (str): input file

	Returns:
		list: content of file
	"""		
	file = file.strip()
	if file is None: return None
	with open(file, 'r') as f:
		lines = f.readlines()
	return lines


def csv_to_tuple(csv):
	"""Returns tuple from the provided comma separated text values 

	Args:
		csv (str): input string

	Returns:
		tuple: comma separated values
	"""		
	if csv.find('"') and not csv.find('\"'):
		ln = csv.lstrip().split('"')
		return tuple([x for i, x in enumerate(ln) if i % 2 != 0])
	else:
		return tuple(csv.split(','))

# formerly known as `to_file`
def write_to_file(filename, matter):
	"""Creates a file with matter

	Args:
		filename (str): filename with path to be creaed.
		matter (str, list, tuple): matter to write to new created file.
	"""		
	with open(filename, 'w') as f:
		if isinstance(matter, str):
			f.write(matter)
		elif isinstance(matter, (list, tuple, set)):
			f.write("\n".join(matter))
	return filename


def add_to_file(filename, matter, cr=True):
	"""Writes List/text to output filename.

	Args:
		filename (str): input file
		matter (str, tuple, list): matter to write to new created file.
		cr (bool, optional): carriage return to add at end of each string/line. Defaults to True.

	Returns:
		_type_: _description_
	"""	
	if not filename: return None
	if isinstance(matter, str):
		if cr and matter and matter[-1] != "\n": matter += "\n"
		with open(filename, 'a') as f:
			f.write(matter)
	elif isinstance(matter, (list, tuple ,set)):
		for i in matter:
			add_to_file(filename, i)


def update(file, find_item, replace_item):
	"""Find and Replace on provided file and saves file

	Args:
		file (str): input file
		find_item (str): search item
		replace_item (str): replacement item
	"""		
	with open(file, 'r') as f:
		filedata = f.read()
	replace_item = str(replace_item)
	if replace_item == 'nan': replace_item = '' 
	newdata = filedata.replace(find_item, str(replace_item))
	with open(file, 'w') as f:
		f.write(newdata)


def jinja_verification(folder):
	"""check all text files from provided folder for verification of jinja strings descrepencies

	Args:
		folder (str): folder to check all jinja files from

	Returns:
		str: verification outcomes
	"""		
	s = ''
	for file in os.listdir(folder):
		goahead = {'GOAHEAD FOR': 0, 'GOAHEAD END': 0,}
		repeatfor = {'REPEAT EACH': 0, 'REPEAT STOP': 0,}
		if not file.endswith(".txt"): continue
		with open(folder + "/" +  file, 'r') as f:
			rf = f.read()
			for k, v in goahead.items(): goahead[k] = rf.count(k)
			for k, v in repeatfor.items(): repeatfor[k] = rf.count(k)
		bg, eg = goahead['GOAHEAD FOR'], goahead['GOAHEAD END']
		br, er = repeatfor['REPEAT EACH'], repeatfor['REPEAT STOP']
		if bg != eg or br != er: s += f'Descrepencies found in file: <{file}>\n'
		if bg != eg: s += f"\tGOAHEAD conditions : begins {bg} v/s ends {eg}\n"
		if br != er: s += f"\tREPEAT conditions : begins {br} v/s ends {er}\n\n"
	return s
# ------------------------------------------------------------------------------
#  YAML FILE
# ------------------------------------------------------------------------------
def write_as_yaml(d, file, mode='w', indent=2, default_flow_style=False, sort_keys=False):
    s = yaml.dump(d, 
        indent=indent,
        default_flow_style=default_flow_style, 
        sort_keys=sort_keys,
    )
    with open(file, mode) as f:
        f.write(s)

def read_yaml(file):
	with open(file, "r") as f:
		return yaml.safe_load(f) or {}


# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------
