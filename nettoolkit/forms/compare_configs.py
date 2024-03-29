
import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from nettoolkit_common import IO
from compare_it import *


def compare_config_texts_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['compare_config_file1'] != '' and i['compare_config_file2'] != '':
			text_diff(i['compare_config_file1'], i['compare_config_file2'], i['op_folder_compare_config_text'])
			sg.Popup("Success!")
			return True
	except Exception as e:
		sg.Popup('Failure!')
		return None


def compare_config_xl_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['compare_config_file3'] != '' and i['compare_config_file4'] != '':
			xl_diff(i['compare_config_file3'], i['compare_config_file4'], i['op_folder_compare_xl'],
				i['compare_config_tab_name'], i['compare_config_index_col'])
			sg.Popup("Success!")
			return True
	except Exception as e:
		sg.Popup('Failure!')
		return None


def compare_config_texts_frame():
	"""tab display - Compares two configuration output

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('compare text files (cisco/juniper)', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Select first file (text file only):',  text_color="yellow"), 
			sg.InputText(key='compare_config_file1'),  
			sg.FileBrowse()],

		[sg.Text('Select second file (text file only):',  text_color="yellow"), 
			sg.InputText(key='compare_config_file2'), 
			sg.FileBrowse()],

		[sg.Text('output folder:', text_color="yellow"), 
			sg.InputText('', key='op_folder_compare_config_text'),  
			sg.FolderBrowse(),
		],

		[sg.Button("Start", change_submits=True, key='go_compare_config_text')],
		under_line(80),

		# -----------------------------------------------------------------------------

		[sg.Text('compare excel files ', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('Select first file (excel file only):',  text_color="yellow"), 
			sg.InputText(key='compare_config_file3'),  
			sg.FileBrowse()],

		[sg.Text('Select second file (excel file only):',  text_color="yellow"), 
			sg.InputText(key='compare_config_file4'), 
			sg.FileBrowse()],

		[sg.Text('output folder:', text_color="yellow"), 
			sg.InputText('', key='op_folder_compare_xl'),  
			sg.FolderBrowse(),
		],

		[sg.Text('tab name:',  text_color="yellow"), 
			sg.InputText(key='compare_config_tab_name'),],
		[sg.Text('index column nmae:',  text_color="yellow"), 
			sg.InputText(key='compare_config_index_col'),],


		[sg.Button("Start", change_submits=True, key='go_compare_config_xl')],
		under_line(80),

		])




def text_diff(f1, f2, output_folder):
	output_file = output_folder+"/compare-text.op.txt"
	diff = {}
	removals = CompareText(f1, f2, "- ")
	adds = CompareText(f2, f1, "+ ")
	diff['removed'] = removals.CTObj.diff
	diff['adds'] = adds.CTObj.diff

	difference_dict_labels = {'adds': "ADDITIONS", 'removed': "REMOVES" }   # arbitrary Header
	diff_str = get_string_diffs(diff,
	        hn='HEADER [hostname]',                                         # provide arbitrary hostname
	        difference_dict_labels=difference_dict_labels
	        )

	IO.to_file(output_file, matter=diff_str)
	return diff_str


def xl_diff(f1, f2, output_folder, sheet_name, index_col):
	output_file = output_folder+"/compare-xl.op.txt"

	diff = {}
	removals = CompareExcelData(f1, f2, sheet_name, "- ")   # removals from file1
	adds = CompareExcelData(f1, f2, sheet_name, "+ ")       # adds to file 2
	remove_diff = removals.diff(index_col)
	add_diff = adds.diff(index_col)
	removals_str = get_string_diffs(remove_diff, "")
	adds_str = get_string_diffs(add_diff, "")
	diff_str = removals_str +'\n\n'+ adds_str

	IO.to_file(output_file, matter=diff_str)
	return diff_str
