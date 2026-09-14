# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
import datetime
from collections import OrderedDict
from getpass import getpass

from .statics import intBeginWith, CISCO_IFSH_IDENTIFIERS, JUNIPER_IFS_IDENTIFIERS
from .flist import remove_empty_members



# from inspect import signature

# import pandas as pd

# from abc import ABC, abstractproperty, abstractclassmethod
# from time import sleep
# from re import compile
# import os
# import threading
# from .common import deprycation_warning


# -----------------------------------------------------------------------------
#                              INPUT METHODS                                  #
# -----------------------------------------------------------------------------


def get_username():
	"""input username prompt

	Returns:
		str: entered username
	"""	
	return input("Enter Username: ")

def get_password():
	"""input password prompt

	Returns:
		str: entered password
	"""	
	return getpass("Enter Password: ")



# -----------------------------------------------------------------------------
#                           STRING OPERATIONS                                 #
# -----------------------------------------------------------------------------

def foundPos(s, sub, pos=0):
	'''Search for substring in string and return index value result

	Args:
		s (str): main string to be search within
		sub (str): substring which is to be search in to main string
		pos (int, optional): position index, search to be start from. Defaults to 0.

	Returns:
		int: find index value
	'''		
	return s.find(sub, pos)

def found(s, sub, pos=0):
	"""Search for substring in string and return Boolean result

	Args:
		s (str): main string to be search within
		sub (str): substring which is to be search in to main string
		pos (int, optional): position index, search to be start from. Defaults to 0.

	Returns:
		bool: find or not
	"""		
	try:
		return True if s.find(sub, pos) > -1 else False
	except:
		return False

def find_within(s, prefix, suffix=None, pos=0):
	"""finds characters between prefix and suffix substrings from string

	Args:
		s (str): main string to be search within
		prefix (str): starting substring
		suffix (str, optional): ending substring. Defaults to None.
		pos (int, optional): position index, search to be start from. Defaults to 0.

	Returns:
		tuple: (str, int) (returned string, position of returned suffix position)
	"""		
	p = foundPos(s, prefix, pos=pos)+len(prefix)
	if suffix is None:
		ln = len(s)
	else:
		ln = foundPos(s, suffix, pos=p+1)
	if p == -1:
		return None
	if ln == -1:
		ln = len(s)
	return (s[p:ln], ln)

def string_within(line, prefix, suffix=None, pos=0):
	"""finds characters between prefix and suffix substrings from string

	Args:
		line (str): main string to be search within
		prefix (str): starting substring
		suffix (str, optional): ending substring. Defaults to None.
		pos (int, optional): position index, search to be start from. Defaults to 0.

	Returns:
		tuple: (str, int) (returned string, position of returned suffix position)
	"""		

	return find_within(line, prefix, suffix, pos)[0]

def suffix_index_within(line, prefix, suffix=None, pos=0):
	"""finds characters between prefix and suffix substrings from string

	Args:
		line (str): main string to be search within
		prefix (str): starting substring
		suffix (str, optional): ending substring. Defaults to None.
		pos (int, optional): position index, search to be start from. Defaults to 0.

	Returns:
		int: index of suffix
	"""	
	return find_within(line, prefix, suffix, pos)[1]

def find_multi(s, sub, start=0, count=None, index=True, beginwith=False):
	"""search for multiple substrings 'sub' within string 's'.
	Usage: find_multi(s, sub, [start=n, [count=c], index=True])

	Args:
		s (str): main string
		sub (str, tuple, list): sub string ( to be search within main string )
		start (int, optional): Optional: substring to be start search from index . Defaults to 0.
		count (int, optional): Optional: count of character from start index. Defaults to None.
		index (bool, optional): Optional: return index or boolean values. Defaults to True.
		beginwith (bool, optional): Optional: check if substring is at beginning. Defaults to False.

	Returns:
		list: list of indexes/bool
	"""		
	count = len(s) if count is None else count+start
	if isinstance(sub, str):
		i = s.find(sub, start, count) 
		if index:
			if beginwith:
				return i if i == 0 else -1
			else:
				return i
		else:
			if beginwith:
				return True if i == 0 else False
			else:
				return False if i == -1 else True
	elif isinstance(sub, (tuple, list)):
		sl = []
		for x in sub:
			sl.append(find_multi(s, x, start, count, index, beginwith))
		return sl
	else:
		return None


