
# ---------------------------------------------------------------------------------------
import nettoolkit as nt
from .gui import NGui

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
# Class to initiate Nettoolkit UserForm
# -----------------------------------------------------------------------------


class Nettoolkit(NGui):
	'''Minitools UserForm asking user inputs.	'''


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