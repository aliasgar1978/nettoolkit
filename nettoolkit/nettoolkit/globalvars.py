
# ---------------------------------------------------------------------------------------
from nettoolkit.nettoolkit.forms.gui_template import TAB_EVENT_UPDATERS
#
from nettoolkit.nettoolkit.forms import (
	btn_ipscanner_exec, btn_minitools_exec, btn_captureit_exec, 
	btn_factsfinder_exec, btn_pyvig_exec, btn_j2config_exec
)
# ---------------------------------------------------------------------------------------
#
from nettoolkit.nettoolkit.forms.md5_calculator import md5_calculator_exec, md5_calculator_frame
from nettoolkit.nettoolkit.forms.pw_enc_dec import pw_enc_cisco_exec, pw_dec_cisco_exec, pw_enc_juniper_exec, pw_dec_juniper_exec, pw_enc_decr_frame
from nettoolkit.nettoolkit.forms.prefixes_oper import (prefixes_oper_summary_exec, prefixes_oper_issubset_exec, prefixes_oper_pieces_exec, 
	summarize_prefixes_frame, issubset_check_prefix_frame, devide_prefixes_frame
)
from nettoolkit.nettoolkit.forms.juniper_oper import juniper_oper_to_jset_exec, juniper_oper_remove_remarks_exec, juniper_oper_frame
#
from nettoolkit.addressing.forms.subnet_scanner import *
from nettoolkit.addressing.forms.compare_scanner_outputs import *
from nettoolkit.addressing.forms.create_batch import *
#
from nettoolkit.capture_it.forms.cred import *
from nettoolkit.capture_it.forms.options import *
from nettoolkit.capture_it.forms.common_to_all import *
from nettoolkit.capture_it.forms.custom import *
#
from nettoolkit.facts_finder.forms.ff_generate import *
from nettoolkit.facts_finder.forms.ff_custom import *
from nettoolkit.facts_finder.forms.ff_custom_cit import *
#
from nettoolkit.pyVig.forms.input_data import *
from nettoolkit.pyVig.forms.custom import *
#
from nettoolkit.j2config.forms.input_data import *
#
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# GLOBAL VARS
# ---------------------------------------------------------------------------------------
MINITOOLS_FRAMES = {
	'1.Juniper': juniper_oper_frame(),
	'2.P/W Enc/Dec': pw_enc_decr_frame(),
	'3.MD5 Calculate': md5_calculator_frame(),
}
IPSCANNER_FRAMES = {
	'1.Subnet Scanner': subnet_scanner_frame(),
	'2.Scan Compare': compare_scanner_outputs_frame(),
	'3.Create Batch': create_batch_frame(),
	'4.Summarize':summarize_prefixes_frame(),
	'5.Break Prefix':devide_prefixes_frame(),
	'6.isSubset':issubset_check_prefix_frame(),
}
CAPTUREIT_FRAMES = {
	'1.Capture': exec_common_to_all_frame(),
	'2.Cred': exec_cred_frame(),
	'3.Options': exec_options_frame(),
	'4.Customize Capture': exec_custom_frame(),
	'5.Facts Gen': exec_ff_custom_cit_frame(),
}
FACTSFINDER_FRAMES = {
	'1.Facts Gen': btn_ff_gen_frame(),	
	'2.Customize Facts': exec_ff_custom_frame(),
}
J2CONFIG_FRAMES = {
	'1.Config Gen': j2_gen_frame(),
}
PYVIG_FRAMES = {
	'1.Visio Gen': pv_input_data_frame(),   # self.input_data()
	'2.Customize pyVig': pv_custom_data_frame(),
	# 'pyVig Filters': pv_apply_filters_frame(),  # self.select_filters()
	# 'pyVig Options': pv_options_frame(),   # self.other_options()
}
# --------------------------------------------------------
MINITOOLS_EVENT_FUNCS = {
	'go_md5_calculator': md5_calculator_exec,
	'go_pw_enc_cisco': pw_enc_cisco_exec,
	'go_pw_dec_cisco': pw_dec_cisco_exec,
	'go_pw_enc_juniper': pw_enc_juniper_exec,
	'go_pw_dec_juniper': pw_dec_juniper_exec,
	'go_juniper_to_set': juniper_oper_to_jset_exec,
	'go_juniper_remove_remarks': juniper_oper_remove_remarks_exec,
}
IPSCANNER_EVENT_FUNCS = {
	'btn_ipscanner': btn_ipscanner_exec,
	'go_subnet_scanner': subnet_scanner_exec,
	'go_compare_scanner_outputs': compare_scanner_outputs_exec,
	'go_create_batch': create_batch_exec,
	'btn_minitools': btn_minitools_exec,
	'go_pfxs_summary': prefixes_oper_summary_exec,
	'go_pfxs_issubset' : prefixes_oper_issubset_exec,
	'go_pfxs_break': prefixes_oper_pieces_exec,
}
CATPUREIT_EVENT_FUNCS = {
	'device_ip_list_file': device_ip_list_file_exec,
	'cisco_cmd_list_file': cisco_cmd_list_file_exec,
	'juniper_cmd_list_file': juniper_cmd_list_file_exec,
	'cit_common': cit_common_exec,
	'custom_cit_file': custom_cit_file_exec,
	'custom_dynamic_cmd_class_name': custom_dynamic_cmd_class_name_exec,
	'custom_ff_file_cit': custom_ff_file_cit_exec,
	'custom_fk_file_cit': custom_fk_file_cit_exec,
	'custom_ff_class_name_cit': custom_ff_name_cit_exec,
	'custom_fk_name_cit': custom_fk_name_cit_exec,
	'btn_captureit': btn_captureit_exec,
}
FACTSFINDER_EVENT_FUNCS = {
	'btn_ff_gen': btn_ff_gen_exec, 
	'btn_factsfinder': btn_factsfinder_exec,
	'custom_ff_file': custom_ff_file_exec,
	'custom_fk_file': custom_fk_file_exec,
	'custom_ff_class_name': custom_ff_name_exec,
	'custom_fk_name': custom_fk_name_exec,
}
J2CONFIG_EVENT_FUNCS = {
	'btn_j2config': btn_j2config_exec,
	'btn_j2_gen': btn_j2_gen_exec,
	'j2_custom_reg': j2_custom_reg_exec,
	# 'j2_custom_cls': j2_custom_cls_exec,
	# 'j2_custom_fn': j2_custom_fn_exec,
}
PYVIG_EVENT_FUNCS = {
	'btn_pyvig': btn_pyvig_exec,
	'pv_radio_input_data_files': pv_radio_input_data_files_exec,
	'pv_radio_cm_file': pv_radio_cm_file_exec,
	'pv_start': pv_start_exec,
}
# --------------------------------------------------------
MINITOOLS_EVENT_UPDATERS = {
	'go_md5_calculator',
	'go_pw_enc_cisco', 'go_pw_dec_cisco', 'go_pw_enc_juniper', 'go_pw_dec_juniper',
}
IPSCANNER_EVENT_UPDATERS = {
	'go_pfxs_summary', 'go_pfxs_issubset', 'go_pfxs_break',
}
CAPTUREIT_EVENT_UPDATERS = {
	'cit_common',
	'device_ip_list_file', 'cisco_cmd_list_file', 'juniper_cmd_list_file',
	'custom_cit_file', 'custom_dynamic_cmd_class_name',
	'custom_ff_file_cit', 'custom_ff_class_name_cit', 'custom_fk_file_cit', 'custom_fk_name_cit',	
}

