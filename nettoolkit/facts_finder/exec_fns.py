

# ====================================================================================

from nettoolkit.nettoolkit_common import read_yaml_mode_us, print_banner
from nettoolkit.facts_finder import CleanFacts, rearrange_tables
from pathlib import *

# ====================================================================================


def get_host(log_file):
	return Path(log_file).stem

def exec_facts_finder(
	log_files,
	custom=None,
	convert_to_cit=True,
	remove_cit_bkp=True,
	skip_txtfsm=True,
	new_suffix='-clean',
	use_cdp=False,
	debug=False,
	):
	print_banner("Excel Facts", 'yellow')
	if custom:	
		custom =  read_yaml_mode_us(custom)['facts_finder']
	else:
		custom = None
	#
	for log_file in log_files:
		if not log_file.endswith(".log"): continue
		device = get_host(log_file)
		print(">> starting", device, "...", end='\t')
		#
		try:
			cleaned_fact = CleanFacts(
				capture_log_file=log_file,
				convert_to_cit=convert_to_cit,
				remove_cit_bkp=remove_cit_bkp,
				skip_txtfsm=skip_txtfsm,
				new_suffix=new_suffix,
				use_cdp=use_cdp,
				debug=debug,
			)
			cleaned_fact()
			print(f"Cleaning done...,", end='\t')
		except Exception as e:
			print(f"Cleaning failed...,")
			print(e)
			continue
		#
		try:
			if custom:
				ADF = custom['CustomDeviceFactsClass'](cleaned_fact, aggregation=False)
				ADF()
				ADF.write()
				print(f"Custom Data Modifications done...,", end='\t')
		except Exception as e:
			print(f"Custom Data Modifications failed...,")
			print(e)
		#
		try:
			foreign_keys = custom['foreign_keys'] if custom else {}
			rearrange_tables(cleaned_fact.clean_file, foreign_keys=foreign_keys)
			print(f"Column Rearranged done..., ", end='\t')
		except Exception as e:
			print(f"Column Rearrange failed...,")
			print(e)
		print(f"Tasks Completed !! {device} !!")


	print("Facts-Finder All Task(s) Complete..")

# ====================================================================================
