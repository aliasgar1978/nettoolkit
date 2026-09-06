
# =======================================================================================
#  IMPORTS
# =======================================================================================

from parser.file_parser import parse_network_output_file
from parser.telemetry.cisco import CISCO_CMD_REGISTER, CISCO_CMD_SECTION
from parser.telemetry.juniper import JUNIPER_CMD_REGISTER, JUNIPER_CMD_SECTION, merge_juniper_transceivers_to_interfaces

from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.fio import write_as_yaml

import yaml

# =======================================================================================
# Main facts extractor function 
# =======================================================================================

def extract_device_telemetry_data(capture_file):

    registers_map = {
        'cisco': CISCO_CMD_REGISTER,
        'juniper': JUNIPER_CMD_REGISTER,
    }
    cmd_sections_map = {
        'cisco': CISCO_CMD_SECTION,
        'juniper': JUNIPER_CMD_SECTION,
    }

    capture_file_result_dic = parse_network_output_file(capture_file, cmd_registers={'cisco': CISCO_CMD_REGISTER, 'juniper': JUNIPER_CMD_REGISTER})
    hostname = capture_file_result_dic['hostname']
    make     = capture_file_result_dic['make']
    cmd_dict = capture_file_result_dic['cmd_op']

    parser_functions = registers_map.get(make)
    cmd_sections     = cmd_sections_map.get(make)
    if not parser_functions:
        raise Exception(f"No Valid command parsers available for identified device type {make}")

    d = {}

    for cmd, section_tuple in cmd_sections.items():
        if cmd not in cmd_dict:
            continue
        #
        cmd_op = cmd_dict[cmd]
        parser_function_tuple = parser_functions.get(cmd)
        if not parser_function_tuple: continue
        for i, parser_function in enumerate(parser_function_tuple):
            parser_dict = parser_function(cmd_op)
            # try:
            op_dict = {section_tuple[i]: parser_dict['op_dict']}

            if make == 'juniper' and cmd == 'show chassis hardware' and i == 1:
                merge_juniper_transceivers_to_interfaces(d, op_dict['hardware_ports'])
            else:
                merge_dict(d, op_dict)


            # except:
            #     print(f"[-] Failed to parse output for command: {cmd}")

    write_as_yaml(d, file=f'{hostname}_devices-telemetry-data.yaml')

# =======================================================================================
# Main bypass
# =======================================================================================
if __name__ == "__main__": 
    # extract_device_telemetry_data("5aa-ecd-b.log")
    # extract_device_telemetry_data("00h-ecd-a.log")
    pass
# =======================================================================================

__all__ = ['extract_device_telemetry_data', ]

