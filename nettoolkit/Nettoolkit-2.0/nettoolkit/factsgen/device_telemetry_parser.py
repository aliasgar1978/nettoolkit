
# =======================================================================================
#  IMPORTS
# =======================================================================================
from collections import OrderedDict
from pathlib import Path

from .parser.file_parser import parse_network_output_file
from .parser.telemetry.cisco import CISCO_CMD_REGISTER
from .parser.telemetry.juniper import JUNIPER_CMD_REGISTER, merge_juniper_transceivers_to_interfaces

from .parser.telemetry.cisco.sdwan import CISCO_SDWAN_CMD_REGISTER, merge_control_conn_local_prop

from nettoolkit.cmn.fdict import merge_dict
from nettoolkit.cmn.fio import write_as_yaml


import yaml

CISCO_REGISTERS = OrderedDict(CISCO_CMD_REGISTER)
CISCO_SDWAN_REGISTERS = OrderedDict(CISCO_SDWAN_CMD_REGISTER)
CISCO_REGISTERS.update(CISCO_SDWAN_REGISTERS)

CMD_REGISTERS = {
    'cisco': CISCO_REGISTERS,
    'juniper': JUNIPER_CMD_REGISTER,
}

# =======================================================================================
# Main facts extractor function 
# =======================================================================================

def extract_device_telemetry_data(capture_file, output_directory=None):
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

    telemetry_data = {}
    additional_outputs = {}

    for i, (command, parser_registrations) in enumerate(device_register.items()):
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
            section_data = {section: parsed_data}

            if (make == 'juniper' 
                and command == 'show chassis hardware' 
                # and i == 1
                and section == 'hardware_ports'
                ):
                merge_juniper_transceivers_to_interfaces(telemetry_data, section_data['hardware_ports'])
            elif ( make == 'cisco'
                and command in (
                'show sdwan control connections', 
                'show sdwan control local-properties'
                )):
                additional_outputs[command] = section_data             
            elif parsed_data:
                merge_dict(telemetry_data, section_data)


    add_exclusions(telemetry_data, additional_outputs)

    output_dir = (
        Path(output_directory)
        if output_directory
        else capture_path.parent
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{hostname}_devices-telemetry-data.yaml'
    write_as_yaml(telemetry_data, file=str(output_file ))


def add_exclusions(telemetry_data, additional_outputs):
    # 1. Merge SDWAN CONTROL CONNECTIONS / LOCAL PROP DATA AND ADD IT TO TELEMETRY
    ctrl_conn_dict = 'show sdwan control connections'
    ctrl_local_prop_dict = 'show sdwan control local-properties'
    if additional_outputs.get(ctrl_conn_dict) and additional_outputs.get(ctrl_local_prop_dict):
        control_conn_merged_dict = merge_control_conn_local_prop(
            additional_outputs[ctrl_conn_dict],
            additional_outputs[ctrl_local_prop_dict]
        )
        merge_dict(telemetry_data,  {'sdwan': control_conn_merged_dict})

    if additional_outputs.get(ctrl_local_prop_dict):
        merge_dict(telemetry_data, {'sdwan': {'system':additional_outputs[ctrl_local_prop_dict]['sdwan']['system']}} )

    # 2. -- Add as comes



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
            extract_device_telemetry_data(capture_file)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            print(f"[-] {capture_file.name}: {exc}")


# =======================================================================================

__all__ = ['extract_device_telemetry_data', ]

