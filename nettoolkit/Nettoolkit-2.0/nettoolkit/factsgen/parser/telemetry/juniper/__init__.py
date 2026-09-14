"""Juniper Specific Command Parser Functions/Classes
And its map wiht show commands
"""

# // HERE IS ALL PARSER FUNCTIONS //
from ._lldp import get_lldp_neighbour
from ._int_description import get_int_description
from ._chassis_hardware import get_chassis_hardware, get_chassis_hardware_ports, merge_juniper_transceivers_to_interfaces
from ._arp_table import get_arp_table
from ._mac_table import get_mac_table
from ._version import get_version
from ._int_terse import get_interface_terse

## Note: merge_juniper_transceivers_to_interfaces ( Adhoc not REGISTERED & SECTION FUNCTION ) USED SEPARATELY TO MERGE DATA WITH INTERFACE


JUNIPER_CMD_REGISTER = {
	'show version'                 : (('system'        , get_version),                ),
	'show interfaces descriptions' : (('interfaces'    , get_int_description),        ),
	'show lldp neighbors'          : (('interfaces'    , get_lldp_neighbour),         ),
	'show chassis hardware'        : (('system'        , get_chassis_hardware), 
                                      ('hardware_ports', get_chassis_hardware_ports), ),
	'show interfaces terse'        : (('interfaces'    , get_interface_terse),        ),
	'show arp'                     : (('interfaces'    , get_arp_table),              ),
    'show ethernet-switching table': (('interfaces'    , get_mac_table),              ),
	# 'show bgp summary'           : (('routing',),                                   ),
}
