
# ---------------------------------------------------------------------------------------
#
from .forms.gui_template import GuiTemplate
from .forms.formitems import *


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
		self.event_catchers.update({v['key']: None for k, v in self.button_pallete_dic.items()})
		self.button_pallete_updaters = {v['key'] for k, v in self.button_pallete_dic.items()}

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
		for short_name, dic in self.button_pallete_dic.items():
			self.tabs_dic.update(dic['frames'])




# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
