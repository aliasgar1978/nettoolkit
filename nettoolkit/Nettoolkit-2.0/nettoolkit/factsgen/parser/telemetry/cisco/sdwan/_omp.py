# ------------------------------------------------------------------------------
from collections import defaultdict
import re


def parse_omp_peers_flat(cmd_op):
    """Parses 'show sdwan omp peers' output.
    Returns a simple flat list of dictionaries containing all entries.
    """
    omp_list = []
    omp_pattern = re.compile(
        r"^(?P<peer_ip>\S+)\s+"
        r"(?P<type>\S+)\s+"
        r"(?P<site_id>\d+)\s+"
        r"(?P<domain_id>\d+)\s+"
        r"(?P<state>\S+)\s+"
        r"(?P<uptime>\S+)\s+"
        r"(?P<flaps>\d+)"
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "----" in line_clean
            or "PEER" in line_clean
            or "TYPE" in line_clean
        ):
            continue

        if match := omp_pattern.match(line_clean):
            omp_list.append(match.groupdict())

    return omp_list


# -------------------------------------------------------------------------------------

def parse_omp_routes_flat(cmd_op):
    """Parses 'show sdwan omp routes' output.
    Returns a flat list of dictionaries containing all prefixes and paths.
    """
    routes_list = []
    routes_pattern = re.compile(
        r"^(?P<vpn>\d+)\s+"
        r"(?P<prefix>\S+)\s+"
        r"(?P<from_peer>\S+)\s+"
        r"(?P<tloc_ip>\S+)\s+"
        r"(?P<color>\S+)\s+"
        r"(?P<encap>\S+)\s+"
        r"(?P<status>[a-zA-Z,]+)"
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "---" in line_clean
            or "VPN" in line_clean
            or "PREFIX" in line_clean
            or "Status codes:" in line_clean
            or line_clean.startswith("C = chosen")
            or line_clean.startswith("I = installed")
        ):
            continue

        if match := routes_pattern.match(line_clean):
            routes_list.append(match.groupdict())

    return routes_list

# ------------------------------------------------------------------------------

def parse_omp_tlocs_by_color(cmd_op):
    grouped_data = defaultdict(list)
    pattern = re.compile(
        r'^(?P<system_ip>\d{1,3}(?:\.\d{1,3}){3})\s+'
        r'(?P<color>[\w\-]+)\s+'
        r'(?P<encap>\w+)\s+'
        r'(?P<status>\w+)\s+'
        r'(?P<type>\w+)\s+'
        r'(?P<from_peer>\d{1,3}(?:\.\d{1,3}){3})\s+'
        r'(?P<peer_status>\w+)', 
        re.MULTILINE
    )
    
    for line in cmd_op:
        match = pattern.match(line.strip())
        if match:
            tloc_details = match.groupdict()
            color = tloc_details.pop("color") 
            grouped_data[color].append(tloc_details)
            
    return dict(grouped_data)

# --------------------------------------------------------------------------------------

def get_omp_peers(cmd_op, *args):
    omp_peers_dict = parse_omp_peers_flat(cmd_op)
    omp_peers = {}
    if omp_peers_dict:
        omp_peers = {'omp_peers': omp_peers_dict}
    return {'op_dict': omp_peers }

def get_omp_routes(cmd_op, *args):
    omp_routes_dict = parse_omp_routes_flat(cmd_op)
    omp_routes = {}
    if omp_routes_dict:
        omp_routes = {'omp_routes': omp_routes_dict}
    return {'op_dict': omp_routes }

def get_omp_tlocs(cmd_op, *args):
    omp_tlocs_dict = parse_omp_tlocs_by_color(cmd_op)
    omp_tlocs = {}
    if omp_tlocs_dict:
        omp_tlocs = {'omp_tlocs': omp_tlocs_dict}
    return {'op_dict': omp_tlocs }

# ------------------------------------------------------------------------------
