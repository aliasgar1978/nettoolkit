"""Cisco Specific Command Parser Functions/Classes
and its map with commands
"""


# // HERE IS ALL PARSER FUNCTIONS //
from ._interfaces import get_interfaces
from ._bgp import get_bgp
from ._ospf import get_ospf
from ._vrfs import get_vrfs
from ._system import get_system
from ._routes import get_routes
from ._prefix_list import get_prefix_lists


CISCO_CMD_REGISTER = {
	'show running-config': (
		get_interfaces, 
		get_bgp, 
		get_ospf,
		get_vrfs, 
		get_system, 
		get_routes,
		get_prefix_lists,
	),
}

CISCO_CMD_SECTION = {
	'show running-config': (
		'interfaces', 
		'routing', 
		'routing',
		'instances', 
		'system', 
		'routes',
		'prefixes',
	),
}
