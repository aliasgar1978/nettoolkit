# OUTPUT SHOULD BE UNFILTERED ( HEADER ROW REQUIRED IN OUTPUT )
"""cisco show interface status command output parser """

# ------------------------------------------------------------------------------

from nettoolkit.cmn.fstr import blank_line, get_string_part, if_standardize, get_cisco_int_type, get_string_trailing
# ------------------------------------------------------------------------------

def get_interface_status(cmd_op, *args):
    """parser - show int status command output

    Parsed Fields:
        * port/interface
        * port_type
        * duplex
        * speed
        * port_status

    Args:
        cmd_op (list, str): command output in list/multiline string.

    Returns:
        dict: output dictionary with parsed fields
    """	
    # cmd_op = command output in list/multiline string.
    int_status_dict = {}
    header_parsed = False
    for l in cmd_op:
        if blank_line(l): continue
        if l.strip().startswith("!"): continue
        if l.strip().startswith("^"): 
            print('[-] missing or invalid input  show interface status, skipped')			
            return int_status_dict

        # // HEADER ROW // #
        # Dynamically compute fixed-width column boundaries from the header row
        if l.startswith("Port"):
            type_begin_at = l.find("Type")
            duplex_begin = l.find("Duplex")
            duplex_end = duplex_begin + 6
            speed_begin = duplex_end
            speed_end = speed_begin + 7
            access_vlan_begin = l.find("Vlan")
            status_begin = l.find("Status")
            status_end = access_vlan_begin - 1
            header_parsed = True 
            continue

        if not header_parsed: continue

        # // DATA TABLE ROWS //
        spl = l.strip().split()
        p = if_standardize(spl[0])
        filter = get_cisco_int_type(p)
        if not int_status_dict.get(filter):
            int_status_dict[filter] = {}
        port_type_dict = int_status_dict[filter]
        port_type_dict[p] = {}
        port = port_type_dict[p]

        # Extract raw string fields cleanly
        raw_status = get_string_part(l, status_begin, status_end).strip().lower()
        
        # --- CONVERTING OPERATIONAL LINK STATES CLEARLY ---
        # 'connected' = physical link is up & protocol is up (up/up)
        # 'notconnect' = admin is up, but physical cable is missing/unplugged (up/down)
        # 'disabled' = admin is explicitly shut down via configuration (down/down)
        state = 'up'
        admin_state = 'up'
        is_err_disabled = False
        
        if 'disabled' in raw_status:
            if 'err' in raw_status:
                admin_state = 'up'
                protocol_state = 'down'
                is_err_disabled = True
            else:
                admin_state = 'down'
                protocol_state = 'down'

        elif 'notconnect' in raw_status:
            admin_state = 'up'
            protocol_state = 'down'
        
        # Nest metrics into the modern object schema block layouts uniformly
        # port['link_status'] = raw_status  # Captures literal 'connected', 'notconnect', etc.
        port['state'] = {
            'admin': admin_state,          # administratively configured state
            'protocol': state             # live line protocol operational state
        }
        if is_err_disabled:
            port['state']['err_disabled'] = True

        port['hardware'] = {
            'media_type': get_string_trailing(l, type_begin_at).strip(),
            'duplex': get_string_part(l, duplex_begin, duplex_end).strip(),
            'speed': get_string_part(l, speed_begin, speed_end).strip(),
        }
    
    return {'op_dict': int_status_dict }
# ------------------------------------------------------------------------------