def find_all(s, sub, start=0, count=None, beginwith=False):
	"""search for multiple substrings 'sub' within string 's' 
	Usage: find_all(s, sub, [start=n, [count=c]])

	Args:
		s (str): main string
		sub (str): sub string ( to be search within main string )
		start (int, optional): Optional: substring to be start search from index. Defaults to 0.
		count (int, optional): Optional: count of character from start index. Defaults to None.
		beginwith (bool, optional): Optional: check if substring is at beginning. . Defaults to False.

	Returns:
		bool: all matches or not
	"""		
	sl = find_multi(s, sub, start, count, False, beginwith)
	try:
		return False if False in sl else True
	except:
		return sl


def find_any(s, sub, start=0, count=None, beginwith=False):
	"""search for multiple substrings 'sub' within string 's' 
	Usage: find_any(s, sub, [start=n, [count=c]])

	Args:
		s (str): main string
		sub (str): sub string ( to be search within main string )
		start (int, optional): Optional: substring to be start search from index. Defaults to 0.
		count (int, optional): Optional: count of character from start index. Defaults to None.
		beginwith (bool, optional): Optional: check if substring is at beginning. . Defaults to False.

	Returns:
		bool: for atleast one matches
	"""		
	sl = find_multi(s, sub, start, count, False, beginwith)
	try:
		return True if True in sl else False
	except:
		return sl


def update(s, searchItem='', replaceItem=''):
	"""find n replace string s

	Args:
		s (str): main string
		searchItem (str, optional): search string. Defaults to ''.
		replaceItem (str, optional): replacement string. Defaults to ''.

	Returns:
		str: updated string
	"""		
	return s.replace(searchItem, replaceItem)


def replace_dual_and_split(s, duo=' ', strip=None):
	"""Finds subsequent characters in string and replace those with single,
	plus, splits the string using provided character (duo).

	Args:
		s (str): main string
		duo (str, optional): characters which requires reductions if susequent. Defaults to ' '.
		strip (int, optional): values (-1=lstrip ,0=strip ,1=rstrip) . Defaults to None.

	Returns:
		list: split using dual characters
	"""		
	return finddualnreplacesingle(s, duo, strip=strip).split(duo)


def finddualnreplacesingle(s, duo=' ', strip=None):
	"""Finds subsequent characters in string and replace those with single.

	Args:
		s (str): Source string
		duo (str, optional): characters which requires reductions if susequent. Defaults to ' '.
		strip (int, optional): values (-1=lstrip ,0=strip ,1=rstrip). Defaults to None.

	Returns:
		_type_: _description_
	"""		
	while s.find(duo+duo) > -1:
		s = s.replace(duo+duo, duo)
	if strip is not None and isinstance(strip, int):
		if strip == -1:
			return s.lstrip()
		elif strip == 0:
			return s.strip()
		elif strip == 1:
			return s.rstrip()
		else:
			pass
			# print('invalid strip value detected', strip)
	else:
		pass
		# print('invalid strip value detected', strip)
	return s


def indention(s):
	"""get string indention value

	Args:
		s (str): input string

	Returns:
		int: number of indentants
	"""		
	return len(s)-len(s.lstrip())

def blank_line(s): 
	"""checks if provided line is blank line or not.

	Args:
		line (str): input line

	Returns:
		bool: is line blank or not
	"""	
	return not s.strip()

def is_blank_line(s):
	"""is provided string/line a blank line

	Args:
		s (str): input string

	Returns:
		bool: boolean value for result
	"""		
	try:
		return len(blank_line(s)) == 0
	except Exception: pass


def is_hostname_line(s, host):
	"""string/line containing hostname of device

	Args:
		s (str): input string
		host (str): hostname to be find in provided string

	Returns:
		bool: boolean value for result
	"""		
	return s.find(host) == 0


def hostname(net_connect):
	"""input paramiko netconnection, returns hostname from device.

	Args:
		net_connect (connection object): paramiko connection object

	Returns:
		str: hostname from connection
	"""		
	try:
		hns = net_connect.find_prompt()[:-1]
		atPos = foundPos(hns, "@")
		if atPos > -1: hns = hns[atPos+1:]
		return hns
	except:
		pass


def hostname_from_cli(line, command):
	"""input standard text input line, for which command was entered

	Args:
		line (str): input line string
		command (str): command

	Returns:
		str: hostname from command line
	"""		
	if not found(line, command): return None
	cmdPos = foundPos(line, command)
	hn = line[:cmdPos].strip()[:-1]
	return hn


def shrink_if(intName, length=2):
	"""Interface Name shortening, input length will decide number of 
	charactes to be included in shortened output

	Args:
		intName (str): interface
		length (int, optional): interface identifier prefix length. Defaults to 2.

	Returns:
		str: short name of interface
	"""		
	if not intName: return ""
	if intName.lower().startswith("tw"): length=3
	iBW = intBeginWith.match(intName)
	return iBW.group()[:length]+intName[iBW.span()[1]:]


