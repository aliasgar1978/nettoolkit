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
		('system',      get_system,       ),
		('interfaces',  get_interfaces,   ),
		('instances',   get_instances,    ),
		('routing',     get_bgps,         ),
		('routing',     get_ospfs,        ),
		('routes',      get_routes,       ),
		('prefixes',    get_prefix_lists, ),
	),
}
