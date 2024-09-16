
# ---------------------------------------------------------------------------------------
try:
	import PySimpleGUI as sg
except:
	pass

from abc import abstractclassmethod
from dataclasses import dataclass, field
import nettoolkit as nt
#
from .forms.gui_template import GuiTemplate
from .forms.formitems import *

### -- Imports For Nettoolkit() class

from nettoolkit.capture_it.forms.frames   import CAPTUREIT_FRAMES
from nettoolkit.facts_finder.forms.frames import FACTSFINDER_FRAMES
from nettoolkit.j2config.forms.frames     import J2CONFIG_FRAMES
from nettoolkit.pyVig.forms.frames        import PYVIG_FRAMES
from nettoolkit.configure.forms.frames    import CONFIGURE_FRAMES
from nettoolkit.addressing.forms.frames   import ADDRESSING_FRAMES
from nettoolkit.pyJuniper.forms.frames    import JUNIPER_FRAMES
from nettoolkit.pyNetCrypt.forms.frames   import CRYPT_FRAMES
from .forms.nt_variables import (
	EVENT_UPDATORS, EVENT_ITEM_UPDATORS, RETRACTABLES, EVENT_FUNCTIONS, FRAMES, BUTTUN_PALLETE_DICT
)



# ---------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Generalized Class to Prepare GUI UserForm using template 
# -----------------------------------------------------------------------------

class NGui(GuiTemplate):

	def __init__(self, * ,
		header="Set Your private Header",
		banner="Set Your private Banner",
		form_width=1440,
		form_height=700,
		frames_dict={},
		event_catchers={},
		event_updaters=set(),
		event_item_updaters=set(),
		retractables=set(),
		button_pallete_dic={},
		):
		super().__init__(
			header, banner, form_width, form_height,
			frames_dict, event_catchers, event_updaters, 
			event_item_updaters, retractables, button_pallete_dic,
		)
		self.button_pallete_updaters = set(self.button_pallete_dic.values())
		self._buttonpallet_to_frames_map = {}

	def __call__(self, initial_frame=None):
		if not self.tabs_dic: self.collate_frames()
		super().__call__(initial_frame) 

	def update_set(self, name, value):
		if self.__dict__.get(name): 
			self.__dict__[name] = self.__dict__[name].union(value)
		else:
			self.__dict__[name] = value


	def update_dict(self, name, value):
		if self.__dict__.get(name): 
			self.__dict__[name].update(value)
		else:
			self.__dict__[name] = value

	@property
	def cleanup_fields(self):
		return self.retractables

	def collate_frames(self):
		for btn, dic in self.buttonpallet_to_frames_map.items():
			self.tabs_dic.update(dic['frames'])

	@property
	def buttonpallet_to_frames_map(self):
		return self._buttonpallet_to_frames_map

	@buttonpallet_to_frames_map.setter
	def buttonpallet_to_frames_map(self, dic):
		self._buttonpallet_to_frames_map.update(dic)

# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 

# -----------------------------------------------------------------------------
# Class to initiate Nettoolkit UserForm
# -----------------------------------------------------------------------------


class Nettoolkit(NGui):
	'''Minitools UserForm asking user inputs.	'''


	bp_to_frames_map = {
		'crypt':      {'button_name': 'btn_cryptology', 'frames': CRYPT_FRAMES,     },
		'juniper':    {'button_name': 'btn_juniper' ,   'frames': JUNIPER_FRAMES    },
		'addressing': {'button_name': 'btn_addressing', 'frames': ADDRESSING_FRAMES },
		'captureit':  {'button_name': 'btn_captureit',  'frames': CAPTUREIT_FRAMES  },
		'factsgen':   {'button_name': 'btn_factsfinder','frames': FACTSFINDER_FRAMES},
		'configure':  {'button_name': 'btn_configure',  'frames': CONFIGURE_FRAMES  },
		'j2config':   {'button_name': 'btn_j2config',   'frames': J2CONFIG_FRAMES   },
		'pyvig':      {'button_name': 'btn_pyvig',      'frames': PYVIG_FRAMES      },
	}


	# Object Initializer
	def __init__(self):
		banner = f'Nettoolkit: v{nt.__version__}'
		header = f'{nt.__doc__}'
		#
		self.initialize_custom_variables()
		self.NG = NGui(
			header              = header,
			banner              = banner,
			event_updaters      = EVENT_UPDATORS,
			event_item_updaters = EVENT_ITEM_UPDATORS,
			retractables        = RETRACTABLES,
			event_catchers      = EVENT_FUNCTIONS,
			button_pallete_dic  = BUTTUN_PALLETE_DICT,
			form_width          = 820,
			form_height         = 740,
		)	
		self.NG.buttonpallet_to_frames_map = self.bp_to_frames_map

	def __call__(self, initial_frame=None):
		self.NG(initial_frame)

	def initialize_custom_variables(self):
		"""Initialize all custom variables
		"""		
		self.custom_dynamic_cmd_class = None      # custom dynamic commands execution class
		self.custom_ff_class = None  # custom facts-finder class
		self.custom_fk = {}          # custom facts-finder foreign keys

	def user_events(self, i, event):
		"""specific event catchers

		Args:
			i (dict): dictionary of GUI fields variables
			event (str): event
		"""		
		pass

# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 


# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
