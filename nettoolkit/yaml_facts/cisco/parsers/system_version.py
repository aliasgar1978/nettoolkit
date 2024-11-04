"""cisco show version command output parser """

# ------------------------------------------------------------------------------
from .common import *
# ------------------------------------------------------------------------------

def get_version(command_output):
	op_dict = {}
	parsed_data = parse_to_dict_using_ntc('show version', command_output)[0]
	#
	op_dict['ios_version'] = parsed_data['VERSION']
	op_dict['boot_image']  = parsed_data['RUNNING_IMAGE']
	op_dict['hostname']    = parsed_data['HOSTNAME']
	op_dict['host-name']   = parsed_data['HOSTNAME']
	op_dict['uptime']      = parsed_data['UPTIME']
	op_dict['serial']      = parsed_data['SERIAL']
	op_dict['model']       = parsed_data['HARDWARE']
	op_dict['conf-reg']    = parsed_data['CONFIG_REGISTER']
	op_dict['make']        = 'cisco'
	op_dict['device_mac']  = parsed_data['MAC']
	
	return {'system': op_dict }

# ------------------------------------------------------------------------------