def if_prefix(intName):
	"""Interface beginning Name

	Args:
		intName (str): interface

	Returns:
		str: interface prefix
	"""		
	if not intName: return ""
	iBW = intBeginWith.match(intName)
	return intName[iBW.start(): iBW.end()]


def if_suffix(intName):
	"""Interface ending ports

	Args:
		intName (str): interface

	Returns:
		str: interface suffix
	"""		
	if not intName: return ""
	try:
		iBW = intBeginWith.match(intName)
		return intName[iBW.end():]
	except:
		return ""

def is_interface(intName):
	int_type = interface_type(intName)
	return bool(int_type[0] and int_type[1])

def if_standardize(intName, expand=True):
	"""standardize the interface for uneven length strings.
	expand will give fulllength, otherwise it will shrink it to its standard size given

	Args:
		intName (str): interface
		expand (bool, optional): expansion of interface. Defaults to True.

	Returns:
		str: standardized interface
	"""		
	if not intName: return intName
	intName = intName.replace(" ", "")
	pfx = if_prefix(standardize_if(intName))
	sfx = if_suffix(intName)
	for _, inttype_length in CISCO_IFSH_IDENTIFIERS.items():
		for int_type, length in inttype_length.items():
			if int_type.lower().startswith(pfx.lower()):
				if expand:
					return f"{int_type}{sfx}"
				else:
					return f"{int_type[:length]}{sfx}"
	return intName


def intf_standardize_or_null(intName, intf_type=None, expand=True):
	"""standardize the interface for uneven length strings.
	expand will give fulllength, otherwise it will shrink it to its standard size given
	for incorrect interface returns blank (None)

	Args:
		intName (str): interface
		expand (bool, optional): expansion of interface. Defaults to True.

	Returns:
		str: standardized interface or blank 
	"""		
	try:
		return standardize_if(intName)
	except:
		return ""


def update_str(s, searchItem='', replaceItem=''):
	"""Updates line for search item with replace item
	(Find/Repalace)

	Args:
		s (str): input string
		searchItem (str, optional): search item. Defaults to ''.
		replaceItem (str, optional): replacement item. Defaults to ''.

	Returns:
		str: updated string
	"""		
	return s.replace(searchItem, replaceItem)


def get_logfile_name(folder, hn, cmd='', ts='', separator="_@_", extn='.log'):
	"""return log file name for the command on device with/wo provided time_stamp

	Args:
		folder (str): path to where file should be saved
		hn (str): file name starting with provided host-name
		cmd (str, optional): file name containing additional commands string. Defaults to ''.
		ts (str, optional): file name containing additional time stamp. Defaults to ''.
		separator (str, optional): hn-cmd-ts separator . Defaults to "_@_".
		extn (str, optional): extension of filename. Defaults to '.log'.

	Returns:
		str: filename along with full path
	"""		
	if ts: ts = separator + ts
	cmd += ts
	if cmd:
		replaceCandidates = ('|',  '\\', '/', ':', '*', '?', '"', '<', '>')
		for x in replaceCandidates:
			cmd = update_str(cmd, x, "_")
		cmd = separator + cmd
	if folder[-1] not in ( "/", "\\"):
		folder += "/" 
	return folder+hn+cmd+extn


def string_concate(s, s1, conj=''):
	"""Concatenate strings s and s1 with conjuctor conj

	Args:
		s (str): input string
		s1 (str): adder string
		conj (str, optional): conjuctor. Defaults to ''.

	Returns:
		str: updated string
	"""		
	return s + s1 if s == '' else s + conj + s1


def right(strg, n):
	"""N-number of characters from right side of string

	Args:
		strg (str): input string
		n (int): number of characters from right

	Returns:
		str: string portion from right
	"""		
	l = len(strg)
	return strg[l-n:l]
	

def mid(strg, pos, n=0):
	"""N-number of characters from position in string; default n is till end

	Args:
		strg (str): input string
		pos (int): position from where slice to begin
		n (int): number of characters from from slice(pos)

	Returns:
		str: string portion from middle
	"""		
	l = len(strg)
	if n > 0 :
		return strg[pos-1:pos+n-1]
	else:
		return strg[pos-1:]


