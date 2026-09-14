
import time
import logging
from nettoolkit.cmn.fio import read_yaml
from pathlib import Path


CHAR_YAML = Path(__file__).with_name('characteristics.yaml')

def get_signature_terminal_len(output_lowered):
    d = read_yaml(CHAR_YAML).get('vendors', {})
    for vendor, ven_dict in d.items():
        for item in ven_dict.get('signatures'):
            if item in output_lowered:
                return vendor, ven_dict.get('terminal_length')
    return None, None

def get_timers():
    return read_yaml(CHAR_YAML).get('timers', {})
    
def wait_for_prompt(channel, timeout=None):
    if not timeout:
        timeout = get_timers().get('prompt_timeout', 60)

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

def wait_for_output(channel, timeout=None):
    if not timeout:
        timeout = get_timers().get('command_timeout', 15)

    output = ""
    idle = 0

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

def send_and_wait(channel, command, wait_time=60, buffer_size=65535):
    """Sends a command to the channel and waits to collect all available output."""
    channel.send(f"{command}\n")
    return wait_for_output(channel, wait_time)

def drain_buffer(channel):
    output = b''
    while channel.recv_ready():
        output += channel.recv(65535)
    return output.decode('utf-8', errors='ignore')

def send_break(channel):
    channel.send("\x03")
    time.sleep(0.5)
    return drain_buffer(channel)

def determine_vendor_profile(device_shell):

    # 1. Wake up channel and read the initial prompt environment
    device_shell.send("\n")
    time.sleep(1.0)
    initial_prompt = ""
    while device_shell.recv_ready():
        initial_prompt += device_shell.recv(4096).decode('utf-8', errors='ignore')
    
    initial_prompt_lower = initial_prompt.lower()
    logging.info(f"[*] Initial system environment: {initial_prompt.strip()}")

    # 2. Linux Root Shell Interception (e.g., root@hostname:~#)
    if all([
        initial_prompt_lower.endswith("#"),
        "@" in initial_prompt_lower,
        ":~" in initial_prompt_lower,]
        ):
        # if "~#" in initial_prompt_lower or "bash" in initial_prompt_lower or ":~" in initial_prompt_lower:
        logging.info("[!] Linux/Bash root shell environment. Elevating to CLI...")
        cli_response = send_and_wait(device_shell, "cli")
        logging.info(f"[*] CLI Transition Output: {cli_response.strip()}")

    logging.info("[*] Probing device vendor...")
    probe_output = send_and_wait(device_shell, "show version")
    probe_lower = probe_output.lower()

    # Clear terminal execution buffer before doing check
    send_break(device_shell)

    # Return identified vendor
    vendor, terminal_cmd = get_signature_terminal_len(probe_lower)
    if vendor and terminal_cmd:
        return vendor, terminal_cmd

    # 2. STRATEGY FALLBACK: If show version is a bare number, probe for Viptela SD-WAN specific commands
    logging.warning("[*] signature inconclusive. Running next level verification...")
    probe_output = send_and_wait(device_shell, "show system status")
    probe_lower = probe_output.lower()
    send_break(device_shell)

    vendor, terminal_cmd = get_signature_terminal_len(probe_lower)
    if vendor and terminal_cmd:
        return vendor, terminal_cmd
        
    logging.error("[-] Signature indeterminate..")
    return None, None





def autodetect_via_prompt(net_connect):
    """
    Probes the live device prompt over the socket 
    to dynamically determine and redispatch the Netmiko class.
    """
    # Wake up the terminal buffer
    net_connect.write_channel("\r\n")
    time.sleep(1)
    
    # Read the current prompt
    current_prompt = net_connect.find_prompt()
    logging.info(f"[*] Analyzing device prompt signature: '{current_prompt}'")
    
    # Check signature characteristics
    if ">" in current_prompt and "%" not in current_prompt:
        # Check for Juniper-style markers or Arista/Cisco user modes
        if "@" in current_prompt:
            return "juniper_junos"
    
    # Fall back to checking common commands if prompt is ambiguous
    # Most enterprise gear responds to basic vendor flags
    test_output = net_connect.send_command_timing("show version")
    test_lower = test_output.lower()
    
    if "cisco" in test_lower:
        return "cisco_ios"
    elif "arista" in test_lower:
        return "arista_eos"
    elif "juniper" in test_lower or "junos" in test_lower:
        return "juniper_junos"
        
    logging.warning("[-] Indeterminate vendor. Defaulting engine to cisco_ios.")
    return "cisco_ios"



def manually_detect_device_type(tunnel_channel):
    """
    Reads the initial SSH banner from the tunnel socket 
    to determine the Netmiko device type before full initialization.
    """
    try:
        # Wait briefly for the remote device to send its SSH banner
        time.sleep(1.5)
        if tunnel_channel.recv_ready():
            # Read up to 1024 bytes of the banner data
            banner_bytes = tunnel_channel.recv(1024)
            banner_str = banner_bytes.decode('utf-8', errors='ignore').lower()
            logging.info(f"[*] Remote SSH Banner caught: {banner_str.strip()}")
            
            # Map banner signatures to Netmiko device types
            if "cisco" in banner_str:
                return "cisco_ios"
            elif "juniper" in banner_str or "junos" in banner_str:
                return "juniper_junos"
            elif "arista" in banner_str:
                return "arista_eos"
            elif "h3c" in banner_str or "huawei" in banner_str:
                return "huawei"
    except Exception as e:
        logging.warning(f"[!] Vendor banner detection warning: {e}")
    
    # Safe production fallback
    logging.error("[-] Could not parse vendor banner. Defaulting to cisco_ios.")
    return "cisco_ios"
