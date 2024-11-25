
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import read_yaml_mode_us, create_folders, open_text_file, print_banner
from pathlib import *
import sys

import nettoolkit.facts_finder as ff
from nettoolkit.facts_finder import CleanFacts, rearrange_tables
from nettoolkit.yaml_facts import YamlFacts

# ====================================================================================

#### -- cache updates -- ####
def update_cache_ff(i):
	update_cache(CACHE_FILE, cit_file_custom_yml=i['ff_file_custom_yml'])
	update_cache(CACHE_FILE, yf_output_folder=i['yf_output_folder'])

def add_path(file):
	sys.path.insert(len(sys.path), str(Path(file).resolve().parents[0]))


def get_host(log_file):
	return Path(log_file).stem


@activity_finish_popup
def facts_finder_start(i):
	if i['ff_file_custom_yml']:
		add_path(i['ff_file_custom_yml'])
		custom =  read_yaml_mode_us(i['ff_file_custom_yml'])['facts_finder'] 
	else:
		custom = None
	print_banner("Excel Facts", 'yellow')
	for log_file in i['ff_log_files'].split(";"):
		if not log_file.endswith(".log"): continue
		device = get_host(log_file)
		print(">> starting", device, "...", end='\t')
		#
		try:
			cleaned_fact = CleanFacts(
				capture_log_file=log_file,
				convert_to_cit=i['ff_convert_to_cit'],
				remove_cit_bkp=i['ff_remove_cit_bkp'],
				skip_txtfsm=i['ff_skip_txtfsm'],
				new_suffix=i['ff_new_suffix'],
				use_cdp=False,
				debug=False,
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


@activity_finish_popup
def yaml_facts_start(i):
	print_banner("Yaml Facts", 'yellow')
	for log_file in i['ff_log_files'].split(";"):
		if not log_file.endswith(".log"): continue
		device = get_host(log_file)
		print(">> starting", device, "...", end='\t')
		#
		try:
			YF = YamlFacts(log_file, i['yf_output_folder'])
			print(f"Yaml File Generation done...,", end='\t')
			print(f"Tasks Completed !! {device} !!")
			if YF.unavailable_cmds:
				print(f"\t{device}: Missing Captures {YF.unavailable_cmds}")

		except Exception as e:
			print(f"Yaml File Generation failed...")
			print(e)
			continue
		#
	print("Yaml Facts-Finder All Task(s) Complete..")


# ======================================================================================

FACTSFINDER_EVENT_FUNCS = {
	'ff_btn_start': facts_finder_start,
	'yf_btn_start': yaml_facts_start,
	'ff_file_custom_yml': update_cache_ff,
	'yf_output_folder': update_cache_ff,
}
FACTSFINDER_EVENT_UPDATERS = set()
FACTSFINDER_ITEM_UPDATERS = set()

FACTSFINDER_RETRACTABLES = {
	'ff_file_custom_yml', 'ff_log_files', 
}
