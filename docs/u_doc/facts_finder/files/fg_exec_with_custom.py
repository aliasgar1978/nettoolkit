# ========================================================================================
# This is a sample execution file, for facts-finder module usage, to generate clean file 
# along with custom module insertion
# Please modify the script as per your custom module name/definitions
# marked at MODIFY: markers
# Also refer to input sections to provide the inputs.
# ========================================================================================


# # ----------------------------------------------------------------------
# # Imports
# # ----------------------------------------------------------------------
import os
import pandas as pd
pd.set_option('mode.chained_assignment', None)		# (optional) disables pandas warning msgs
from facts_finder import CleanFacts, rearrange_tables

# # ----------------------------------------------------------------------
# # MODIFY:
# # ----------------------------------------------------------------------
# # Custom Project Import [ Modify as per your own project name ]
# # ----------------------------------------------------------------------
# # custom_project_name ==> refer to custom project
# # CustomDeviceFacts   ==> refer to a custom class in custom project
# # FOREIGN_KEYS        ==> refer to dictionary of list of additional columns 
# #                         to be allowed to be inserted in to output excel
# # ----------------------------------------------------------------------
from custom_project_name import CustomDeviceFacts			## Load appropriate class/function from Custom project.
from custom_project_name import FOREIGN_KEYS				## Load Custom FOREIGN_KEYS




# # ----------------------------------------------------------------------
# # Function to evaluate data
# # ----------------------------------------------------------------------
def evaluate_data(
	capture_log_file,
	capture_xl_file,
	new_suffix='-clean',   ## change it if you want something else (deault: '-clean')
	use_cdp=False
	):
	cleaned_fact = CleanFacts(capture_log_file, capture_xl_file, new_suffix, use_cdp)
	cleaned_fact()
	print(f"Cleaning done...,", end='\t')
	return cleaned_fact


# # ----------------------------------------------------------------------
# # Main Function
# # ----------------------------------------------------------------------
def main(
	capture_log_file,
	capture_xl_file,
	custom=True,
	rearrange=True,
	):	

	# # ----------------------------------------------------------------------
	# # VERIFICATION
	# # ----------------------------------------------------------------------
	try:
	  with open(capture_log_file, 'r') as f:
		print(">> starting", capture_log_file, "...", end='\t')

	except:
	  print(f"Unable to access {capture_log_file}, skipping\n{'-'*80}")
	  return None


	# # ----------------------------------------------------------------------
	# # Evaluate Data GENERAL
	# # ----------------------------------------------------------------------
	# #           available attributes of cleaned_fact
	# # ----------------------------------------------------------------------
	# #   cleaned_fact.clean_file == file name of output clean file 
	# #   cleaned_fact.hostname   == hostname of device
	# #   cleaned_fact.config     == configuration of device ( set output in case of juniper )
	# #   cleaned_fact.dev_type   == device type ('cisco', 'juniper')
	# # ----------------------------------------------------------------------
	try:
		cleaned_fact = evaluate_data(capture_log_file, capture_xl_file)
	except:		
		print(f"Cleaning Failed..., Skipping process\n{'-'*80}")
		return None


	if custom:
		# # ----------------------------------------------------------------------
		# # MODIFY:
		# # ----------------------------------------------------------------------
		# # Modify Data - CUSTOM
		# # ----------------------------------------------------------------------
		# # [ CUSTOM UPDATE GOES HERE : AS PER CUSTOM DEFINITIONS ]
		# # AN EXAMPLE CODE GIVEN BELOW. REPLACE IT WITH YOUR OWN CODE.
		# # ----------------------------------------------------------------------
		try:
			# # custom class/function which should update `cleaned_fact.clean_file` with custom columns and data
			CDF = CustomDeviceFacts(cleaned_fact)	
			# # there must be a method to overrwrite the cleaned_fact.clean_file with modified data, sample below.
			CDF.write()
			print(f"Custom Data Modifications done...,", end='\t')
		except:		
			print(f"Custom Data Modifications Failed...,", end='\t')

	# # ----------------------------------------------------------------------
	# # Rearrange Columns
	# # ----------------------------------------------------------------------
	if rearrange:
		try:
			if custom:
				# # ----------------------------------------------------------
				# # MODIFY:
				# # ----------------------------------------------------------
				# # CUSTOM: FOREIGN_KEYS - refer above for more details on it, 
				# # Edit as per your custom project
				# # ----------------------------------------------------------
				rearrange_tables(cleaned_fact.clean_file, foreign_keys=FOREIGN_KEYS)
				#
			else:
				rearrange_tables(cleaned_fact.clean_file)
			print(f"Column Rearranged done..., ", end='\t')
		except:		
			print(f"Column Rearranged Failed..., Skipping process\n{'-'*80}")
			return None

	# ----------------------------------------------------------------------

	print(f"All Tasks Completed !! {capture_log_file} !!\n{'-'*80}")

# # ---------------------------------------------------------------------------------------------------


# # ----------------------------------------------------------------------
# # Executions
# # ----------------------------------------------------------------------
if __name__ == '__main__':

	# # -------------------------------------------------------------------------------
	# # MODIFY: INPUTS
	# # -------------------------------------------------------------------------------
	# # Provide captured log and parsed Excel file names, captured using capture-it
	# # -------------------------------------------------------------------------------
	capture_log_file = 'fullpath/hostname.log'
	capture_xl_file = 'fullpath/hostname.xlsx'

	main(
		capture_log_file=capture_log_file,
		capture_xl_file=capture_xl_file,
		custom=True,		              ## optional (default: True)
		rearrange=True,                   ## optional (default: True)
	)

# # ---------------------------------------------------------------------------------------------------
