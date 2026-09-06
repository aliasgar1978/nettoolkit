
# =======================================================================================
#  IMPORTS
# =======================================================================================

from parser.file_parser import parse_network_output_file
from parser.device.cisco import CISCO_CMD_REGISTER, CISCO_CMD_SECTION
from parser.device.juniper import JUNIPER_CMD_REGISTER, JUNIPER_CMD_SECTION

from nettoolkit.juniper import JSet
from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.fio import write_as_yaml
# from pprint import pprint
import yaml

# =======================================================================================
# Main facts extractor function 
# =======================================================================================

def extract_device_facts(capture_file):

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
    if make == 'juniper':
        js = JSet(input_list=cmd_dict.get("show configuration", []))
        cmd_dict["show configuration"] = js()
        with open(hostname+"_jset.txt", 'w') as f:
            f.write("\n".join(cmd_dict['show configuration']))

    for cmd, section_tuple in cmd_sections.items():
        if cmd not in cmd_dict:
            continue
        #
        cmd_op = cmd_dict[cmd]
        parser_function_tuple = parser_functions.get(cmd)
        if not parser_function_tuple: continue
        for i, parser_function in enumerate(parser_function_tuple):
            parser_dict = parser_function(cmd_op)
            try:
                op_dict = {section_tuple[i]: parser_dict['op_dict']}
                merge_dict(d, op_dict)
            except:
                print(f"[-] Failed to parse output for section: {section_tuple[i]} for {parser_function}")

    write_as_yaml(d, file=f'{hostname}_devices-data.yaml')

# =======================================================================================
# Main bypass
# =======================================================================================
if __name__ == "__main__": 
    # extract_device_facts("5aa-ecd-b.log")
    # extract_device_facts("00h-ecd-a.log")
    pass
# =======================================================================================

__all__ = ['extract_device_facts', ]

