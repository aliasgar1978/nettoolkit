"""
This python based project help generating yaml database of network device .

"""

# ------------------------------------------------------------------------------

from .interface_lldp_neighbors import get_lldp_neighbour
from .interface_cdp_neighbors  import get_cdp_neighbour
from .interface_status         import get_interface_status
from .interface_descriptions   import get_interface_description
from .interface_arp_table      import get_arp_table
from .interface_mac_table      import get_mac_address_table
from .interface_run            import get_interfaces_running

from .system_version           import get_version
from .system_run               import get_system_running

from .bgp_run                  import get_bgp_running

from .vrf_run                  import get_vrfs_running

from .ospf_run                 import get_ospf_running

from .statics_run              import get_system_running_routes

from .prefix_list_run          import get_system_running_prefix_lists

# ------------------------------------------------------------------------------

