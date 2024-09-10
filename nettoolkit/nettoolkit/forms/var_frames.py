

# ---------------------------------------------------------------------------------------
#
from nettoolkit.pyJuniper.forms.md5_calculator import *
from nettoolkit.pyJuniper.forms.pw_enc_dec import *
from nettoolkit.pyJuniper.forms.juniper_oper import *
#
from nettoolkit.addressing.forms.subnet_scanner import *
from nettoolkit.addressing.forms.compare_scanner_outputs import *
from nettoolkit.addressing.forms.prefixes_oper import *
from nettoolkit.addressing.forms.create_batch import *
#
from nettoolkit.capture_it.forms.frames import CAPTUREIT_FRAMES
from nettoolkit.facts_finder.forms.frames import FACTSFINDER_FRAMES
from nettoolkit.j2config.forms.frames import J2CONFIG_FRAMES
from nettoolkit.pyVig.forms.frames import PYVIG_FRAMES
#
#
#
#
from nettoolkit.compare_it.forms.compare_configs import *
#
from nettoolkit.configure.forms.config_by_excel import *
from nettoolkit.configure.forms.cred import *
#
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
#   Frames - tabs and its frame functions
# ---------------------------------------------------------------------------------------
MINITOOLS_FRAMES = {
	'1.Juniper': juniper_oper_frame(),
	'2.P/W Enc/Dec': pw_enc_decr_frame(),
	'3.MD5 Calculate': md5_calculator_frame(),
	'4.Compare-it': compare_config_texts_frame(),
}
IPSCANNER_FRAMES = {
	'1.Subnet Scanner': subnet_scanner_frame(),
	'2.Scan Compare': compare_scanner_outputs_frame(),
	'3.Create Batch': create_batch_frame(),
	'4.Summarize':summarize_prefixes_frame(),
	'5.Break Prefix':devide_prefixes_frame(),
	'6.isSubset':issubset_check_prefix_frame(),
}


CONFIGURE_FRAMES ={
	'1.Cred': exec_cred1_frame(),
	'2.Configure': exec_config_by_excel_frame(),
}

# ---------------------------------------------------------------------------------------
FRAMES = {}
FRAMES.update(MINITOOLS_FRAMES)
FRAMES.update(IPSCANNER_FRAMES)
FRAMES.update(CAPTUREIT_FRAMES)
FRAMES.update(FACTSFINDER_FRAMES)
FRAMES.update(J2CONFIG_FRAMES)
FRAMES.update(PYVIG_FRAMES)
FRAMES.update(CONFIGURE_FRAMES)
# ---------------------------------------------------------------------------------------

__all__ = [FRAMES]