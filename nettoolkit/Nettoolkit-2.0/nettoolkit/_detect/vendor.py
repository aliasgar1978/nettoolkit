
import time


def send_and_wait(channel, command, wait_time=2.0, buffer_size=65535):
    """Sends a command to the channel and waits to collect all available output."""
    channel.send(f"{command}\n")
    time.sleep(wait_time)
    
    output = ""
    while channel.recv_ready():
        output += channel.recv(buffer_size).decode('utf-8', errors='ignore')
    return output

def clear_buffer(device_shell):
    device_shell.send("\x03")
    time.sleep(0.5)
    if device_shell.recv_ready():
        device_shell.recv(65535)


def get_vendor_terminal_len_cmd(output_lowered):
    if "viptela" in output_lowered or "vedge" in output_lowered or "vedgeos" in output_lowered:
        return "cisco_viptela", "paginate false"
    elif "silver peak" in output_lowered or "edgeconnect" in output_lowered or " vx-" in output_lowered or "ec-" in output_lowered:
        return "aruba_silverpeak", "terminal length 0"
    elif "ios-xe" in output_lowered or "ios xe" in output_lowered:
        return "cisco_xe", "terminal length 0"
    elif "juniper" in output_lowered or "junos" in output_lowered :
        return "juniper_junos", "set cli screen-length 0"
    elif "arista" in output_lowered:
        return "arista_eos", "terminal length 0"
    return None,None

def determine_vendor_profile(device_shell):

    # 1. Wake up channel and read the initial prompt environment
    device_shell.send("\n")
    time.sleep(1.0)
    initial_prompt = ""
    while device_shell.recv_ready():
        initial_prompt += device_shell.recv(4096).decode('utf-8', errors='ignore')
    
    initial_prompt_lower = initial_prompt.lower()
    print(f"[*] Initial system environment: {initial_prompt.strip()}")

    # 2. Linux Root Shell Interception (e.g., root@hostname:~#)
    if "~#" in initial_prompt_lower or "bash" in initial_prompt_lower or ":~" in initial_prompt_lower:
        print("[!] Linux/Bash root shell environment. Elevating to CLI...")
        cli_response = send_and_wait(device_shell, "cli", wait_time=2.0)
        print(f"[*] CLI Transition Output: {cli_response.strip()}")

    print("[*] Probing device vendor...")
    probe_output = send_and_wait(device_shell, "show version", wait_time=2.0)
    probe_lower = probe_output.lower()

    # Clear terminal execution buffer before doing check
    clear_buffer(device_shell)

    # Return identified vendor
    vendor, terminal_cmd = get_vendor_terminal_len_cmd(probe_lower)
    if vendor and terminal_cmd:
        return vendor, terminal_cmd

    # 2. STRATEGY FALLBACK: If show version is a bare number, probe for Viptela SD-WAN specific commands
    print("[*] signature inconclusive. Running next level verification...")
    viptela_probe = send_and_wait(device_shell, "show control connections", wait_time=2.0)
    viptela_lower = viptela_probe.lower()

    # Clear buffer again
    clear_buffer(device_shell)

    if "peer" in viptela_lower or "local color" in viptela_lower or "site-id" in viptela_lower or "vsmart" in viptela_lower:
        return "cisco_viptela", "paginate false"
        
    if "cisco" in probe_lower:
        return "cisco_ios", "terminal length 0"
        
    print("[-] Signature indeterminate..")
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
    print(f"[*] Analyzing device prompt signature: '{current_prompt}'")
    
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
        
    print("[-] Indeterminate vendor. Defaulting engine to cisco_ios.")
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
            print(f"[*] Remote SSH Banner caught: {banner_str.strip()}")
            
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
        print(f"[!] Vendor banner detection warning: {e}")
    
    # Safe production fallback
    print("[-] Could not parse vendor banner. Defaulting to cisco_ios.")
    return "cisco_ios"
