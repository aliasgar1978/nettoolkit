""" creates ping script xxxx.bat file for ping test during / after cr
provide prefixes and names of prefixes to it. 
"""

import nettoolkit as nt
import PySimpleGUI as sg
from pprint import pprint

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class CreateBatch():
	'''Inititates a UserForm asking user inputs.	'''

	header = 'batch file generator'
	version = 'v1.0.0'

	# Object Initializer
	def __init__(self):
		self.dic = {
			# mandatories
			'pfxs':[],
			'names':[],
			'ips':(),
		}
		self.op_folder = '.'
		self.create_form()

	def banner(self):
		"""Banner / Texts with bold center aligned fonts

		Returns:
			list: list with banner text
		"""    		
		return [sg.Text(self.version, font='arialBold', justification='center', size=(768,1))] 

	def tabs(self, **kwargs):
		"""create tab groups for provided kwargs

		Returns:
			sg.TabGroup: Tab groups
		"""    		
		tabs = []
		for k, v in kwargs.items():
			tabs.append( sg.Tab(k, [[v]]) )
		return sg.TabGroup( [tabs] )

	def button_ok(self, text, **kwargs):  
		"""Insert an OK button of regular size. provide additional formating as kwargs.

		Args:
			text (str): Text instead of OK to display (if need)

		Returns:
			sg.OK: OK button
		"""		
		return sg.OK(text, size=(10,1), **kwargs)	
	def button_cancel(self, text, **kwargs):
		"""Insert a Cancel button of regular size. provide additional formating as kwargs.

		Args:
			text (str): Text instead of Cancel to display (if need)

		Returns:
			sg.Cancel: Cancel button
		"""    	  
		return sg.Cancel(text, size=(10,1), **kwargs)

	def button_pallete(self):
		"""button pallete containing standard OK  and Cancel buttons 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[
			[self.button_ok("Go", bind_return_key=True), self.button_cancel("Cancel"),],
		] ), ]

	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		self.tabs()
		layout = [
			self.banner(), 
			self.button_pallete(),
			self.tabs_display(),
		]
		self.w = sg.Window(self.header, layout, size=(700,500))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()
			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event == 'Cancel': 
				# del(self.dic)
				break
			if event == 'Go': 
				# update self.dic
				for k in self.dic:
					self.dic[k] = self.get_list(i[k])
				self.op_folder = i['op_folder']
				break
		self.w.Close()
		for ip in self.dic['ips']:
			create_batch_file(self.dic['pfxs'], self.dic['names'], ip, self.op_folder)

	@staticmethod
	def get_list(raw_items):
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

	def tabs_display(self):
		"""define tabs display

		Returns:
			list: list of tabs
		"""    		
		tabs_dic = {
			'prefixes': self.select_prefixes(),
			'names': self.select_names(),
			'ips': self.select_ips(),
			'op_path': self.select_file_path(),

		}
		return [self.tabs(**tabs_dic),]


	def select_file_path(self):
		"""input output files 

		Returns:
			sg.Frame: Frame with input data components
		"""    		
		return sg.Frame(title='Output Files Path', 
						title_color='red', 
						# size=(500, 4), 
						key='op_path',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text('select folder where op files to be generated :', size=(20, 1), text_color="blue"), 
				sg.InputText('', key='op_folder'),  
				sg.FolderBrowse(),
			],
			])


	def select_prefixes(self):
		"""selection of filters tab display

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title='list of Prefixes', 
						title_color='blue', 
						# size=(500, 4), 
						key='list_of_prefixes',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text("Provide Prefixes - line/comma separated")],
			[sg.Multiline("", key='pfxs', autoscroll=True, size=(30,20), disabled=False) ],
			[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],

			])

	def select_names(self):
		"""selection of filters tab display

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title='list of Names', 
						title_color='blue', 
						# size=(500, 4), 
						key='list_of_names',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text("Provide Prefix Names - line/comma separated")],
			[sg.Multiline("", key='names', autoscroll=True, size=(40,20), disabled=False) ],
			[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],

			])

	def select_ips(self):
		"""selection of filters tab display

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title='list of IPs', 
						title_color='blue', 
						# size=(500, 4), 
						key='list_of_ips',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text("Provide ips - line/comma separated")],
			[sg.Multiline("", key='ips', autoscroll=True, size=(10,5), disabled=False) ]

			])


# ------------------------------------
def create_batch_file(pfxs, names, ip, op_folder):
	if not isinstance(ip, int):
		try:
			ip = int(ip)
		except:
			s = f"wrong ip detected .{ip}, will be skipped"
			sg.Popup(s)
			print(s)
			return None
	op_batch_filename = f"{op_folder}/ping_test-ips-.{ip}.bat"  
	#
	if not isinstance(pfxs, (list, tuple)):
		s = f'Wrong type of prefix list \n{pfxs}, \ncould not proceed, check inputs\nExpected <class "list"> or <class "tuple">, got {type(pfxs)}\n'
		sg.Popup(s)
		print(s)
		return None
	if not isinstance(names, (list, tuple)):
		s = f'Wrong type of name list \n{names}, \ncould not proceed, check inputs\nExpected <class "list"> or <class "tuple">, got {type(names)}\n'
		sg.Popup(s)
		print(s)
		return None
	if len(pfxs) != len(names):
		s = "length of prefixes mismatch with length of names. both should be of same length \ncould not proceed, check inputs"
		sg.Popup(s)
		print(s)
		return None
	#
	# ------------------------------------
	list_of_ips = add_ips_to_lists(pfxs, ip)
	s = create_batch_file_string(list_of_ips, names)
	write_out_batch_file(op_batch_filename, s)
	# ------------------------------------

def add_ips_to_lists(pfxs, n):
	list_of_1_ips = []
	for pfx in pfxs:
		subnet = nt.addressing(pfx)
		try:
			ip1 = subnet[n]
			list_of_1_ips.append(ip1)
		except:
			pass
	return list_of_1_ips

def create_batch_file_string(lst, names):
	s = ''
	for ip, name in zip(lst, names):
		s += f'start "{name}" ping -t {ip}\n'
	return s


def write_out_batch_file(op_batch_filename, s):
	with open(op_batch_filename, 'w') as f:
		f.write(s)

# ------------------------------------

if __name__ == '__main__':
	# ------------------------------------
	# TEST
	# ------------------------------------
	u = CreateBatch()
	del(u)

