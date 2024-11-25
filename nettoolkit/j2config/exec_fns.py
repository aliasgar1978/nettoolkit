
# ====================================================================================

from nettoolkit.nettoolkit_common import read_yaml_mode_us, print_banner
from nettoolkit.j2config import PrepareConfig
from pathlib import *

# ====================================================================================

def get_host(file):
	return Path(file).stem.split("-clean")[0]

def get_custom_classes(custom):
	return {k: v for k, v in custom['j2_class_filters'].items() }

def get_custom_funcs(custom):
	return { v for k, v in custom['j2_functions_filters'].items() }

def exec_config_generation(
		data_files,
		template_file,
		output_folder,
		regional_file, 
		custom,
	):
	print_banner("Config Gen", 'green')
	try:
		regional_class = None
		custom = read_yaml_mode_us(custom)
		regional_class = custom['j2_regional']['regional_class']
	except Exception as e:
		raise Exception(f"Custom Yaml is mandatory for selection of item and hierarchical_orders")
	#
	for data_file in data_files:
		if not data_file.endswith(".xlsx"): continue
		device = get_host(data_file)
		print(f"Generating Configuration for {device}", end="\t")
		# try:
		if True:
			PrCfg = PrepareConfig(
				data_file=data_file,
				jtemplate_file=template_file,
				output_folder=output_folder,
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
		# except:
		# 	print(f"Failed..")

	print("Configuration Generation All Task(s) Complete..")

# ====================================================================================
