"""cisco show cdp neighbour command output parser """

# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------

def parse_cedge_xe_local_properties(cmd_op):
    """Parses 'show sdwan control local-properties'.
    Returns a clean dictionary keyed directly by the 'public_ip' string.
    """
    parsed_data = {
        "system": {
            "organization_name": "none",
            "site_id": "none",
            "system_ip": "none",
            "chassis": "none",
            "serial": "none",
            "cert_serial": "none",
        },
        "interfaces": {},
    }

    meta_patterns = {
        "organization_name": re.compile(
            r"^organization-name\s+(.+)$", re.IGNORECASE
        ),
        "site_id": re.compile(r"^site-id\s+(\d+)$", re.IGNORECASE),
        "system_ip": re.compile(r"^system-ip\s+([\d.]+)$", re.IGNORECASE),
        "chassis": re.compile(
            r"^chassis-num/unique-id\s+(\S+)$", re.IGNORECASE
        ),
        "cert_serial": re.compile(r"^serial-num\s+(\S+)$", re.IGNORECASE),
        "serial": re.compile(r"^subject-serial-num\s+(\S+)$", re.IGNORECASE),
    }
    interface_pattern = re.compile(
        r"^(?P<interface>[a-zA-Z0-9/.\-]+)\s+"
        r"(?P<public_ip>[0-9.]+)\s+"
        r"(?P<public_port>\d+)\s+"
        r"(?P<private_ip>[0-9.]+)\s+"
        r"(?P<private_ipv6>\S+)\s+"  # Handles '::' or an actual IPv6 address
        r"(?P<private_port>\d+)\s+"
        r"\S+\s+"  # Skips VS/VM counters (e.g., 2/1, 2/0)
        r"(?P<color>\S+)\s+"
        r"(?P<state>\S+)\s+"
        r".*$"  # Safely matches/skips all remaining variable-width trailing flags/timers
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "----" in line_clean
            or "PUBLIC" in line_clean
            or "MAX" in line_clean
            or "TNL" in line_clean
            ):
            continue

        meta_found = False
        for key, pattern in meta_patterns.items():
            if match_meta := pattern.match(line_clean):
                parsed_data["system"][key] = match_meta.group(1).strip()
                meta_found = True
                break

        if meta_found:
            continue

        if "INTERFACE" in line_clean:
            continue

        if match := interface_pattern.match(line_clean):
            data = match.groupdict()
            color = data["color"]

            parsed_data['interfaces'][color] = {
                "interface": data["interface"],
                # "color": data["color"],
                "state": data["state"],
                "private_ip": data["private_ip"],
                "private_port": data["private_port"],
                "public_ip": data["public_ip"],
                "public_port": data["public_port"],
            }

    return parsed_data

# def parse_local_properties(cmd_op):
#     """Parses 'show sdwan control local-properties' output.

#     Returns a dict keyed by public_ip.
#     """
#     local_map = {}
#     local_pattern = re.compile(
#         r"^(?P<interface>[a-zA-Z0-9/.\-]+)\s+"  # Matches ge0/0, ge0/1.100, etc.
#         r"(?P<color>\S+)\s+"
#         r"(?P<state>\S+)\s+"
#         r"\d+\s+no\s+\S+\s+no\s+\S+\s+"  # Skips VNM, PROXY, RESTRICT, STUN, LOW BNDWD
#         r"(?P<private_ip>\S+)\s+"
#         r"(?P<private_port>\d+)\s+"
#         r"(?P<public_ip>\S+)\s+"
#         r"(?P<public_port>\d+)"
#     )

#     for line in cmd_op:
#         line_clean = line.strip()
#         if (
#             not line_clean
#             or "----" in line_clean
#             or "INTERFACE" in line_clean
#             or "personality" in line_clean
#             or "system-ip" in line_clean
#             or "site-id" in line_clean
#             or "domain-id" in line_clean
#             or "organization-name" in line_clean
#             ):
#             continue

#         if match := local_pattern.match(line.strip()):
#             data = match.groupdict()
#             pub_ip = data["public_ip"]

#             local_map[pub_ip] = {
#                 "interface": data["interface"],
#                 "color": data["color"],
#                 "state": data["state"],
#                 "private_ip": data["private_ip"],
#                 "private_port": data["private_port"],
#                 "public_port": data["public_port"],
#             }

#     return local_map



# ------------------------------------------------------------------------------

def get_ctrl_local_prop(cmd_op, *args):
    op_dict = parse_cedge_xe_local_properties(cmd_op)  or {}
    return {'op_dict': op_dict }


# =============================================================================

def merge_control_conn_local_prop(parsed_controls, parsed_local_props):
    final_merged_dict = {}
    for color, interface_data in parsed_local_props['sdwan']['interfaces'].items():
        intf_name = interface_data.pop("interface")
        interface_data["color"] = color
        interface_data["active_control_connections"] = parsed_controls['sdwan'].get(
            color, []
        )

        final_merged_dict[intf_name] = interface_data
    return {"wan_connections": final_merged_dict}
