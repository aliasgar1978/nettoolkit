
# ---------------------------------------------------------------------------------------
sg = None
try:
	import PySimpleGUI as sg
except:
	pass
import pandas as pd
from pathlib import *
import nettoolkit.nettoolkit.forms as frm

# ---------------------------------------------------------------------------------------
formpath_str = str(frm).split('from')[-1].split(">")[0].strip()[1:-1]
p = Path(formpath_str)
previous_path = p.resolve().parents[0]
CACHE_FILE = previous_path.joinpath('caches.xlsx')
CONNECTOR_TYPES_FILE = previous_path.joinpath('cable_n_connectors.xlsx')


# ------------------------------------------------------------------------
def popupmsg(pre=None, *, post=None,):
	"""Decorator to provide pre/post custom popup message to a function

	Args:
		pre (str, optional): Popup Message to display before function execution. Defaults to None.
		post (str, optional): Popup Message to display after function execution. Defaults to None.
	"""    	
	def outer(func):
		def inner(*args, **kwargs):
			if pre: 
				sg.Popup(pre)
			#
			fo = func(*args, **kwargs)
			#
			if post: 
				sg.Popup(post)
			return fo
		return inner
	return outer

# ---------------------------------------------------------------------------------------

def blank_line(): 
	"""to insert a blank row

	Returns:
		list: blank row
	"""		
	return [sg.Text(''),]

def item_line(item, length):
	"""to draw a line with provided character or repeat a character for n-number of time

	Args:
		item (str): character
		length (int): to repeat the character

	Returns:
		list: list with repeated item Text
	"""    	
	return [sg.Text(item*length)]

def under_line(length): 
	"""To draw a line

	Args:
		length (int): character length of line

	Returns:
		list: underline row
	"""		
	return [sg.Text('_'*length)]

def banner(version):
	"""Banner / Texts with bold center aligned fonts

	Args:
		version (str): version of code

	Returns:
		list: list with banner text
	"""    		
	return [sg.Text(version, font='arialBold', justification='center', size=(768,1))] 


def footer(version, width):
	"""Footer Credit text

	Args:
		version (str): gui template version
		width (_type_): width of window

	Returns:
		list: list with footer text
	"""    	
	return [sg.Text(f"Prepared using Nettoolkit NGUI {version}", justification='right', size=(width, 1))]

def tabs(**kwargs):
	"""create tab groups for provided kwargs

	Returns:
		sg.TabGroup: Tab groups
	"""    		
	tabs = []
	for k, v in kwargs.items():
		tabs.append( sg.Tab(k, [[v]]) )
	return sg.TabGroup( [tabs] )


def button_ok(text, **kwargs):  
	"""Insert an OK button of regular size. provide additional formating as kwargs.

	Args:
		text (str): Text instead of OK to display (if need)

	Returns:
		sg.OK: OK button
	"""		
	return sg.OK(text, size=(10,1), **kwargs)	

def button_cancel(text, **kwargs):
	"""Insert a Cancel button of regular size. provide additional formating as kwargs.

	Args:
		text (str): Text instead of Cancel to display (if need)

	Returns:
		sg.Cancel: Cancel button
	"""    	  
	return sg.Cancel(text, size=(10,1), **kwargs)

def button_pallete():
	"""button pallete containing standard OK  and Cancel buttons 

	Returns:
		list: list with sg.Frame containing buttons
	"""    		
	return [sg.Frame(title='Button Pallete', 
			title_color='blue', 
			relief=sg.RELIEF_RIDGE, 
			layout=[
		[button_ok("Go", bind_return_key=True), button_cancel("Cancel"),],
	] ), ]

def get_list(raw_items):
	"""create list from given raw items splits by enter and comma

	Args:
		raw_items (str): multiline raw items

	Returns:
		list: list of items
	"""	
	ri_lst = raw_items.split("\n")
	lst = []
	for i, item in enumerate(ri_lst):
		if item.strip().endswith(","):
			ri_lst[i] = item[:-1]
	for ri_item in ri_lst:
		lst.extend(ri_item.split(","))
	for i, item in enumerate(lst):
		lst[i] = item.strip()		
	return lst

def tabs_display(**tabs_dic):
	"""define tabs display

	Returns:
		list: list of tabs
	"""    		
	return [tabs(**tabs_dic),]

# ---------------------------------------------------------------------------------------

def update_cache(cache_file, **kwargs):
	"""add/update cache item/value

	Args:
		cache_file (str): cache file name with full path
	"""		
	#
	df = pd.read_excel(cache_file).fillna("")
	dic = df.to_dict()
	#
	for input_key, input_value in kwargs.items():
		prev_value = ""
		prev_value_idx = None
		if input_key in dic['VARIABLE'].values():
			for (vrk, vr), (vlk, vl) in zip(dic['VARIABLE'].items(), dic['VALUE'].items()):
				if vr == input_key:
					prev_value_idx = vlk
					prev_value = vl
		v = input_value or prev_value
		if not prev_value or v != prev_value:
			if prev_value_idx is None:
				try:
					prev_value_idx = max(dic['VARIABLE'].keys())+1
				except:
					prev_value_idx = 0
			dic['VARIABLE'][prev_value_idx] = input_key
			dic['VALUE'][prev_value_idx] = v
	ndf = pd.DataFrame(dic, columns=['VARIABLE', 'VALUE'])
	ndf.to_excel(cache_file, index=False)


def get_cache(cache_file, key):
	"""retrive the value for provided key(item) from cache file

	Args:
		cache_file (str): cache file name with full path
		key (str): name of item

	Returns:
		str: matched item value from cache file
	"""	
	#
	try:
		df = pd.read_excel(cache_file).fillna("")
	except FileNotFoundError:
		df = pd.DataFrame({'VARIABLE': [], 'VALUE':[]})
		df.to_excel(cache_file, index=False)
	dic = df.to_dict()
	#
	for vrk, vr in dic['VARIABLE'].items():
		if key == vr:
			return dic['VALUE'][vrk]
	#
	return ""
# ---------------------------------------------------------------------------------------


def get_cable_n_connectors(file, column, item):
	"""retrive the value for provided item for given column

	Args:
		file (str): cached cable and connector file name with full path
		column (str): column name (attribute)
		item (str): row item (connector type)

	Returns:
		str: matched item value from cached file
	"""	
	try:
		df = pd.read_excel(file).fillna("")
	except FileNotFoundError:
		df = pd.DataFrame({'media_type': [], 'cable_type':[], '_connector_type':[], 'speed':[] })
		df.to_excel(file, index=False)
	dic = df.to_dict()
	#
	for vrk, vr in dic['media_type'].items():
		if item.lower() == vr.lower():
			return dic[column][vrk]
	#
	return ""

def add_cable_n_connectors(file, **kwargs):
	"""add item/value

	Args:
		file (str): cached cable and connector excel file name with full path
	"""		
	#
	df = pd.read_excel(file).fillna("")
	df2 = pd.DataFrame(kwargs)
	df = pd.concat([df, df2], ignore_index=True).fillna("")
	df.to_excel(file, index=False)

# ---------------------------------------------------------------------------------------

