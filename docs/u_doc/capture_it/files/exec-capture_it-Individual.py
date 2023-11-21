"""
==============
TREE STRUCTURE
==============

Parent
|
| - + myPrograms
|   |	- exec-capture_it - Individual.py
|   |	- cred.py ( contains login username (un), password (pw) )
|
| - + captures
|   | - [ output files ]	
|
| - + commands
    | - devices_cmds.xlsx

"""

# --------------------------------------------
# IMPORTS
# --------------------------------------------
from capture_it import capture_individual, LogSummary
from nettoolkit import *
from pathlib import *
from pprint import pprint
import sys


# --------------------------------------------
# path / folder settings
# --------------------------------------------
p = Path(".")
previous_path = p.resolve().parents[0]
sys.path.insert(len(sys.path), str(previous_path))
capture_folder = str(previous_path.joinpath('captures'))
commands_folder = str(previous_path.joinpath('commands'))


# --------------------------------------------
# Some Local Functions
# --------------------------------------------

# Read Commands / Devices from Excel
def get_devices_command_dict(dev_cmd_xl_file):
  # READ EXCEL
  df_dict = read_xl(dev_cmd_xl_file)

  # create individual {ip: [commands list]} dictionary
  devices_command_dict = {}
  for sht, df in df_dict:
    df = df.fillna('')
    ips = tuple(df['ips'][df['ips'] != ''])
    commands = tuple(df['commands'][df['commands'] != ''])
    if not devices_command_dict.get(ips):
      devices_command_dict[ips] = []
    devices_command_dict[ips].extend(commands)

  return devices_command_dict


# ------------------------------------------------------------------------------------------------------------
# EXECUTE
# ------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

  # --------------------------------------------
  #    INPUT: Credentials
  # --------------------------------------------
  #
  # option 1 ------------- ( import un/pw from a file )
  from cred import un, pw

  # option 2 ------------- ( input manualy )
  # un = get_username()
  # pw = get_password()

  # authentication Dictionary -----------
  auth = { 'un':un, 'pw':pw, 'en':pw }

  # ------------------------------------------------
  #   INPUT:  DEVICES/COMMANDS Excel FILE
  # ------------------------------------------------
  dev_cmd_xl_file = f'{commands_folder}/devices_cmds.xlsx'

  # ---- get dictionary of {ip:[cmds]} for each individual device or set of devices  ----
  devices_command_dict = get_devices_command_dict(dev_cmd_xl_file)

  # ---- START CAPTURE ----
  c = capture_individual(
    auth, 
    devices_command_dict,
    op_path=capture_folder, 
    cumulative=True,      # optional arg
    forced_login=True,    # optional arg 
    parsed_output=True,   # optional arg
    visual_progress=10,                    # optional arg (def: 3)
    log_type='individual',                 # optional arg - options = 'common', individual', 'both', None ( def: None)
    common_log_file='common-debug.log',    # optional arg if log_type is individual (def: None)
    concurrent_connections=30              # optional arg (def: 100)
  )
  LS = LogSummary(c, print=True, write_to=f'{capture_folder}/cmds_log_summary.log')
  print("Capture Task(s) Complete..")
  # ------------------------------------------------
