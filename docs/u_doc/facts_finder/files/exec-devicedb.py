# ========================================================================================
# This is a sample execution file, for facts-finder usage, to generate excel db file 
# Please modify the script for providing input marked at INPUT: markers
# ========================================================================================


# -------------------------------------------------
# Import necessary package, modules
# -------------------------------------------------
from facts_finder import DeviceDB
from facts_finder import device
from nettoolkit import write_to_xl


# -------------------------------------------------
# INPUT: Define your input files ( i.e. captures )
# -------------------------------------------------
file = "file_with_output_captured.log"          # provide capture file
output_file = 'output_file.xlsx'

# -------------------------------------------------
# Generate and evaluate database from device
# -------------------------------------------------
_model = device(file)           # select the model based on input file
device_database = DeviceDB()    # create a new device database object
df_dict = device_database.evaluate(_model)      # evaluate object by providing necessary model, and return dictionary

# -------------------------------------------------
# Write database to Excel
# -------------------------------------------------
write_to_xl(output_file, df_dict, index=True, overwrite=True)    # write output to Excel
