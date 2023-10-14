
import PySimpleGUI as sg

import nettoolkit as nt
from nettoolkit_common.gpl import STR, LOG
from nettoolkit.forms import GuiTemplate, btn_ipscanner_exec, btn_minitools_exec, btn_captureit_exec
from nettoolkit.forms.formitems import *

#
from nettoolkit.forms.md5_calculator import md5_calculator_exec, md5_calculator_frame
from nettoolkit.forms.pw_enc_dec import pw_enc_cisco_exec, pw_dec_cisco_exec, pw_enc_juniper_exec, pw_dec_juniper_exec, pw_enc_decr_frame
from nettoolkit.forms.prefixes_oper import prefixes_oper_summary_exec, prefixes_oper_issubset_exec, prefixes_oper_pieces_exec, prefixes_oper_frame
from nettoolkit.forms.juniper_oper import juniper_oper_to_jset_exec, juniper_oper_remove_remarks_exec, juniper_oper_frame
#
from nettoolkit.forms.subnet_scanner import subnet_scanner_exec, subnet_scanner_frame, count_ips
from nettoolkit.forms.compare_scanner_outputs import compare_scanner_outputs_exec, compare_scanner_outputs_frame
from nettoolkit.forms.create_batch import create_batch_exec, create_batch_frame
#
from capture_it.forms.cred import *
from capture_it.forms.options import *
from capture_it.forms.common_to_all import *
from capture_it.forms.custom import *



# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class Nettoolkit(GuiTemplate):
	'''Minitools UserForm asking user inputs.	'''

	# Object Initializer
	def __init__(self):
		self.header = f'Nettoolkit: {nt.version()} - {super().header}'
		super().__init__()
		self.tabs_dic = {
			# - minitools
			'MD5 Calculate': md5_calculator_frame(),
			'P/W Enc/Dec': pw_enc_decr_frame(),
			'Prefix Operations': prefixes_oper_frame(),
			'Juniper': juniper_oper_frame(),
			# - ipscanner
			'Subnet Scanner': subnet_scanner_frame(),
			'Compare Scanner Outputs': compare_scanner_outputs_frame(),
			'Create Batch': create_batch_frame(),
			# - captureit
			'cred': exec_cred_frame(),
			'options': exec_options_frame(),
			'custom': exec_custom_frame(),
			'Common': exec_common_to_all_frame(),
		}
		self.event_catchers = {
			# - minitools
			'go_md5_calculator': md5_calculator_exec,
			'go_pw_enc_cisco': pw_enc_cisco_exec,
			'go_pw_dec_cisco': pw_dec_cisco_exec,
			'go_pw_enc_juniper': pw_enc_juniper_exec,
			'go_pw_dec_juniper': pw_dec_juniper_exec,
			'go_pfxs_summary': prefixes_oper_summary_exec,
			'go_pfxs_issubset' : prefixes_oper_issubset_exec,
			'go_pfxs_break': prefixes_oper_pieces_exec,
			'go_juniper_to_set': juniper_oper_to_jset_exec,
			'go_juniper_remove_remarks': juniper_oper_remove_remarks_exec,
			'btn_ipscanner': btn_ipscanner_exec,
			# - ipscanner
			'go_subnet_scanner': subnet_scanner_exec,
			'go_compare_scanner_outputs': compare_scanner_outputs_exec,
			'go_create_batch': create_batch_exec,
			'btn_minitools': btn_minitools_exec,
			# - captureit
			'device_ip_list_file': device_ip_list_file_exec,
			'cisco_cmd_list_file': cisco_cmd_list_file_exec,
			'juniper_cmd_list_file': juniper_cmd_list_file_exec,
			'cit_common': cit_common_exec,
			'custom_cit_file': custom_cit_file_exec,
			'custom_dynamic_cmd_class_name': custom_dynamic_cmd_class_name_exec,
			'generate_facts': generate_facts_exec,
			'custom_ff_file': custom_ff_file_exec,
			'custom_fk_file': custom_fk_file_exec,
			'custom_ff_class_name': custom_ff_name_exec,
			'custom_fk_name': custom_fk_name_exec,
			'btn_captureit': btn_captureit_exec,
		}
		self.event_updaters = {
			# - minitools
			'go_md5_calculator',
			'go_pw_enc_cisco',
			'go_pw_dec_cisco',
			'go_pw_enc_juniper',
			'go_pw_dec_juniper',
			'go_pfxs_summary',
			'go_pfxs_issubset',
			'go_pfxs_break',
			# - ipscanner
			# - captureit
			'cit_common',
			'device_ip_list_file',
			'cisco_cmd_list_file',
			'juniper_cmd_list_file',
			'custom_cit_file',
			'custom_dynamic_cmd_class_name',
			'generate_facts',
			'custom_ff_file', 'custom_ff_class_name',
			'custom_fk_file', 'custom_fk_name',
		}
		self.tab_updaters = {
			'btn_ipscanner',
			'btn_minitools',
			'btn_captureit',
		}
		self.custom_dynamic_cmd_class = None   # custom dynamic commands execution class
		self.custom_ff_class = None  # custom facts finder class
		self.custom_fk = {}  # custom facts finder foreign keys
		self.set_button_pallete()


	def user_events(self, i, event):
		if event == 'file_md5_hash_check':
			self.event_update_element(file_md5_hash_value={'value': ""})
		if event == 'go_count_ips':
			self.event_update_element(ss_ip_counts={'value': count_ips(i['pfxs'], i['till'])})


	@property
	def cleanup_fields(self):
		return (
			# - minitools
			'file_md5_hash_check', 'file_md5_hash_value',
			'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
			'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
				'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
			'file_juniper', 'op_folder_juniper',
			# - ipscanner
			'op_folder', 'pfxs', 'sockets', 'till', 
			'file1', 'file2',
			'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',
			# - captureit
			'op_folder', 'cred_en', 'cred_un', 'cred_pw', 
			'device_ip_list_file', 'device_ips',
			'cisco_cmd_list_file', 'cisco_cmds',
			'juniper_cmd_list_file', 'juniper_cmds',
			'custom_cit_file', 'custom_dynamic_cmd_class_name', 'custom_dynamic_cmd_class_str',
			'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str',
			'custom_fk_file', 'custom_fk_name','custom_fk_str',
			'append_to', 'common_log_file', 'cred_log_type', 'concurrent_connections', 'visual_progress',

		)

	def set_button_pallete(self):
		nbpb = [
			sg.Button("Minitools", change_submits=True, key='btn_minitools'), 
			sg.Button("IPScanner", change_submits=True, key='btn_ipscanner'), 
			sg.Button("CaptureIT", change_submits=True, key='btn_captureit'), 
		]
		self.add_to_button_pallete_buttons(nbpb)


# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 



# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# Test UI #
	# u = Nettoolkit()
	# u()
	# del(u)

# ------------------------------------------------------------------------------
