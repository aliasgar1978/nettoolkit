
from nettoolkit.nettoolkit_common.gpl import *
from nettoolkit.nettoolkit_common import *
from nettoolkit.nettoolkit_db import *
from nettoolkit.addressing import IPv4, IPv6
from nettoolkit.pyNetCrypt import *
from nettoolkit.pyJuniper import *

# ================================================================================================
# common functions
# ================================================================================================

def append_attribute(dic, attribute, value, remove_duplicate=False):
	if not dic.get(attribute):
		dic[attribute] = value		
	elif dic[attribute] and isinstance(dic[attribute], str):
		if remove_duplicate and value == dic[attribute]: return
		dic[attribute] = [ dic[attribute], value ]
	elif dic[attribute] and isinstance(dic[attribute], list):
		if remove_duplicate and value in dic[attribute]: return
		dic[attribute].append( value )
	else:
		dic[attribute] = value

def get_instance_parameter_for_items(dic, line, spl, items, unique=False):
	for item in items:
		_get_instance_parameter(dic, line, spl, item, unique)

def _get_instance_parameter(dic, line, spl, item, unique=False):
	if item not in spl: return
	append_attribute(dic, attribute=item, value=spl[spl.index(item)+1], remove_duplicate=unique)

def update_true_instance_items(dic, line, spl, items):
	for item in items:
		_update_true_instance(dic, line, spl, item)

def _update_true_instance(dic, line, spl, item):
	if item not in spl: return
	dic[item]=True

def get_nest_attributes(input_dict, line, spl, nest_attrs, next_attr=True, unique=False):
	if isinstance(nest_attrs, dict):
		for k, v in nest_attrs.items():
			if not v: continue
			if k not in spl: continue
			dic = add_blankdict_key(input_dict, k)
			get_nest_attributes(dic, line, spl, v, next_attr, unique)

	elif isinstance(nest_attrs, (list, tuple, set)):
		if next_attr:
			get_instance_parameter_for_items(input_dict, line, spl, nest_attrs, unique)
		else:
			update_true_instance_items(input_dict, line, spl, nest_attrs)

	else:
		print(f"Unidentified attribute type: {type(nest_attrs)}, {nest_attrs}")






def get_appeneded_value(dic, key, value):
	"""appends the value to an existing value found in dictionary with provided key if exist other wise returns same value

	Args:
		dic (dict): dictionary
		key (str): dictionary key
		value (str): arbitrary value to be appended to existing key if exist

	returns:
		str: appened string
	"""
	if not dic.get(key):
		return value
	else:
		return dic[key] + '\n'+ value

def add_to_list(lst, item):
	"""appends item to list if not found

	Args:
		lst (list): list
		item (str, int): item to be added to list

	Returns:
		list: updated list
	"""	
	if item in lst:
		return lst
	return lst.append(item)

# ================================================================================================

def get_subnet(address):
	"""derive subnet number for provided ipv4 address

	Args:
		address (str): ipv4 address in string format a.b.c.d/mm

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv4(address).subnet_zero()

def get_v6_subnet(address):
	"""derive subnet number for provided ipv6 address

	Args:
		address (str): ipv6 address in string with mask

	Returns:
		str: subnet zero == network address
	"""    	
	return IPv6(address).subnet_zero()


def get_int_ip(ip): 
	"""get ip address from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: ip address
	"""	
	return ip.split("/")[0]

def get_int_mask(ip): 
	"""get mask from ip/mask info

	Args:
		ip (str): ip with mask

	Returns:
		str: mask
	"""	
	return ip.split("/")[-1]
# ================================================================================================


def add_blankdict_key(dic, key):
	if not dic.get(key):
		dic[key] = {}
	return dic[key]

def add_blankset_key(dic, key):
	if not dic.get(key):
		dic[key] = set()
	return dic[key]

def add_blanklist_key(dic, key):
	if not dic.get(key):
		dic[key] = []
	return dic[key]

def add_blanktuple_key(dic, key):
	if not dic.get(key):
		dic[key] = ()
	return dic[key]

def add_blanknone_key(dic, key):
	if not dic.get(key):
		dic[key] = None
	return dic[key]

def update_key_value(dic, key, value):
	if not dic.get(key):
		dic[key] = value

def next_index_item(lst, item):
	return lst[lst.index(item)+1]