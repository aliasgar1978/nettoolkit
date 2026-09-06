
import re


def get_chassis_hardware(cmd_op: list) -> dict:
    """Parses 'show chassis hardware' output to extract global identity details.
    
    Returns a unified root-level hardware object structure.
    """
    payload = {
        "hardware": {}
    }

    for line in cmd_op:
        line = line.strip()
        if not line:
            continue
            
        spl = line.split()
        if not spl:
            continue

        # Extract Chassis Serial Number using explicit index checking
        if spl[0].lower() == "chassis":
            try:
                payload["hardware"]["serial"] = spl[-2]
            except IndexError:
                pass
            break  # Exit early once root chassis serial is captured

    return {'op_dict': payload}

def get_chassis_hardware_ports(cmd_op: list) -> dict:
    """Parses 'show chassis hardware' output to extract physical port modules.
    
    Isolates transceiver mapping details into an intermediate layout for 
    clean downstream interface blending.
    """
    payload = {
        "transceiver_map": {}
    }
    
    fpc_id = ""
    pic_id = ""

    for line in cmd_op:
        line = line.strip()
        if not line:
            continue
            
        spl = line.split()
        if not spl:
            continue

        token_type = spl[0].upper()
        if token_type not in ("FPC", "PIC", "XCVR"):
            continue

        if len(spl) < 2:
            continue

        if token_type == "FPC":
            fpc_id = spl[1]
            pic_id = ""
            
        elif token_type == "PIC":
            pic_id = fpc_id + "/" + spl[1]
            
        elif token_type == "XCVR":
            if pic_id:
                port_idx = spl[1]
                normalized_path = fpc_id + "/" + spl[1] if "/" in port_idx else pic_id + "/" + port_idx
                # Store media description mapped to its structural hardware slot path
                payload["transceiver_map"][normalized_path] = spl[-1]

    return {'op_dict': payload}




def merge_juniper_transceivers_to_interfaces(interfaces_db, transceiver_map):
    """
    Uses regular expressions to extract port identifiers (e.g., 0/0/0) 
    from full Junos interface strings and maps them straight to the transceiver dataset.
    """
    transceiver_map = transceiver_map['transceiver_map']
    if not interfaces_db or not transceiver_map:
        return interfaces_db

    # Navigate down to your core physical interfaces collection layer safely
    if 'interfaces' in interfaces_db and 'physical' in interfaces_db['interfaces']:
        physical_ports = interfaces_db['interfaces']['physical']
    else:
        physical_ports = interfaces_db.get('physical', interfaces_db)

    if not isinstance(physical_ports, dict):
        return interfaces_db

    # REVERSED LOOP: Start with the bare transceiver port keys (e.g., '0/0/0')
    for bare_port, sfp_type in transceiver_map.items():
        if not sfp_type:
            continue

        sfp_upper = sfp_type.upper()
        
        # 1. Collect ALL possible interface matches for this specific slot number
        # e.g., if bare_port is '0/0/0', matches might be ['ge-0/0/0', 'xe-0/0/0']
        port_pattern = re.compile(rf'-.*{re.escape(bare_port)}(\b|\.|$)')
        candidate_interfaces = [if_name for if_name in physical_ports.keys() if port_pattern.search(if_name)]

        if not candidate_interfaces:
            continue

        # 2. RESOLUTION ENGINE FOR DUAL-SPEED / COLLISION PORTS
        target_if_name = None

        if len(candidate_interfaces) == 1:
            # If only one port prefix option exists in the config text, use it directly
            target_if_name = candidate_interfaces[0]
        else:
            # Collision detected! Evaluate the active configuration profile state
            active_candidates = []
            
            for if_name in candidate_interfaces:
                port_block = physical_ports[if_name]
                
                # An interface is considered "active" if it has configured logical units, 
                # descriptions, or isn't administratively shut down.
                has_units = 'units' in port_block and len(port_block['units']) > 0
                is_admin_up = port_block.get('state', {}).get('admin', 'up') != 'down'
                has_desc = port_block.get('description') is not None
                
                if has_units or has_desc:
                    if is_admin_up:
                        active_candidates.append(if_name)

            if len(active_candidates) == 1:
                target_if_name = active_candidates[0]
            elif len(active_candidates) > 1:
                # If multiple active profiles exist (rare configuration anomaly),
                # prefer the faster media lane (xe- or et-) for the transceiver metrics
                faster_ports = [i for i in active_candidates if i.startswith('xe-') or i.startswith('et-')]
                target_if_name = faster_ports[0] if faster_ports else active_candidates[0]
            else:
                # If all candidate profiles are unconfigured placeholders, default to the faster string lane
                faster_ports = [i for i in candidate_interfaces if i.startswith('xe-') or i.startswith('et-')]
                target_if_name = faster_ports[0] if faster_ports else candidate_interfaces[0]

        # 3. Inject the transceiver metadata safely into the resolved target interface node container
        if target_if_name:
            target_port_node = physical_ports[target_if_name]
            if isinstance(target_port_node, dict):
                if 'transceiver' not in target_port_node:
                    target_port_node['transceiver'] = {}
                target_port_node['transceiver']['sfp_type'] = sfp_type

    return interfaces_db
