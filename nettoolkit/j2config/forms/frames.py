
from nettoolkit.nettoolkit.forms.formitems import *

# ===================================================================

def j2config_frame():
	"""tab display

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Configuration Generator', font='Bold', text_color="black") ],

		[sg.Text('Template file\t', text_color="black"), sg.InputText('', key='j2_file_template'), sg.FilesBrowse() ],
		[sg.Text('Data file\t\t', text_color="black"),     sg.InputText('', key='j2_file_data'),     sg.FilesBrowse() ],
		[sg.Text('Output Folder\t', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'j2_output_folder'), key='j2_output_folder', change_submits=True), 
		 sg.FolderBrowse() ],
		under_line(80),

		[sg.Text('Regional Data Excel [optional]', text_color="black"), 
		 sg.InputText(get_cache(CACHE_FILE, 'j2_file_regional'), key='j2_file_regional', change_submits=True), 
		 sg.FilesBrowse() ],
		[sg.Text('Custom Package Yaml file:\t  ', text_color="black"), 
	     sg.InputText(get_cache(CACHE_FILE, 'cit_file_custom_yml'), key='j2_file_custom_yml', change_submits=True,), 
	     sg.FileBrowse(button_color="grey"), ],
		under_line(80),

		# ------------------------------------------------------------------------------------
		[sg.Text('\t\t\t\t\t\t\t\t\t'),
		 sg.Button("Config Generate", change_submits=True, key='j2_btn_start', button_color="blue"),],

		])


J2CONFIG_FRAMES = {
	'Configuration Generation': j2config_frame(),
}