def delete_trailing_remarks(s):
	"""Deletes trailing remarks from Juniper config line/string

	Args:
		s (str): number of characters from right

	Returns:
		str: updated string
	"""		
	terminal = s.find(";")
	br_open = s.find("{")
	br_close = s.find("}")
	if s.find("##") > max(terminal, br_open, br_close) :
		s = s[:s.find("##")].rstrip()
		return s.rstrip()
	endingpos = foundPos(s, ";")
	if endingpos < 0: endingpos = foundPos(s, "{")
	if endingpos < 0: endingpos = foundPos(s, "}")
	if endingpos > -1: return s[:endingpos+1]
	return s.rstrip()


def to_list(s):
	"""Returns list for the provided string - s, 
	splits string by lines

	Args:
		s (str): multiline input string

	Returns:
		list: splitted lines
	"""		
	s = s.split("\n")
	for i, x in enumerate(s):
		s[i] = x + "\n"
	return s


def to_set(s):
	"""Return set of values for the provided string - s.
	splits string by lines and comma

	Args:
		s (str): multiline input string

	Returns:
		set: splitted lines/items
	"""		
	if isinstance(s, str):
		_s = []
		for _ in s.split('\n'):
			_s.extend(_.split(','))
		return set(remove_empty_members((_s)))
	else:
		return set(s)


def header_indexes(line):
	"""input header string line of a text table.
	returns dictionary with key:value pair where 
	keys are header string and value are string index (position) of string in line

	Args:
		line (str): input header string

	Returns:
		dict: header with its index numbers
	"""		
	exceptional_headers = {}
	headers = OrderedDict()
	prev_k = None
	for k in replace_dual_and_split(line.rstrip()):
		k = k.strip()
		key = k
		if key in exceptional_headers: key = "__"+key
		headers[key] = [foundPos(line, k), None]
		if prev_k is not None:
			headers[prev_k][1] = foundPos(line, k)
		prev_k = key
	headers[key][1] = 90
	return headers


def header_indexes_using_splitby(line, split_by="  "):
	"""input header string line of a text table.
	returns dictionary with key:value pair where 
	keys are header string and value are string index (position) of string in line

	Args:
		line (str): input header string
		split_by (str): string using which line is to be broken

	Returns:
		dict: header with its index numbers
	"""		
	exceptional_headers = {}
	headers = OrderedDict()
	prev_k = None
	last_found_position = 0

	spl_line = remove_empty_members(line.split(split_by))

	for k in spl_line:
		k = k.strip()
		key = k
		if key in exceptional_headers: 
			key = "__"+key

		start_pos = foundPos(line, k, last_found_position)
		headers[key] = [foundPos(line, k, start_pos), None]

		if prev_k is not None:
			headers[prev_k][1] = start_pos

		prev_k = key
		last_found_position = start_pos + len(k)

	if prev_k is not None:
		headers[key][1] = len(line)

	return headers


def prepend_bgp_as(bgp_as, n):
	"""`n` number of BGP AS Number prepending string.

	Args:
		bgp_as (str): bgp as number
		n (int): to repeat with

	Returns:
		str: as-path prepend string
	"""		
	s = ''
	for x in range(n): s += str(bgp_as) + " "
	return s[:-1]


def ending(line, c): 
	"""check if line ends with c or not, same as native string.endswith()
	addition is it first strips the line and then checks

	Args:
		line (str): input string
		c (str): condition string

	Returns:
		bool: boolean value for result
	"""		
	return line.strip().endswith(c)


def starting(line, c): 
	"""check if line starts with c or not, same as native string.startswith()
	addition is it first strips the line and then checks

	Args:
		line (str): input string
		c (str): condition string


	Returns:
		bool: boolean value for result
	"""		
	return line.strip().startswith(c)

# -----------------------------------------------------------------------------

def interface_type(ifname):
	"""get the interface type from interface string

	Args:
		ifname (str): interface name/string

	Raises:
		ValueError: raise error if input missing

	Returns:
		tuple: tuple with interface type (e.g PHYSICAL, VLAN...) and sub interface type 
		(e.g FastEthernet, .. ). None if not detected
	"""    	
	iname = ''
	for i in ifname:
		if not i.isdigit(): iname += i
		else: break
	ifname = iname
	if ifname: 
		for int_type, int_types in  CISCO_IFSH_IDENTIFIERS.items():
			for sub_int_type in int_types:
				if sub_int_type.lower().startswith(ifname.lower()):
					return (int_type, sub_int_type)
	return ("", "")

