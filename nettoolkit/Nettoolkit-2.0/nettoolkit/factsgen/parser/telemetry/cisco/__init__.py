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
	'show version'               : (
        ('system', get_version),
    ),
	'show interfaces description': (
        ('interfaces', get_interface_description),
    ),
	'show interfaces status'     : (
        ('interfaces', get_interface_status),
    ),
	'show cdp neighbors'         : (
        ('interfaces', get_cdp_neighbour),
	),
	'show lldp neighbors'        : (
        ('interfaces', get_lldp_neighbour),
	),
	'show mac address-table'     : (
        ('interfaces', get_mac_table),
	),
	'show ip arp'                : (
        ('interfaces', get_arp_table),
	),
}
