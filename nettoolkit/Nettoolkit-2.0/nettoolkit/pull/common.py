
# --------------------------------------------------------------------------------

import ipaddress
import time
import re
import logging

# ------------------------------------------------------------------------------

def clean_hostname(prompt):
    raw = prompt.rstrip('#>]$ ').strip()
    if '@' in raw:
        raw = raw.split('@')[-1]
    if '(' in raw:
        raw = raw.split('(')[0]
    return raw.strip()

# ------------------------------------------------------------------------------

def is_valid_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

def extract_ip_from_text(text):
    tokens = re.findall(r'[0-9a-fA-F:\.]+', text)
    for token in tokens:
        token = token.strip(':.')
        try:
            ipaddress.ip_address(token)
            return token
        except ValueError:
            continue
            
    return None

def get_device_ip_using_nlist(ssh_shell, target):
    if is_valid_ip(target):
        return target

    logging.info(f"[*] Resolving hostname '{target}' via jump server...")
    
    # 1. Try 'nlist'
    ssh_shell.send(f"nlist {target}\n")
    time.sleep(2)
    output = ssh_shell.recv(10000).decode('utf-8', errors='ignore')
    resolved_ip = extract_ip_from_text(output)
    
    if resolved_ip:
        logging.info(f"[+] Resolved {target} to: {resolved_ip}")
        return resolved_ip
    else:
        raise ValueError(f"[-] Could not extract a valid IPv4/IPv6 address for hostname: {target}")

# ------------------------------------------------------------------------------

def strip_ansi_and_clean(text):
    """
    Removes ANSI escape codes, terminal control characters (like vt100 formatting),
    and normalizes carriage returns for clean text files.
    """
    # Regex to match ANSI escape sequences (e.g., \x1b[?7h, \x1b[m, \x1b[2J)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', text)
    
    # Strip common terminal control artifacts character backspaces or terminal queries
    cleaned = re.sub(r'\x1b\[\?\d+[hl]', '', cleaned)
    
    # Normalize Windows/Network line endings (\r\n) to simple lines (\n)
    return cleaned.replace('\r\n', '\n').replace('\r', '\n')

# --------------------------------------------------------------------------------

def wait_for_prompt(channel, timers_dict):
    timeout = timers_dict.get('prompt_timeout', 60)

    output = ""
    start = time.time()

    while time.time() - start < timeout:

        if channel.recv_ready():
            output += channel.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )

            if output.rstrip().endswith( ("#", ">", "$", ":") ):
                return output

        time.sleep(0.5)

    return output

def wait_for_output(channel, command, timers_dict):
    timeout = timers_dict.get('command_timeout', 15)

    output = ""
    idle = 0

    channel.send(f"{command}\n")

    while idle < 3 and timeout > 0:
        if channel.recv_ready():
            output += channel.recv(65535).decode(
                "utf-8",
                errors="ignore"
            )
            idle = 0
        else:
            idle += 1
            timeout -= 1
            time.sleep(1)

    return output

# --------------------------------------------------------------------------------

def drain_buffer(channel):
    output = b''
    while channel.recv_ready():
        output += channel.recv(65535)
    return output.decode('utf-8', errors='ignore')

def send_break(channel):
    channel.send("\x03")
    time.sleep(0.5)
    return drain_buffer(channel)

# --------------------------------------------------------------------------------

