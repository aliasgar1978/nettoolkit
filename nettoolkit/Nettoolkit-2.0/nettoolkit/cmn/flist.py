
# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
import os

# -----------------------------------------------------------------------------
#                             LIST MODIFICATIONS                              #
# -----------------------------------------------------------------------------

def remove_empty_members(lst):
	"""house keeping of list, removes empty members from list

	Args:
		lst (list): input list

	Returns:
		list: updated list
	"""		
	empty_members = ('', None, 'N/A', 'nil', [])
	tmp_lst = [m for m in lst if not m in empty_members]
	return tmp_lst


def expand_vlan_list(vlan_list):
	"""takes input vlan list, expands it's ranges if any within

	Args:
		vlan_list (list): input vlans list

	Raises:
		Exception: Invalid vlan number

	Returns:
		list: list of vlans (individual)
	"""		
	exp_vl_list = set()
	for v in vlan_list:
		if not v: continue
		try:
			vl = int(v)
			exp_vl_list.add(vl)
			continue
		except:
			s, e = v.split("-")
			try:
				s, e = int(s), int(e)
				r = set(range(s, e+1))
				exp_vl_list = exp_vl_list.union(r)
			except:
				raise Exception(f"[-] Invalid vlan number.  Expected int got {type(s)}, {type(e)}")
	return exp_vl_list


def convert_vlans_list_to_range_of_vlans_list(vlan_list):
	"""converts list of individual vlans to a list of range of vlans

	Args:
		vlan_list (str): input list

	Returns:
		list: list of vlans (with ranges)
	"""		
	vlans_dict, vlans_list, prev, last_key = {}, [], "", ""
	vlan_list = sorted(expand_vlan_list(vlan_list))
	for i, vlan in enumerate(vlan_list):
		if not vlan: continue
		if i == 0:
			prev = vlan
			last_key = vlan
			continue
		if vlan == prev + 1: 
			prev = vlan
			continue
		else:
			vlans_dict[last_key] = prev
			prev = vlan
			last_key = vlan
	else:
		vlans_dict[last_key] = prev
	
	for k, v in vlans_dict.items():
		if k == v:
			vlans_list.append(str(k))
		else:
			vlans_list.append(str(k) + "-" + str(v))    
	return vlans_list


def list_variants(input_list):
	"""list of vlans in different format list of vlans, space separated string, comma separated string,		

	Args:
		input_list (list): input list

	Returns:
		dict: list variants (str, csv, ssv)
	"""		
	str_list = [str(_) 
		for _ in convert_vlans_list_to_range_of_vlans_list(input_list)]
	ssv_list = " ".join(str_list)
	csv_list = ",".join(str_list)
	return {
		'str_list': str_list,
		'ssv_list': ssv_list,
		'csv_list': csv_list,			
	}


def list_of_devices(list_of_files):
	"""get hostnames (first index item) from list of files.

	Args:
		list_of_files (list): input file list

	Returns:
		set: devices from file list
	"""		
	devices = set()
	for file in list_of_files:
		if not file.strip(): continue
		f = ".".join(os.path.basename(file).split(".")[:-1])
		hn = f.split("_")[0]
		if not hn in devices: devices.add(hn)
	return devices


# formerly known as `split`
def split_to_group(lst, n):
	"""yield provided list with group of n number of items

	Args:
		lst (list): list of items
		n (int): items per group 

	Yields:
		list generator: group of items
	"""		
	s = 0
	lst = tuple(lst)
	for _ in range(s, len(lst), n):
		yield lst[_: s+n]
		s += n


def list_to_octet(lst):
	"""joins and return string with provided list with '.', helpful in created ipv4 string with list of 4 numeric items.  Doesn't verify correctness of ip. any number can be concatenated with any numbers of instances.

	Args:
		lst (list): input ip address splitted by "."

	Returns:
		str: concatenated ip address
	"""		
	"""
	
	Returns str
	"""
	l = ''
	for x in lst: l = str(x) if l == '' else l +'.'+ str(x)
	return l


def flatten(lst):
	"""flattens nested list to single list

	Returns:
		list: flattened list
	"""		
	l = []
	for _ in lst:
		if isinstance(_, str):
			l.append(_)
		elif isinstance(_, (set, tuple, list)):
			l.extend( flatten(_) )
	return l


def longest_str_len(lst):
	"""returns length of longest string from provided lst , members shoudl be of string type

	Args:
		lst (list): list of strings

	Returns:
		int: length of maximum length command
	"""		
	if lst:
		return max(len(str(_)) for _ in lst)
	else:
		return 0

## TBD // Need to change name from add_to_list to --> add_to_list_if_missing()
## remove add_to_list at last
def add_to_list(lst, item):
	"""appends item to list if not found

	Args:
		lst (list): list
		item (str, int): item to be added to list

	Returns:
		list: updated list
	"""	
	if not isinstance(lst, list):
		lst  = [lst, ]
	if item in lst:
		return lst
	return lst.append(item)
add_to_list_if_missing = add_to_list

def create_and_add_to_list(src, item):
	if isinstance(src, list):
		return src.append(item)
	if isinstance(src, (str, int)):
		return [src, item]
	else:
		raise Exception(f"Invalid input source: {src} expected type: (str, int, list), got: {type(src)}")

# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------