FACTSFINDER_EVENT_UPDATERS = {
	'btn_ff_gen',
	'custom_ff_file', 'custom_ff_class_name', 'custom_fk_file', 'custom_fk_name',	
}
J2CONFIG_EVENT_UPDATERS = {
	'btn_j2_gen', 'j2_custom_reg', 'j2_custom_cls', 'j2_custom_fn', 
}
PYVIG_EVENT_UPDATERS = {
	'pv_radio_input_data_files', 'pv_radio_cm_file', 
	'pv_start',
}
# --------------------------------------------------------

MINITOOLS_RETRACTABLES = {
	'file_md5_hash_check', 'file_md5_hash_value',
	'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
	'file_juniper', 'op_folder_juniper',
}
IPSCANNER_RETRACTABLES = {
	'op_folder', 'pfxs', 'sockets', 'till', 
	'file1', 'file2',
	'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',
	'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
	'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
}
CAPTUREIT_RETRACTABLES = {
	'cit_op_folder', 'cred_en', 'cred_un', 'cred_pw', 
	'device_ip_list_file', 'device_ips',
	'cisco_cmd_list_file', 'cisco_cmds',
	'juniper_cmd_list_file', 'juniper_cmds',
	'custom_cit_file', 'custom_dynamic_cmd_class_name', 'custom_dynamic_cmd_class_str', 'custom_dynamic_cmd_class_depenedt_str',
	'custom_ff_file_cit', 'custom_ff_class_name_cit', 'custom_ff_class_str_cit',
	'custom_fk_file_cit', 'custom_fk_name_cit','custom_fk_str_cit',
	'append_to', 'common_log_file', 'cred_log_type', 'max_connections', 'visual_progress',
}
FACTSFINDER_RETRACTABLES = {
	'ff_log_files', 	
	'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str',
	'custom_fk_file', 'custom_fk_name','custom_fk_str',
}
J2CONFIG_RETRACTABLES = set()
PYVIG_RETRACTABLES = {
	'py_stencil_folder', 'py_default_stencil', 'py_output_folder', 'py_op_file', 'pv_input_data_files', 'pv_cm_file', 
}

# --------------------------------------------------------
# ---------------------------------------------------------------------------------------
