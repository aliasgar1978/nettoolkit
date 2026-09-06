# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#                          DICTIONARY MODIFICATIONS                           #
# -----------------------------------------------------------------------------

# INTERNAL : update dictionary d for provided keyvalue pairs
# param: d: dest dictionary
# param: kv: src dictionary with key value pairs
# --> updated destn dict

def __update_keyValue(d, kv):
	if isinstance(d, dict):
		for k, v in kv.items():
			if isinstance(v, dict):
				for x, y in v.items():
					d = merge_dict(d, kv)
			else:
				d[k] = v
	return d


def merge_dict(dx, dy):
	"""Merges two dictionaries for identical keys 

	Args:
		dx (dict): first dictionary
		dy (dict): second dictionary

	Returns:
		dict: merged dictionary
	"""		
	for k, v in dy.items():
		try:
			dx[k] = __update_keyValue(dx[k], dy[k])
		except:
			dx[k] = dy[k]
	return dx


def recursive_dic(dic, indention=0):
	"""convert dictionary (dic) to string. recursive dictionary increases indention. (deprycated, will be replaced with `dict_to_str`)

	Args:
		dic (dict): input dictionary
		indention (int, optional): number of spaces. Defaults to 0.

	Returns:
		str: Multiline string
	"""		
	s = ""
	if isinstance(dic, dict):
		for k, v in dic.items():
			s += f"{' '*indention}{k}\n"
			indention += 1
			s += recursive_dic(v, indention)
			indention -= 1
	elif isinstance(dic, (tuple,list,set)):
		for x in dic: 
			if x: s += str(x)+'\n'
	elif isinstance(dic, str):
		if dic: s+= f"  {' '*indention}{dic}\n"
	return s


def dict_to_str(dic, indention=0):
	"""convert dictionary (dic) to string. recursive dictionary increases indention.

	Args:
		dic (dict): input dictionary
		indention (int, optional): number of spaces. Defaults to 0.

	Returns:
		str: Multiline string
	"""		
	recursive_dic(dic, indention)

# -----------------------------------------------------------------------------
#                         DICTIONARY DIFFERECES                               #
# -----------------------------------------------------------------------------

class DifferenceDict(dict):
	"""Template class to get difference in two dictionary objects.
	use dunder +/- for adds/removes.	
	"""

	missing = "- "
	additive = "+ "

	def __init__(self, d):
		self.d = d

	def __sub__(self, d): return self.get_change(d, self.missing)
	def __add__(self, d): return self.get_change(d, self.additive)

	def get_change(self, d, change):
		"""compare current object/dict with provided new object/dict (ie: d) 
		and return differences based on change required ("- "/"+ ")

		Args:
			d (dict): dictionary of differences
			change (str): change type from ("- "/"+ ")  i.e. removed/added

		Returns:
			_type_: _description_
		"""		
		"""
		"""
		if isinstance(d, DifferenceDict):
			return dict_differences(self.d, d.d, change)
		elif isinstance(d, dict):
			return dict_differences(self.d, d, change)

# INTERNAL / RECURSIVE
# returns differences for provided subnet/change
# input subject can be of string/int/float/set/dictionary
# input change is change type prefix
# return value type depends on input subject type.
def _get_differences(subject, change):
	if isinstance(subject, (str, int, float)):
		diff = change + str(subject)
	elif isinstance(subject, (list, tuple)):
		diff = []
		for item in subject:
			df = _get_differences(item, change)
			diff.append(df)
	elif isinstance(subject, set):
		diff = set()
		for item in subject:
			df = _get_differences(item, change)
			diff.add(df)
	elif isinstance(subject, dict):
		diff = dict()
		for key, value in subject.items():
			key = change + str(key)
			if value:
				diff[key] = _get_differences(value, change)
			else: 
				diff[key] = ''
	else:
		raise Exception(f"[-] InvalidSubjectTypeError: {type(subject)}:{subject}")
	return diff


def dict_differences(d1, d2, change):
	"""returns differences for provided two dictionaries 
	input d1, d2 type: string/int/float/set/dictionary
	input change is change type prefix (ex: " -", " +")
	return value type depends on input d1, d2 type.

	Args:
		d1 (str, int, float, set, dict): input 1
		d2 (str, int, float, set, dict): input 2
		change (str):  change type from ("- "/"+ ")  i.e. removed/added

	Raises:
		Exception: TypeMismatch

	Returns:
		dict: differences in dictionary format
	"""	
	diff = {}
	if d1 == d2: return None
	if (not (isinstance(d1, (dict, set)) or isinstance(d2, (dict, set))) and
		type(d1) != type(d2)): 		
		raise Exception(f"[-] TypeMismatch- d1:{type(d1)}d2:{type(d2)} - {d1}{d2}")
	if isinstance(d1, dict):
		for k_d1, v_d1 in d1.items():
			if k_d1 not in d2: 
				diff.update( _get_differences({k_d1: v_d1}, change) )
				continue
			if v_d1 == d2[k_d1]: continue
			diff[k_d1] = dict_differences(v_d1, d2[k_d1], change)
	elif isinstance(d1, set):
		diff = _get_differences(d1.difference(d2), change)
	else:
		if d1:
			diff = _get_differences(d1, change)

	return diff

# -----------------------------------------------------------------------------
#                         Common Dictionary Methods                           #
# -----------------------------------------------------------------------------
class DictMethods():
	"""PAPA DUNDER EXTENSIONS FOR DICTIONARY OBJECTS

	[self.dic is abstract property which gets iterates over]
	"""

	def __iter__(self):
		for k, v in self.dic.items():
			yield (k, v)

	def __getitem__(self, item):
		try:
			return self.dic[item]
		except KeyError:
			return None

	def __get__(self, key, item):
		try:
			return self[key][item]
		except KeyError:
			return None

	def __setitem__(self, item, value):
		self.dic[item] = value

	def __delitem__(self, srno):
		try:
			for k in sorted(self.dic.keys()):
				if k <= srno: continue
				self.dic[k-1] = self.dic[k]
			del(self.dic[k])
		except:
			raise KeyError

	def append(self, item, value):
		"""appends value to self[item] dictionary. create new list if no value found for item, appends to list if available.

		Args:
			item (str, int): key of dictionary
			value (list): value to be added to dictionary item

		Raises:
			Exception: WrongInput
		"""		
		try:
			if not self.dic.get(item):
				self.dic[item] = []
			elif isinstance(self.dic[item], (str, int)):
				self.dic[item] = [self.dic[item],]
			self.dic[item].append(value)
		except:
			raise Exception

def get_appeneded_value(dic, key, value, appened_as='l'):
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
	if appened_as == 's':
		return dic[key] + '\n'+ value
	if appened_as == 'l':
		if isinstance(dic[key], str):
			return [dic[key], value]
		elif isinstance(dic[key], list):
			return dic[key].append(value)
		else:
			raise Exception(f"Invalid type: in get_appeneded_value(key): Expected either Str,List; got {type(dic[key])}  ")
	else:
		raise Exception(f"Invalid argument append_as: expected either `s`or `l` got {appened_as}")



# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------