def standardize_if(ifname, expand=False):
	"""standardized interface naming

	Args:
		ifname (str): variable length interface name
		expand (bool, optional): expand will make it full length name. Defaults to False.

	Raises:
		ValueError: if missing with mandatory input
		TypeError: if invalid value detected
		KeyError: if invalid shorthand key detected		

	Returns:
		str: updated interface string
	"""    	
	if not ifname:
		raise ValueError("Missing mandatory input ifname")
	if not isinstance(expand, bool): 
		raise TypeError(f"Invalid value detected for input expand, "
		f"should be bool.")
	if not isinstance(ifname, str): 
		raise TypeError(f"Invalid value detected for input ifname, "
		f"should be ")
	srcifname = ''
	for i in ifname:
		if not i.isdigit(): srcifname += i
		else: break
	if not srcifname: return None
	try:
		it = interface_type(srcifname)
		if it: 
			int_type, int_pfx = it[0], it[1]
		else:
			return ifname
	except:
		raise TypeError(f"unable to detect interface type for {srcifname}")
	try:
		shorthand_len = CISCO_IFSH_IDENTIFIERS[int_type][int_pfx]
	except:
		if get_juniper_int_type(ifname): return ifname
		raise KeyError(f"Invalid shorthand Key detected {int_type}, {int_pfx}")
	if expand:  return int_pfx+ifname[len(srcifname):]
	return int_pfx[:shorthand_len]+ifname[len(srcifname):]


# -------------------------------------------------------------------------------------
def get_juniper_int_type(intf):
	"""returns juniper interface type

	Args:
		intf (str): juniper interface

	Returns:
		str: interface type (ge, xe, etc)
	"""	
	int_type = ""
	for k, v in JUNIPER_IFS_IDENTIFIERS.items():
		if intf.startswith(v):
			int_type = k
			break
	return int_type

def get_cisco_int_type(intf):
	"""returns cisco interface type

	Args:
		intf (str): cisco interface

	Returns:
		str: interface type (FastEthernet, GigEthernet, etc..)
	"""	
	return interface_type(intf)[0].lower()


# -----------------------------------------------------------------------------

def standardize_mac(mac):
	"""removes . or : from mac address and make it a standard

	Args:
		mac (str): mac address

	Returns:
		str: standard format of mac address
	"""    	
	return mac.replace(":","").replace(".","").lower()

def mac_2digit_separated(mac):
	"""converts input mac to 2 digit separated mac format, separator=`:`

	Args:
		mac (str): mac address

	Returns:
		str: 2 digit separated format of mac address
	"""    	
	compact = standardize_mac(mac)
	if len(compact) != 12:
		return mac
	# Slice the string down into standard 2-character hexadecimal fields
	return ":".join(compact[i:i+2] for i in range(0, 12, 2))

def mac_4digit_separated(mac):
	"""converts input mac to 4 digit separated mac format, separator=`.`

	Args:
		mac (str): mac address

	Returns:
		str: 4 digit separated format of mac address
	"""    	
	compact = standardize_mac(mac)
	if len(compact) != 12:
		return mac
	# Slice the string down into standard 4-character hexadecimal fields
	return ".".join(compact[i:i+4] for i in range(0, 12, 4))

# ------------------------------------------------------------------------------

def get_string_part(line, begin, end):
	"""get the sub-string out of provided long string(line)

	Args:
		line (str): string line
		begin (int): sub-str start point
		end (int): sub-str end point

	Raises:
		TypeError: Raise error if input is invalid or sub-string falls outside

	Returns:
		str: sub-string
	"""    	
	try: return line[begin: end].strip()
	except: raise TypeError("Unrecognized Input")

def get_string_trailing(line, begin_at):
	"""get the training part of sub-string starting from provided index

	Args:
		line (str): string line
		begin_at (int): sub-str start point

	Raises:
		TypeError: Raise error if input is invalid or sub-string falls outside

	Returns:
		str: sub-string
	"""    	
	try: return line[begin_at:].strip()
	except: raise TypeError("Unrecognized Input")
# ------------------------------------------------------------------------------------
def remove_domain(hn):
	"""Removes domain suffix from provided hostname string

	Args:
		hn (str): fully qualified dns hostname

	Returns:
		str: hostname left by removing domain suffix
	"""
	return hn.split(".")[0]
# ------------------------------------------------------------------------------------

def get_device_manu(intf):
	"""returns device type from provided interface

	Args:
		intf (str): interface

	Returns:
		device type: manufacturer (cisco, juniper)
	"""	
	jit = get_juniper_int_type(intf)
	cit = get_cisco_int_type(intf)
	if jit.lower() == 'physical': return "juniper"
	if cit.lower() == 'physical': return "cisco"
	return ""

# -----------------------------------------------------------------------------

def time_stamp():
	"""current time stamp (for log purpose)

	Returns:
		str: current datetime string
	"""		
	return str(datetime.datetime.now())[:19]


# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------
