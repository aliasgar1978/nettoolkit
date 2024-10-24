"""Description: 
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from dataclasses import dataclass, field
from collections import OrderedDict
from nettoolkit.nettoolkit_common import *
from nettoolkit.nettoolkit_common.gpl import *
from nettoolkit.addressing import to_dec_mask, invmask_to_mask, addressing

from nettoolkit.facts_finder.generators.commons import *
from nettoolkit.facts_finder.generators.juniper.common import *

from nettoolkit.pyNetCrypt import juniper_decrypt

# ==============================================================================================
#  Local Statics
# ==============================================================================================
merge_dict = DIC.merge_dict


# ==============================================================================================
#  Local Functions
# ==============================================================================================

def get_int_port_dict(op_dict, port):
	int_filter = get_juniper_int_type(port).lower()
	if not op_dict.get(int_filter):
		op_dict[int_filter] = {}
	int_filter_dict = op_dict[int_filter]
	#
	if port.startswith("irb."): 
		port=int(port[4:])
	elif port.startswith("ae") or port.startswith("lo"): 
		port=port[2:]
	#
	if not int_filter_dict.get(port): 
		int_filter_dict[port] = {}
	return int_filter_dict[port]



# ==============================================================================================
#  Classes
# ==============================================================================================



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
