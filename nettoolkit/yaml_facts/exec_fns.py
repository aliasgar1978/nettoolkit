"""Description: 
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from nettoolkit.yaml_facts import YamlFacts
from pathlib import *
from nettoolkit.nettoolkit_common import print_banner


# ==============================================================================================
#  Local Statics
# ==============================================================================================


# ==============================================================================================
#  Local Functions
# ==============================================================================================
def get_host(log_file):
	return Path(log_file).stem

def exec_yaml_facts(
	log_files,
	output_folder=None,
	):
	print_banner("Yaml Facts", 'yellow')
	for log_file in log_files:
		if not log_file.endswith(".log"): continue
		device = get_host(log_file)
		print(">> starting", device, "...", end='\t')
		#
		try:
			YF = YamlFacts(log_file, output_folder)
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


# ==============================================================================================
#  Classes
# ==============================================================================================



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
