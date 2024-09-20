
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file, open_folder, printmsg
from nettoolkit.nettoolkit_db import write_to_xl, read_xl_all_sheet
from pathlib import *
import sys

from nettoolkit.pyVig import pyVig, CableMatrix

# ====================================================================================

#### -- cache updates -- ####
def update_cache_pyvig(i):
	update_cache(CACHE_FILE, cit_file_custom_yml=i['pv_file_custom_yml'])
	update_cache(CACHE_FILE, pv_folder_stencil=i['pv_folder_stencil'])
	update_cache(CACHE_FILE, pv_file_default_stencil=i['pv_file_default_stencil'])
	update_cache(CACHE_FILE, pv_folder_output=i['pv_folder_output'])
	update_cache(CACHE_FILE, pv_file_output_db=i['pv_file_output_db'])
	update_cache(CACHE_FILE, pv_file_output_visio=i['pv_file_output_visio'])
	update_cache(CACHE_FILE, pv_file_cable_matrix=i['pv_file_cable_matrix'])
	update_cache(CACHE_FILE, pv_file_output_file_visio=i['pv_file_output_file_visio'])

def update_keep_all_cols(obj, i):
	obj.event_update_element(pv_opt_keep_all_cols={'value': True})

def update_cm_cache_pyvig(obj, i):
	xlextension = "" if i['pv_file_output_db'].endswith(".xlsx") else ".xlsx" 
	visextension = "" if i['pv_file_output_visio'].endswith(".vsdx") else ".vsdx" 
	#
	op_db_file = i['pv_folder_output'] + "/" + i['pv_file_output_db'] + xlextension
	op_vis_file = i['pv_folder_output'] + "/" + i['pv_file_output_visio'] + visextension
	obj.event_update_element(pv_file_cable_matrix={'value': op_db_file})	
	obj.event_update_element(pv_file_output_file_visio={'value': op_vis_file})	
	update_cache_pyvig(i)

def exec_pv_folder_output_open(i):
	open_folder(i['pv_folder_output'])
def exec_pv_folder_stencil_open(i):
	open_folder(i['pv_folder_stencil'])
def exec_pv_file_default_stencil_open(i):
	open_folder(i['pv_file_default_stencil'])
def exec_pv_file_cable_matrix_open(i):
	open_folder(i['pv_file_cable_matrix'])
def exec_pv_file_output_file_visio_open(i):
	open_folder(i['pv_file_output_file_visio'])

def add_path(file):
	sys.path.insert(len(sys.path), str(Path(file).resolve().parents[0]))

def get_filename(file):
	return Path(file).stem

@printmsg(pre=f'Start Prepating Cable Matrix', post="Finish Preparing Cable Matrix..")
def pyvig_start_cm(obj, i):
	if i['pv_file_custom_yml']:
		add_path(i['pv_file_custom_yml'])
		custom =  read_yaml_mode_us(i['pv_file_custom_yml'])['pyvig'] 
	#
	files = [file for file in i['pv_files_clean_data'].split(";") if file.endswith(".xlsx")]
	default_stencil = get_filename(i['pv_file_default_stencil'])
	opd = {'sheet_filters': {}}
	CM = CableMatrix(files)
	CM.custom_attributes( default_stencil=default_stencil )
	CM.custom_functions(
	  hierarchical_order=custom['custom_functions']['hierarchical_order'],
	  item=custom['custom_functions']['item'],
	)
	CM.custom_var_functions(
	  ip_address=custom['custom_var_functions']['ip_address'],
	)
	CM.run()
	CM.update(custom['update']['sheet_filter_columns_add'])
	opd['sheet_filters'] = custom['sheet_filter']['get_sheet_filter_columns'](CM.df_dict)
	opd['is_sheet_filter'] = True if opd['sheet_filters'] else False 
	#
	CM.calculate_cordinates(sheet_filter_dict=opd['sheet_filters'])
	CM.arrange_cablings(keep_all_cols=i['pv_opt_keep_all_cols'])
	xlextension = "" if i['pv_file_output_db'].endswith(".xlsx") else ".xlsx" 
	opd['data_file'] = i['pv_folder_output'] + "/" + i['pv_file_output_db'] + xlextension
	write_to_xl(opd['data_file'], CM.df_dict, index=False, overwrite=True)
	obj.event_update_element(pv_file_cable_matrix={'value': opd['data_file']})	
	#
	return opd


@printmsg(pre=f'Start Generating Visio',
    post=f'Finished Generating Visio')
def prepare_visio_drawing(dic, i):
	visextension = "" if i['pv_file_output_visio'].endswith(".vsdx") else ".vsdx" 
	dic['op_file'] = str(Path(i['pv_folder_output'])) + "/" + i['pv_file_output_db'] + visextension
	dic['data_file'] = i['pv_file_cable_matrix']
	dic['stencil_folder'] =  i['pv_folder_stencil']
	#
	if i['pv_file_custom_yml']:
		add_path(i['pv_file_custom_yml'])
		custom =  read_yaml_mode_us(i['pv_file_custom_yml'])['pyvig'] 
		#
		if not dic.get('sheet_filters'):
			dfd = read_xl_all_sheet(dic['data_file'])
			dic['sheet_filters'] = custom['sheet_filter']['get_sheet_filter_columns'](dfd)
			dic['is_sheet_filter'] = True if dic['sheet_filters'] else False 
		dic['cols_to_merge'] = custom['cols_to_merge']
	#
	pyVig(**dic)


def pyvig_start_visio(obj, i):
	update_keep_all_cols(obj, i)
	dic = {}
	prepare_visio_drawing(dic, i)

def pv_start_cm_visio(obj, i):
	update_keep_all_cols(obj, i)
	dic = pyvig_start_cm(obj, i)
	prepare_visio_drawing(dic, i)

# ======================================================================================

PYVIG_EVENT_FUNCS = {
	'pv_btn_start_cm': pyvig_start_cm,
	'pv_btn_start_visio': pyvig_start_visio,
	'pv_btn_start_cm_visio': pv_start_cm_visio,
	'pv_file_custom_yml': update_cache_pyvig,
	'pv_folder_stencil': update_cache_pyvig,
	'pv_file_default_stencil': update_cache_pyvig,
	'pv_file_cable_matrix': update_cache_pyvig,
	'pv_file_output_file_visio': update_cache_pyvig,

	'pv_folder_output': update_cm_cache_pyvig,
	'pv_file_output_db': update_cm_cache_pyvig,
	'pv_file_output_visio': update_cm_cache_pyvig,

	'pv_folder_output_open': exec_pv_folder_output_open,
	'pv_folder_stencil_open': exec_pv_folder_stencil_open,
	'pv_file_default_stencil_open': exec_pv_file_default_stencil_open,
	'pv_file_cable_matrix_open': exec_pv_file_cable_matrix_open, 
	'pv_file_output_file_visio_open': exec_pv_file_output_file_visio_open,

}
PYVIG_EVENT_UPDATERS = {
	'pv_folder_output', 'pv_file_output_db', 'pv_file_output_visio',
	'pv_btn_start_cm', 'pv_btn_start_visio', 'pv_btn_start_cm_visio',
}
PYVIG_ITEM_UPDATERS = set()

PYVIG_RETRACTABLES = {
	'pv_files_clean_data', 'pv_folder_stencil', 'pv_file_default_stencil', 
}

