"""Cisco Specific Command Parser Functions/Classes for device telemetry
and its map with commands
"""


# // HERE IS ALL PARSER FUNCTIONS //
from ._ctrl_conns import get_ctrl_conns
from ._ctrl_local_prop import get_ctrl_local_prop, merge_control_conn_local_prop
from ._bfd import get_bfd_sessions
from ._omp import get_omp_peers, get_omp_routes, get_omp_tlocs
from ._system import get_sdwan_system, get_sdwan_software, get_license_summary

# merge_control_conn_local_prop --> exceptional for merging later on.
#
#
CISCO_SDWAN_CMD_REGISTER = {

	'show sdwan control connections': (
        ('sdwan', get_ctrl_conns),
    ),
    
	'show sdwan control local-properties': (
        ('sdwan', get_ctrl_local_prop),
    ),

    'show sdwan bfd sessions': (
        ('sdwan', get_bfd_sessions),
    ),

    'show sdwan omp peers': (
        ('sdwan', get_omp_peers),
    ),

    'show sdwan omp routes': (
        ('sdwan', get_omp_routes),
    ),

    'show sdwan omp tlocs': (
        ('sdwan', get_omp_tlocs),
    ),

    'show sdwan system': (
        ('sdwan', get_sdwan_system),
    ),

    'show sdwan software': (
        ('sdwan', get_sdwan_software),
    ),

    'show license summary': (
        ('sdwan', get_license_summary),
    ),

}

