
from nettoolkit.cmn.fio import read_yaml






def get_commands_for_type(commands_lists_yaml_file, device_type):
    """Returns specific list of commands based on vendor profile."""
    cmd_dict = read_yaml(commands_lists_yaml_file)
    return cmd_dict.get(device_type, ['show version',])

    ## SAMPLE
    # commands = {
    #     'cisco_xe': ['show version', 'show ip interface brief', 'show running-config'],
    #     'cisco_ios': ['show version', 'show ip interface brief', 'show running-config'],
    #     'juniper_junos': ['show version', 'show interfaces terse', 'show configuration'],
    #     'arista_eos': ['show version', 'show ip interface brief', 'show running-config'],
    #     'cisco_viptela': ['show interface | tab', 'show int desc | tab', ],
    #     'aruba_silverpeak': ['en', 'show int',]
    # }
    

