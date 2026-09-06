
# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from collections import OrderedDict	
from re import compile


intBeginWith = compile(r'^\D+')
# ------------------------------------------------------------------------------
# Standard number of characters for identifing interface short-hand
# ------------------------------------------------------------------------------
PHYSICAL_IFS = OrderedDict()
PHYSICAL_IFS.update({
		'Ethernet': 2, 
		'FastEthernet': 2,
		'GigabitEthernet': 2, 
		'TenGigabitEthernet': 2, 
		'FortyGigabitEthernet':2, 
		'HundredGigE':2,
		'AppGigabitEthernet': 2,
		'mgmt': 4,
		'Async': 5,
})
PHYSICAL_IFS['TwoGigabitEthernet'] = 3     # Do not alter sequence of these two.
PHYSICAL_IFS['TwentyFiveGigE'] = 3  # ....
CISCO_IFSH_IDENTIFIERS = {
	"l3vlan": {'Vlan':2,},
	"tunnel": {'Tunnel':2,},
	"loopback": {'Loopback':2,} ,
	"aggregated": {'Port-channel':2,},
	"physical": PHYSICAL_IFS,
	"nvi": {'NVI':2,},
	"nv": {'NV':2,},
}
JUNIPER_IFS_IDENTIFIERS = {
	"l3vlan": ('irb', 'vlan', 'iw'),
	"loopback": ('lo', ),
	"range": ('interface-range', ),
	"tunnel": ('lt', 'gr', 'ip', 'mt', 'vt', 'vtep', 'xt' ),
	"aggregated": ('ae', 'as', 'fc'),
	"physical": ('fe', 'ge', 'xe', 'et', 'xle', 'fte', ),
	"management": ('mg', 'em', 'me', 'fxp', 'vme', 'bme', 'bm'),
	"internal": ('sxe', 'bcm', 'cp', 'demux', 'dsc', 'es', 'gre', 'ipip', 'ixgbe', 'lc','lsi', 'mo',
		'ms', 'pd', 'pimd', 'rlsq', 'rms', 'rsp', 'sp', 'tap', 'umd', 'vsp', 'vc4',  ),
	"circuit": ('at', 'cau4', 'ce1', 'coc1', 'coc3', 'coc12', 'coc48', 'cstm1', 'cstm4', 'cstm16', 
		'ct1', 'ct3', 'ds', 'e1', 'e3', 'ls', 'ml', 'oc3', 'pip', 'se', 'si',  'so', 'stm1', 'stm4', 'stm16',
		't1', 't3',    ),
	"monitoring": ('dfc', ),
}

# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------

