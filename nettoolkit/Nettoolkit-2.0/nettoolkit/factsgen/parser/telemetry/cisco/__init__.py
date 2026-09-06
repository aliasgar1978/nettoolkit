"""Cisco Specific Command Parser Functions/Classes for device telemetry
and its map with commands
"""


# // HERE IS ALL PARSER FUNCTIONS //
from ._cdp import get_cdp_neighbour
from ._lldp import get_lldp_neighbour
from ._int_status import get_interface_status
from ._int_description import get_interface_description
from ._mac_table import get_mac_table
from ._arp_table import get_arp_table
from ._version import get_version

#

#
CISCO_CMD_REGISTER = {
	'show lldp neighbors': (get_lldp_neighbour,),
	'show cdp neighbors': (get_cdp_neighbour, ),
	'show interfaces status': (get_interface_status, ),
	'show interfaces description': (get_interface_description, ),
	'show mac address-table': (get_mac_table, ),
	'show ip arp' : (get_arp_table, ),
	'show version': (get_version, ),	
}

CISCO_CMD_SECTION = {
	'show version': ('system', ),	
	'show interfaces description': ('interfaces', ),
	'show interfaces status': ('interfaces', ),
	'show cdp neighbors': ('interfaces', ),
	'show lldp neighbors': ('interfaces',),
	'show mac address-table': ('interfaces', ),
	'show ip arp' : ('interfaces', ),
}
