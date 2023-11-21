
# --------------------------------------------
# IMPORTS
# --------------------------------------------
from capture_it import capture, LogSummary
from nettoolkit import *
from pathlib import *
import sys

# --------------------------------------------
# path / folder settings
# --------------------------------------------
p = Path(".")
previous_path = p.resolve().parents[0]
sys.path.insert(len(sys.path), str(previous_path))
capture_folder = str(previous_path.joinpath('captures'))
commands_folder = str(previous_path.joinpath('commands'))

"""
==============
TREE STRUCTURE
==============

Parent
|
| - + myPrograms / scripts
|   | - exec-capture_it-Common.py
|   | - cred.py ( contains login username (un), password (pw) )
|
| - + captures
|   | - [ output files ]  
|
| - + commands
    | - devices.txt (list of device ip addresses)
    | - cisco_cmds_txtfsm.txt (LIST OF CISCO COMMANDS TO BE CAPTURED)
    | - juniper_cmds_txtfsm.txt (LIST OF JUNIPER COMMANDS TO BE CAPTURED)


"""

# --------------------------------------------
# Some Local Functions
# --------------------------------------------

# get the list of items.
def get_item_list(file):
  with open(file, 'r') as f:
    lns = f.readlines() 
  return [ _.strip() for _ in lns]


# get the list of devices, default all, or leg wise if provided.
def get_devices(device_list_file):
  devices = get_item_list(device_list_file)
  return devices

# get the dictionary of list of commands
def get_commands_list_dictionary(cisco_file, juniper_file, arista_file):
  CISCO_IOS_CMDS = get_item_list(cisco_file)
  JUNIPER_JUNOS_CMDS = get_item_list(juniper_file)
  ARISTA_EOS_CMDS = get_item_list(arista_file)
  return {
    'cisco_ios'  : CISCO_IOS_CMDS,
    'juniper_junos': JUNIPER_JUNOS_CMDS,
    'arista_eos': ARISTA_EOS_CMDS,
  }

# ------------------------------------------------------------------------------------------------------------
#  EXECUTE
# ------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

  # --------------------------------------------
  #    INPUT: Credentials
  # --------------------------------------------
  # option 1 ------------- ( import un/pw from a file )
  from cred import un, pw    ## cred.py should be a file from where you stored login un/pw

  # option 2 ------------- ( input manualy )
  # un = get_username()
  # pw = get_password()

  # authentication Dictionary -----------
  auth = { 'un':un, 'pw':pw, 'en':pw }

  # --------------------------------------------
  #    INPUT: necessary files
  # --------------------------------------------
  device_list_file = f"{commands_folder}/devices.txt"
  cisco_cmds_file = f"{commands_folder}/cisco_cmds_txtfsm.txt"
  juniper_cmds_file = f'{commands_folder}/juniper_cmds_txtfsm.txt'
  arista_cmds_file = f"{commands_folder}/cisco_cmds_txtfsm.txt"

  # ---- get devices & commands  ----
  devices = get_devices(device_list_file)
  cmds = get_commands_list_dictionary(cisco_cmds_file, juniper_cmds_file, arista_cmds_file)


  # ---- START CAPTURE ----
  c = capture(
    devices,                  # mandatory - list of devices
    auth,                     # mandatory - authentication parameters dictionary
    cmds,                     # mandatory - dictionary of list of commands
    path=capture_folder,      # mandatory - output capture path
    cumulative=True,                       # optional arg ( other options = False, 'both')
    forced_login=True,                     # optional arg 
    parsed_output=True,                    # optional arg (def: False)
    visual_progress=11,                    # optional arg (def: 3)
    log_type='both',                       # optional arg - options = 'common', individual', 'both', None ( def: None)
    common_log_file='common-debug.log',    # optional arg if log_type is individual (def: None)
    concurrent_connections=40              # optional arg (def: 100)
  )
  LS = LogSummary(c, print=True, write_to=f'{capture_folder}/cmds_log_summary.log')
  print("Capture Task(s) Complete..")
  #------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
