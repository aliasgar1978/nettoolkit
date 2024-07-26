
from nettoolkit.nettoolkit.forms.formitems import *
from pathlib import *
import sys


def get_classes(file):
	with open(file, 'r') as f:
		lines = f.readlines()
	classes = [ line.strip().split()[1].split("(")[0] 
				for line in lines
				if line.strip().startswith('class ') ]
	return classes

def get_variables(file):
	with open(file, 'r') as f:
		lines = f.readlines()
	v = []
	for line in lines:
		spl = line.split()
		if len(spl) > 2 and spl[1] == "=" :
			v.append(spl[0])
	return v


def custom_ff_file_cit_exec(obj, i):
	try:
		classes = get_classes(i['custom_ff_file_cit'])
		obj.event_update_element(custom_ff_class_name_cit={'values': classes})
		update_cache(CACHE_FILE, custom_facts_finder_pkg_module=i['custom_ff_file_cit'])
		return True
	except:
		return False


def custom_fk_file_cit_exec(obj, i):
	try:
		v = get_variables(i['custom_fk_file_cit'])
		obj.event_update_element(custom_fk_name_cit={'values': v})
		update_cache(CACHE_FILE, custom_facts_finder_foreign_key_module=i['custom_fk_file_cit'])
		return True
	except:
		return False

def custom_ff_name_cit_exec(obj, i):
	try:
		p = Path(i['custom_ff_file_cit'])
		previous_path = p.resolve().parents[1]
		sys.path.insert(len(sys.path), str(previous_path))
		file = p.name.replace(".py", "")
		s = f'from {p.parts[-2]}.{file} import {i["custom_ff_class_name_cit"]}'
		obj.event_update_element(custom_ff_class_str_cit={'value': s})
		exec(s)
		obj.custom_ff_class = eval(i["custom_ff_class_name_cit"])
		update_cache(CACHE_FILE, custom_facts_finder_module_class=i['custom_ff_class_name_cit'])
		return True
	except:
		return False

def custom_fk_name_cit_exec(obj, i):
	try:
		p = Path(i['custom_fk_file_cit'])
		previous_path = p.resolve().parents[1]
		sys.path.insert(len(sys.path), str(previous_path))
		file = p.name.replace(".py", "")
		s = f'from {p.parts[-2]}.{file} import {i["custom_fk_name_cit"]}'
		obj.event_update_element(custom_ff_class_str_cit={'value': s})
		exec(s)
		update_cache(CACHE_FILE, custom_facts_finder_module_foreign_keys=i['custom_fk_name_cit'])		
		if eval(f'isinstance({i["custom_fk_name_cit"]}, dict)'):
			obj.custom_fk = eval(i["custom_fk_name_cit"])
			return True
		else:
			sg.Popup("incorrect type, variable should be of dictionary type")			
			return False
	except:
		return False


def exec_ff_custom_cit_frame():
	"""tab display - Custom inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		

	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Generate Facts', font='Bold', text_color="black") ],

		[sg.Checkbox('clean file generate', key='generate_facts', default=False, text_color='black')],
		under_line(80),
		[sg.Text('Customize Facts', font='Bold', text_color="black") ],


		[sg.Text('custom facts-finder package file:', text_color='black'), 
		 sg.InputText(get_cache(CACHE_FILE, 'custom_facts_finder_pkg_module'), key='custom_ff_file_cit', change_submits=True, ), sg.FileBrowse(),
		],
		[sg.Text('custom facts-finder class from above package', text_color='black'), 
		 sg.InputCombo([], default_value=get_cache(CACHE_FILE, 'custom_facts_finder_module_class'), key='custom_ff_class_name_cit', size=(20,1), change_submits=True, ),
		], 
		[sg.Text('', key='custom_ff_class_str_cit', text_color='light yellow',),], 
		[sg.Text(''),], 
		[sg.Text('custom file having foreign keys dictionary:', text_color='black'), 
		 sg.InputText(get_cache(CACHE_FILE, 'custom_facts_finder_foreign_key_module'), key='custom_fk_file_cit', change_submits=True, ), sg.FileBrowse(),
		],
		[sg.Text('foreign key dictionary variable from above package', text_color='black'), 
		 sg.InputCombo([], default_value=get_cache(CACHE_FILE, 'custom_facts_finder_module_foreign_keys'), key='custom_fk_name_cit', size=(20,1), change_submits=True, ),
		], 
		[sg.Text('', key='custom_fk_str_cit', text_color='light yellow'),], 
		under_line(80),

		])
