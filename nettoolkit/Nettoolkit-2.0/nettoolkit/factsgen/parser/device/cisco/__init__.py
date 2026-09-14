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


## Registeredcommand: ( (Section , function), ... ) ##
CISCO_CMD_REGISTER = {
	'show running-config': (
		('interfaces', get_interfaces,    ),
		('routing',    get_bgp,           ),
		('routing',    get_ospf,          ),
		('instances',  get_vrfs,          ),
		('system',     get_system,        ),
		('routes',     get_routes,        ),
		('prefixes',   get_prefix_lists,  ),        
	)
}
