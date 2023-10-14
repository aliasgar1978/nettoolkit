
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
from abc import abstractclassmethod, abstractproperty

from nettoolkit.forms.formitems import *


# ---------------------------------------------------------------------------------------
# GLOBAL VARS
# ---------------------------------------------------------------------------------------
IPSCANNER_TABS = ['Subnet Scanner', 'Compare Scanner Outputs', 'Create Batch']
MINITOOLS_TABS = ['MD5 Calculate', 'P/W Enc/Dec', 'Prefix Operations', 'Juniper']
CAPTUREIT_TABS = ['cred', 'options', 'custom', 'Common']

# -----------------------------------------------------------------------------
# Class to Define a standard UserForm Template
# -----------------------------------------------------------------------------

class GuiTemplate():
	'''Minitools UserForm asking user inputs.	'''

	header = 'GuiTemplate: v0.1.0'

	# Object Initializer
	def __init__(self):
		self.tabs_dic = {}
		self.event_catchers = {}
		self.event_updaters = set()
		self.tab_updaters = set()
		self.retractables = set()
		self.standard_button_pallete_buttons()

	def __call__(self):
		self.create_form()


	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		layout = [
			banner(self.header), 
			self.button_pallete(),
			tabs_display(**self.tabs_dic),
		]

		self.w = sg.Window(self.header, layout, size=(800, 700), finalize=True)#, icon='data/sak.ico')
		# enable_disable(self, list(self.tabs_dic.keys()), [])
		btn_minitools_exec(self)
		while True:
			event, (i) = self.w.Read()

			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event in ('Cancel', sg.WIN_CLOSED) : 
				break
			if event in ('Clear',) : 
				self.clear_fields()
				pass
			if event in self.event_catchers:
				# ---------------------------------------------
				if event in self.event_updaters:
					success = self.event_catchers[event](self, i)	
				elif event in self.tab_updaters:
					success = self.event_catchers[event](self)	
				else:
					success = self.event_catchers[event](i)
				# ---------------------------------------------
				if not success:
					print("Mandatory inputs missing or incorrect.\tPlease verify inputs.")
				# ---------------------------------------------

			self.user_events(i, event)

		self.w.Close()

	@abstractclassmethod
	def user_events(self, i, event):
		pass

	@abstractproperty
	def cleanup_fields(self):
		return []

	def standard_button_pallete_buttons(self):
		"""get list of standard button pallete
		"""		
		self._button_pallete_buttons = [ 
			button_cancel("Cancel"),
			sg.Button("Clear", change_submits=True,size=(10, 1), key='Clear')
		]

	@property
	def button_pallete_buttons(self):
		return self._button_pallete_buttons

	def add_to_button_pallete_buttons(self, nbpb):
		"""add new buttons to button pallete

		Args:
			nbpb (list): list of additional buttons in pysimplegui format
		"""		
		self._button_pallete_buttons.extend(nbpb)


	def button_pallete(self):
		"""button pallete frame 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[self.button_pallete_buttons] ),]

	def event_update_element(self, **kwargs):
		"""update an element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def clear_fields(self):
		"""clear field values to null
		"""		
		for field in self.cleanup_fields:
			d = {field:{'value':''}}
			self.event_update_element(**d)

# ---------------------------------------------------------------------------------------

def enable_disable(obj, tabs_to_disable, tabs_to_enable):
	"""enable/disable provided object frames

	Args:
		obj (Nettoolkit): Nettoolkit class instance object
		tabs_to_disable (list): list of tabs to be disabled
		tabs_to_enable (list): list of tabs to be enabled
	"""	
	for tab in tabs_to_disable:
		d = {tab: {'visible':False}}
		obj.event_update_element(**d)	
	for i, tab in enumerate(tabs_to_enable):
		e = {tab: {'visible':True}}
		obj.event_update_element(**e)
		if i ==0: obj.w[tab].select()

# ---------------------------------------------------------------------------------------

def btn_ipscanner_exec(obj):
	"""executor function to switch and enable ipscanner tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	tabs_to_disable = MINITOOLS_TABS + CAPTUREIT_TABS
	enable_disable(obj, tabs_to_disable, IPSCANNER_TABS)
	return True

def btn_minitools_exec(obj):
	"""executor function to switch and enable minitools tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	tabs_to_disable = IPSCANNER_TABS + CAPTUREIT_TABS
	enable_disable(obj, tabs_to_disable, MINITOOLS_TABS)
	return True

def btn_captureit_exec(obj):
	"""executor function to switch and enable captureit tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	tabs_to_disable = IPSCANNER_TABS+ MINITOOLS_TABS
	enable_disable(obj, tabs_to_disable, CAPTUREIT_TABS)
	return True

# ---------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
