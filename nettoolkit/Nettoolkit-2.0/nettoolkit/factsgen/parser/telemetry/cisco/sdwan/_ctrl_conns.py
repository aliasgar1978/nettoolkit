"""cisco show cdp neighbour command output parser """

# ------------------------------------------------------------------------------
import re

# ------------------------------------------------------------------------------
def parse_control_connections(cmd_op):
    """Parses 'show sdwan control connections' output reliably.

    Returns a dict keyed by color.
    """
    control_map = {}
    
    # Complete list of Cisco SD-WAN well-known colors
    well_known_colors = [
        "3g", "4g", "5g", "biz-internet", "blue", "bronze", "custom1", "custom2", 
        "custom3", "custom4", "custom5", "default", "gold", "green", "lte", 
        "metro-ethernet", "mpls", "private1", "private2", "private3", "private4", 
        "private5", "private6", "public-internet", "red", "silver"
    ]
    color_pattern = r"(" + "|".join(well_known_colors) + r")$"

    for line in cmd_op:
        line_clean = line.strip()
        
        # Skip headers and empty lines
        if not line_clean or "----" in line_clean or "PEER" in line_clean or "TYPE" in line_clean:
            continue
            
        # 1. extract the first 9 fields and rest into 'tail'
        match_leading = re.match(r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)$", line_clean)
        if not match_leading:
            continue
            
        peer_type    = match_leading.group(1)
        protocol     = match_leading.group(2)
        system_ip    = match_leading.group(3)
        site_id      = match_leading.group(4)
        domain_id    = match_leading.group(5)
        private_ip   = match_leading.group(6)
        private_port = match_leading.group(7)
        public_ip    = match_leading.group(8)
        public_port  = match_leading.group(9)
        tail         = match_leading.group(10).strip()
        
        # 2. remaining tail text
        tail_parts = tail.split()
        if not tail_parts:
            continue
            
        # 3. right side
        last_field = tail_parts[-1]
        
        # Detect if UPTIME - CONTROLLER GROUP ID merge together
        m = re.match( r"^(?P<uptime>\d+:\d+:\d+:\d+)(?P<gid>\d+)$", last_field )
        if m:
            group_id = m.group('gid')
            uptime = m.group('uptime')
            state = tail_parts[-2]
            proxy = tail_parts[-3]
            org_color_mix = " ".join(tail_parts[:-3])
        else:
            group_id = tail_parts[-1]
            uptime = tail_parts[-2]
            state = tail_parts[-3]
            proxy = tail_parts[-4]
            org_color_mix = " ".join(tail_parts[:-4])

        # Organization and Color
        color_match = re.search(color_pattern, org_color_mix, re.IGNORECASE)
        if color_match:
            color = color_match.group(1)
            org = org_color_mix[:color_match.start()].strip()
        else:
            color = "unknown"
            org = org_color_mix.strip()

        # update
        control_map.setdefault(color, []).append(
            {
                "peer_type": peer_type,
                "peer_public_ip": public_ip,
                "peer_private_ip": private_ip,
                "peer_system_ip": system_ip,
                "protocol": protocol,
                "state": state,
                "uptime": uptime,
                "org": org,
                "group_id": group_id
            }
        )

    return control_map

# ------------------------------------------------------------------------------

def get_ctrl_conns(cmd_op, *args):
    op_dict = parse_control_connections(cmd_op)  or {}
    return {'op_dict': op_dict }
