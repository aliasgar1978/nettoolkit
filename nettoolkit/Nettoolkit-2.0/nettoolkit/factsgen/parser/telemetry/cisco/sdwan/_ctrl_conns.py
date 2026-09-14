"""cisco show cdp neighbour command output parser """

# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------

def parse_control_connections(cmd_op):
    """Parses 'show sdwan control connections' output.

    Returns a dict keyed by public_ip.
    """
    control_map = {}
    control_pattern = re.compile(
        r"^(?P<peer_type>\S+)\s+"
        r"(?P<protocol>\S+)\s+"
        r"(?P<system_ip>\S+)\s+"
        r"(?P<site_id>\d+)\s+"
        r"(?P<domain_id>\d+)\s+"
        r"(?P<private_ip>\S+)\s+"
        r"(?P<private_port>\d+)\s+"
        r"(?P<public_ip>\S+)\s+"
        r"(?P<org>.+?)\s{2,}"  # Matches text with spaces, looks for at least 2 trailing spaces
        r"(?P<color>\S+)\s+"
        r"(?P<proxy>\S+)\s+"
        r"(?P<state>\S+)\s+"
        r"(?P<uptime>\S+)"
    )

    for line in cmd_op:
        line_clean = line.strip()
        if not line_clean or "----" in line_clean or "PEER TYPE" in line_clean:
            continue
        if match := control_pattern.match(line.strip()):
            data = match.groupdict()
            color = data["color"]

            # Initialize a list of connections for this public IP if not exists
            if color not in control_map:
                control_map[color] = []

            control_map[color].append(
                {
                    "peer_type": data["peer_type"],
                    "peer_public_ip": data["public_ip"],
                    "peer_private_ip": data["private_ip"],
                    "peer_system_ip": data["system_ip"],
                    "protocol": data["protocol"],
                    "state": data["state"],
                    "uptime": data["uptime"],
                }
            )

    return control_map


# ------------------------------------------------------------------------------

def get_ctrl_conns(cmd_op, *args):
    op_dict = parse_control_connections(cmd_op)  or {}
    return {'op_dict': op_dict }
