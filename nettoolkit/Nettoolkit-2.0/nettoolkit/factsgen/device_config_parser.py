
# =======================================================================================
#  IMPORTS
# =======================================================================================
from pathlib import Path

from parser.file_parser import parse_network_output_file
from parser.device.cisco import CISCO_CMD_REGISTER
from parser.device.juniper import JUNIPER_CMD_REGISTER

from nettoolkit.juniper import JSet
from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.fio import write_as_yaml
# from pprint import pprint
import yaml

CMD_REGISTERS = {
    'cisco': CISCO_CMD_REGISTER,
    'juniper': JUNIPER_CMD_REGISTER,
}

# =======================================================================================
# Main facts extractor function 
# =======================================================================================

def extract_device_facts(capture_file, output_directory=None):
    capture_path = Path(capture_file)
    capture_file_result_dic = parse_network_output_file(capture_path, 
                                                        cmd_registers=CMD_REGISTERS)
    hostname = capture_file_result_dic.get('hostname')
    make     = capture_file_result_dic.get('make')
    cmd_dict = capture_file_result_dic.get('cmd_op', {})
    if not hostname or not make:
        raise ValueError(f"Could not identify hostname/vendor from {capture_file}")

    device_register = CMD_REGISTERS.get(make)
    if device_register is None:
        raise ValueError(
            f"Unsupported device make {make!r} "
            f"for {capture_path}"
        )

    device_data = {}

    if make == 'juniper':
        js = JSet(input_list=cmd_dict.get("show configuration", []))
        cmd_dict["show configuration"] = js()
        with open(hostname+"_jset.txt", 'w') as f:
            f.write("\n".join(cmd_dict['show configuration']))

    for command, parser_registrations in device_register.items():
        command_output = cmd_dict.get(command)
        if command not in cmd_dict or command_output is None:
            print(f"[-] Missing capture: [{hostname}] - [{command}]")
            continue

        parser_registrations = device_register.get(command)
        if not parser_registrations: continue

        for section, parser_function in parser_registrations:
            parser_result = parser_function(command_output)

            if not isinstance(parser_result, dict):
                raise TypeError(
                    f"{parser_function.__name__} returned "
                    f"{type(parser_result).__name__}, expected dict"
                )
            if 'op_dict' not in parser_result:
                raise KeyError(
                    f"{parser_function.__name__} did not return 'op_dict'"
                )

            parsed_data = parser_result.get('op_dict', {})
            if parsed_data:
                    merge_dict(device_data, {section: parsed_data})

    output_dir = (
        Path(output_directory)
        if output_directory
        else capture_path.parent
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{hostname}_devices-data.yaml'
    write_as_yaml(device_data, file=str(output_file ))

# =======================================================================================
# Main bypass
# =======================================================================================
if __name__ == "__main__": 
    pass

    from pathlib import Path
    inventory_directory = Path("./device_vault")
    for capture_file in inventory_directory.iterdir():
        if not capture_file.is_file(): continue
        if capture_file.suffix.lower() not in {".log", ".txt", ".cfg"}: continue
        # extract_device_facts(f"./{inventory_directory}/{capture_file}")
        try:
            extract_device_facts(capture_file)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print(f"[-] {capture_file.name}: {exc}")

# =======================================================================================

__all__ = ['extract_device_facts', ]

