
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file, open_folder, open_excel_file
from pathlib import *
import sys

from nettoolkit.j2config import PrepareConfig
from nettoolkit.j2config.general import get_model_template_version


# ====================================================================================

#### -- cache updates -- ####
def update_cache_j2(i):
	update_cache(CACHE_FILE, cit_file_custom_yml=i['j2_file_custom_yml'])
	update_cache(CACHE_FILE, j2_file_regional=i['j2_file_regional'])	
	update_cache(CACHE_FILE, j2_output_folder=i['j2_output_folder'])	
	update_cache(CACHE_FILE, j2_file_template=i['j2_file_template'])	
	update_cache(CACHE_FILE, j2_file_data=i['j2_file_data'])	

def exec_j2_file_regional_open(i):
	open_excel_file(i['j2_file_regional'])
def exec_j2_folder_output_open(i):
	open_folder(i['j2_output_folder'])
def exec_j2_file_data_open(i):
	open_excel_file(i['j2_file_data'])
def exec_j2_file_template_open(i):
	open_text_file(i['j2_file_template'])
def exec_j2_files_output_open(i):
	for file in i['j2_output_files'].split(";"):
		open_text_file(file)

def get_host(file):
	return Path(file).stem.split("-clean")[0]

def add_path(file):
	sys.path.insert(len(sys.path), str(Path(file).resolve().parents[0]))


def get_custom_classes(custom):
	return {k: v for k, v in custom['j2_class_filters'].items() }

def get_custom_funcs(custom):
	return { v for k, v in custom['j2_functions_filters'].items() }


def j2config_start(obj, i):
	if i['j2_file_custom_yml']:
		add_path(i['j2_file_custom_yml'])
		custom =  read_yaml_mode_us(i['j2_file_custom_yml']) 
	#
	regional_file = i['j2_file_regional'] if i['j2_file_regional'] else None
	regional_class = custom['j2_regional']['regional_class'] if i['j2_file_custom_yml'] else None
	#
	for data_file in i['j2_file_data'].split(";"):
		if not data_file.endswith(".xlsx"): continue
		device = get_host(data_file)
		print(f"Generating Configuration for {device}", end="\t")
		try:
			PrCfg = PrepareConfig(
				data_file=data_file,
				jtemplate_file=i['j2_file_template'],
				output_folder=i['j2_output_folder'],
				regional_file=regional_file,
				regional_class=regional_class,
			)
			custom_classes = get_custom_classes(custom)
			custom_funcs = get_custom_funcs(custom)
			#
			PrCfg.custom_class_add_to_filter(**custom_classes)
			PrCfg.custom_module_methods_add_to_filter(*custom_funcs)
			#
			PrCfg.start()
			print(f"Done..")
		except:
			print(f"Failed..")

	update_output_files(obj, i)

	print("Configuration Generation All Task(s) Complete..")


def update_output_files(obj, i):
	update_cache_j2(i)
	model, template_ver = get_model_template_version(i['j2_file_template'])
	files = ";".join( 
		[f"{i['j2_output_folder']}/{get_host(file)}-{model}-{template_ver}-j2Gen.cfg"
		 for file in i['j2_file_data'].split(";")
	])
	obj.event_update_element(j2_output_files={'value': files})


# ======================================================================================

J2CONFIG_EVENT_FUNCS = {
	'j2_btn_start': j2config_start,
	'j2_file_custom_yml': update_cache_j2,
	'j2_file_regional': update_cache_j2,
	'j2_file_data': update_cache_j2,
	'j2_file_template': update_cache_j2,
	'j2_output_folder': update_cache_j2,

	'j2_file_template_open': exec_j2_file_template_open,
	'j2_file_data_open': exec_j2_file_data_open,
	'j2_folder_output_open': exec_j2_folder_output_open,
	'j2_file_regional_open': exec_j2_file_regional_open,
	'j2_files_output_open': exec_j2_files_output_open,
}
J2CONFIG_EVENT_UPDATERS = {
	'j2_btn_start'
}
J2CONFIG_ITEM_UPDATERS = set()

J2CONFIG_RETRACTABLES = {
	'j2_file_template', 'j2_file_data', 
}

