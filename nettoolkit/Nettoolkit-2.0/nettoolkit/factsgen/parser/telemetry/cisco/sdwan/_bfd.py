# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------

def parse_bfd_sessions(cmd_op):
    """Parses 'show sdwan bfd sessions' output.
    Returns a dict keyed by 'local_color'.
    """
    bfd_map = {}

    bfd_pattern = re.compile(
        r"^(?P<peer_system_ip>\S+)\s+"
        r"(?P<peer_id>\d+)\s+"
        r"(?P<state>\S+)\s+"
        r"(?P<local_color>\S+)\s+"
        r"(?P<remote_color>\S+)\s+"
        r"(?P<source_ip>\S+)\s+"
        r"(?P<dst_public_ip>\S+)\s+"
        r"(?P<dst_public_port>\d+)\s+"
        r"(?P<encap>\S+)"
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "----" in line_clean
            or "SYSTEM IP" in line_clean
            or "SOURCE" in line_clean
        ):
            continue

        if match := bfd_pattern.match(line_clean):
            data = match.groupdict()
            color_key = data.pop("local_color") 

            if color_key not in bfd_map:
                bfd_map[color_key] = []

            bfd_map[color_key].append(
                {
                    "peer_system_ip": data["peer_system_ip"],
                    "peer_site_id": data["peer_id"],
                    "bfd_state": data["state"],
                    "remote_color": data["remote_color"],
                    "source_ip": data["source_ip"],
                    "dst_public_ip": data["dst_public_ip"],
                    "dst_public_port": data["dst_public_port"],
                    "encapsulation": data["encap"],
                }
            )

    return bfd_map

# ------------------------------------------------------------------------------

def get_bfd_sessions(cmd_op, *args):
    bfd_sessions_dict = parse_bfd_sessions(cmd_op)
    bfd_sessions = {}
    if bfd_sessions_dict:
        bfd_sessions = {'bfd_sessions': bfd_sessions_dict}
    return {'op_dict': bfd_sessions }
