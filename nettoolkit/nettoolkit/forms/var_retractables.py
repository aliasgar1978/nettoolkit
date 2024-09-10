
from nettoolkit.capture_it.forms.execs import CAPTUREIT_RETRACTABLES
from nettoolkit.facts_finder.forms.execs import FACTSFINDER_RETRACTABLES
from nettoolkit.j2config.forms.execs import J2CONFIG_RETRACTABLES
from nettoolkit.pyVig.forms.execs import PYVIG_RETRACTABLES

# ---------------------------------------------------------------------------------------
#  sets of retractable variables 
# ---------------------------------------------------------------------------------------

MINITOOLS_RETRACTABLES = {
	'file_md5_hash_check', 'file_md5_hash_value',
	'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
	'file_juniper', 'op_folder_juniper',
	'quick_show_device_ip', 'quick_show_cmds', 'quick_sh_cred_un', 'quick_sh_cred_pw', 'quick_sh_cred_en',
	'pw_file_cisco', 'pw_file_juniper',
}
IPSCANNER_RETRACTABLES = {
	'op_folder', 'pfxs', 'sockets', 'till', 
	'file1', 'file2',
	'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',
	'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
	'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
}


# FACTSFINDER_RETRACTABLES = {
# 	'ff_log_files', 	
# 	'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str_cit',
# 	'custom_fk_file', 'custom_fk_name','custom_fk_str_cit',
# }
# J2CONFIG_RETRACTABLES = set()
# PYVIG_RETRACTABLES = {
# 	'py_stencil_folder', 'py_default_stencil', 'py_output_folder', 'py_op_file', 'pv_input_data_files', 'pv_cm_file', 
# }
CONFIGURE_RETRACTABLES = {
	'config_excel_files', 'lb_config_excel_files', 'lb_config_excel_files_sequenced',
	'configuration_log_folder', 'cred_en1', 'cred_un1', 'cred_pw1', 
}

# -------------------------------------------------------------------------
RETRACTABLES = set()
RETRACTABLES = RETRACTABLES.union(MINITOOLS_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(IPSCANNER_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(CAPTUREIT_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(FACTSFINDER_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(J2CONFIG_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(PYVIG_RETRACTABLES)
RETRACTABLES = RETRACTABLES.union(CONFIGURE_RETRACTABLES)
# -------------------------------------------------------------------------

__all__ = [RETRACTABLES]