"""Juniper Specific Command Parser Functions/Classes
And its map wiht show commands
"""



# // HERE IS ALL PARSER FUNCTIONS //
from ._system import get_system
from ._interfaces import get_interfaces
from ._instances import get_instances
from ._bgp import get_bgps
from ._ospf import get_ospfs
from ._routes import get_routes
from ._prefix_lists import get_prefix_lists


JUNIPER_CMD_REGISTER = {
	'show configuration':(
		get_system,
		get_interfaces,
		get_instances,
		get_bgps, 
		get_ospfs,
		get_routes,
		get_prefix_lists,
	),
}

JUNIPER_CMD_SECTION = {
	'show configuration':(
		'system',
		'interfaces',
		'instances',
		'routing', 
		'routing', 
		'routes', 
		'prefixes',
	),
}

