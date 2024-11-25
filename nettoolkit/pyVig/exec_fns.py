

from nettoolkit.nettoolkit_common import read_yaml_mode_us, printmsg, print_banner
from nettoolkit.nettoolkit_db import write_to_xl, read_xl_all_sheet
from nettoolkit.pyVig import pyVig, CableMatrix


@printmsg(pre=f'Start Prepating Cable Matrix', post="Finish Preparing Cable Matrix..")
def exec_pyvig_cable_matrix(
		files,
		output_file,	        ## full path
		custom,                 ## custom yaml file.
		default_stencil=None,
		keep_all_cols=True,
	):
	#
	print_banner("Cable Matrix", 'magenta')
	#
	files = [file for file in files if file.endswith(".xlsx")]
	opd = {'sheet_filters': {}}
	#
	try:
		pyvig_custom = read_yaml_mode_us(custom)['pyvig'] 
	except Exception as e:
		raise Exception(f"Custom Yaml is mandatory for selection of item and hierarchical_orders")
	#
	CM = CableMatrix(files)
	CM.custom_attributes( default_stencil=default_stencil )
	CM.custom_functions(
	  hierarchical_order=pyvig_custom['custom_functions']['hierarchical_order'],
	  item=pyvig_custom['custom_functions']['item'],
	)
	CM.custom_var_functions(
	  ip_address=pyvig_custom['custom_var_functions']['ip_address'],
	)
	CM.run()
	CM.update(pyvig_custom['update']['sheet_filter_columns_add'])
	opd['sheet_filters'] = pyvig_custom['sheet_filter']['get_sheet_filter_columns'](CM.df_dict)
	opd['is_sheet_filter'] = True if opd['sheet_filters'] else False 
	#
	CM.calculate_cordinates(sheet_filter_dict=opd['sheet_filters'])
	CM.arrange_cablings(keep_all_cols=keep_all_cols)
	#
	opd['data_file'] = output_file
	write_to_xl(opd['data_file'], CM.df_dict, index=False, overwrite=True)
	#
	return opd


@printmsg(pre=f'Start Generating Visio', post=f'Finished Generating Visio')
def exec_pyvig_visio(
		data_file,				## excel cable matrix
		output_file,	        ## full path
		stencil_folder,
		custom,
		dic,
	):
	#
	print_banner("Visio Gen", 'magenta')
	dic['data_file'] = data_file
	dic['op_file'] = output_file
	dic['stencil_folder'] =  stencil_folder
	#
	try:
		pyvig_custom = read_yaml_mode_us(custom)['pyvig'] 
	except Exception as e:
		raise Exception(f"Custom Yaml is mandatory for selection of item and hierarchical_orders")
	#
	if not dic.get('sheet_filters'):
		dfd = read_xl_all_sheet(dic['data_file'])
		dic['sheet_filters'] = pyvig_custom['sheet_filter']['get_sheet_filter_columns'](dfd)
		dic['is_sheet_filter'] = True if dic['sheet_filters'] else False 
	dic['cols_to_merge'] = pyvig_custom['cols_to_merge']
	#
	pyVig(**dic)

