

# ----------------------------------------------------------------------
# 1.1 Necessary Import 
#     Define necessary folder names
# ----------------------------------------------------------------------
from j2config import PrepareConfig
from pathlib import *
import sys

# --------------------------------------------
# path / folder settings
# --------------------------------------------
p = Path(".")
previous_path = p.resolve().parents[0]
sys.path.insert(len(sys.path), str(previous_path))
capture_folder   = str(previous_path.joinpath('captures'  ))
jtemplate_folder = str(previous_path.joinpath('jtemplates'))
output_folder    = str(previous_path.joinpath('j2-outputs'))


# ----------------------------------------------------------------------
# 1.2 Custom Project Import 
# ----------------------------------------------------------------------
# ## ------------------------------------------
# ## Load Custom project, modules
# ## Update as per your customer package
# ## ------------------------------------------
from custom_j2config.classes import Summaries, Block, Vrf, Vlan, Bgp, Physical
from custom_j2config import module1
from custom_j2config.regional import Region
# ## ------------------------------------------




# ------------------------------------------------------------------------------------------------------------------
# 1.3 DEFINE FUNCTIONS
# ------------------------------------------------------------------------------------------------------------------

# get the PrepareConfig Object
def prep_config(data_file, jtemplate_file, output_folder, regional_file, regional_class):
	PrCfg = PrepareConfig(data_file, jtemplate_file, output_folder, regional_file, regional_class)
	return PrCfg


# define all custom classes in a dictionary, add edit as necessary
def get_custom_classes():
	custom_classes = {
		'Summaries': Summaries, 
		'Block': Block, 
		'Vrf': Vrf,
		'Vlan': Vlan,
		'Bgp': Bgp, 
		'Physical': Physical,
	}
	return custom_classes

# Fork in custom classes to PrepareConfig Object
def exec_custom_modifications(PrCfg, custom_classes):
	custom_modules = {module1, }						       ## add more modules (if any loaded)
	PrCfg.custom_class_add_to_filter(**custom_classes)
	PrCfg.custom_module_methods_add_to_filter(*custom_modules)



# Main Function Execution flow.
def main(data_file, jtemplate_file, output_folder, regional_file=None, regional_class=None):

	# ------------------------------------------------------------------------------------------------------------------
	## 0. Start ------
	#
	print(f"Working on [{data_file}] using template [{jtemplate_file}]...", end='\t')

	# ------------------------------------------------------------------------------------------------------------------
	## 1. prepare config -----
	try:
		PrCfg = prep_config(data_file, jtemplate_file, output_folder, regional_file, regional_class)
		print(f"1...", end='\t')
	except Exception as e:
		print(f"ConfigGen Preparation Failed..\n {e}")
		return None

	# ------------------------------------------------------------------------------------------------------------------
	## 2. Add custom classes
	try:
		custom_classes = get_custom_classes()
		print(f"2...", end='\t')
	except Exception as e:
		print(f"Custom class Load Failed..\n Config Generation may give error if unfound necessary required class(es)")
		print(f"{e}")
	#
	try:
		exec_custom_modifications(PrCfg, custom_classes)
		print(f"3...", end='\t')
	except Exception as e:
		print(f"Custom class add Failed..\n Config Generation may give error if unfound necessary required class(es)")
		print(f"{e}")

	# ------------------------------------------------------------------------------------------------------------------
	## 3. start generating config
	try:
		PrCfg.start()
		print(f"4...", end='\t')
	except Exception as e:
		print(f"Configuration Generation Failed..\n")
		print(f"{e}")
		return None

	print("Configuration Generation Task Complete..")
	# ------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------
# 1.4 Executions
# ------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

	# ----- update inputs & execute main --------
	main(
		#
		# mandatory arguments: Excel database and Jinja Template files
		data_file=f'{capture_folder}/device_data-clean.xlsx',
		jtemplate_file=f'{jtemplate_folder}/jinja_template.j2',
		#
		## optional argument: output folder parth (default ".")
		output_folder=output_folder,
		#
		## optional arguments:  to override device var values. (use after necessary custom `Region` class imports)
		regional_file='regional_database.xlsx',
		regional_class=Region,
	)

# ------------------------------------------------------------------------------------------------------------------
