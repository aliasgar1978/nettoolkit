
import time
import paramiko


from nettoolkit._detect.vendor import send_and_wait, determine_vendor_profile
from .common import get_device_ip_using_nlist, strip_ansi_and_clean, clean_hostname
from .commands import get_commands_for_type

JUMP_SERVER_IP = "rlpv13447.gcsc.att.com"
JUMP_SERVER_IP = "rlpv12149.gcsc.att.com"
JUMP_SERVER_IP = "rlpv10188.gcsc.att.com"
JUMP_SERVER_USER = "al202t"
PRIVATE_KEY_PATH = "C:/Users/al202t/OneDrive - AT&T Services, Inc/Documents/Identity2048"
DEVICE_USER = "al202t"
# DEVICE_USER = "root"
DEVICE_USER = "admin"



def capture_device_data(target_input):
    rsa_token = input(f"Enter RSA Soft Token pin/passcode for {target_input}: ")

    # 1. Connect to Jump Server
    print(f"[*] Connecting to Jump Server ({JUMP_SERVER_IP})...")
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    k = paramiko.RSAKey.from_private_key_file(PRIVATE_KEY_PATH)
    jump_client.connect(hostname=JUMP_SERVER_IP, username=JUMP_SERVER_USER, pkey=k)
    
    # Resolve the Target IP from the jump server shell
    jump_shell = jump_client.invoke_shell()
    time.sleep(1)
    jump_shell.recv(5000) 
    device_ip = get_device_ip_using_nlist(jump_shell, target_input)
    jump_shell.close() 

    # 2. Open Direct TCP Tunnel through Jump Server
    print(f"[*] Building TCP Tunnel to {device_ip}...")
    jump_transport = jump_client.get_transport()
    dest_addr = (device_ip, 22)
    local_addr = (JUMP_SERVER_IP, 22)
    tunnel_channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)

    # 3. Authenticate to the Target Device over the Tunnel
    print(f"[*] Authenticating target device session...")
    device_transport = paramiko.Transport(tunnel_channel)
    device_transport.start_client()
    device_transport.auth_password(username=DEVICE_USER, password=rsa_token)
    
    # 4. Open an Interactive Shell with a massive window height to neutralize paging
    device_shell = device_transport.open_session()
    # Setting height=0 tells many modern operating systems not to page text output
    device_shell.get_pty(term='vt100', width=200, height=0)
    device_shell.invoke_shell()
    
    # Clear welcome banners from the buffer
    time.sleep(2)
    initial_buffer = ""
    if device_shell.recv_ready():
        initial_buffer = device_shell.recv(65535).decode('utf-8', errors='ignore')

    # 5. Send 'show version' to probe for the manufacturer profile
    print("[*] Probing device vendor signature...")
    probe_output = send_and_wait(device_shell, "show version", wait_time=2.5)
    probe_lower = probe_output.lower()

    # 6. Send Ctrl+C immediately to kill any accidental output paging loops
    print("[*] Sending CTRL+C to clear execution buffers...")
    device_shell.send("\x03") 
    time.sleep(1)
    if device_shell.recv_ready():
        device_shell.recv(65535) # Clear the buffer post-break

    # 7. Identify vendor and assign respective pagination-disable command
    detected_type, paging_cmd = determine_vendor_profile(device_shell)
    print(f"[+] Identified Device Type: {detected_type}")

    # 8. Send the specific disable paging command string
    print(f"[*] Neutralizing paging with: '{paging_cmd}'")
    raw_prompt_data = send_and_wait(device_shell, paging_cmd, wait_time=1.0)
    
    # Determine actual structural hostname from the remaining prompt
    cleaned_prompt_data = strip_ansi_and_clean(raw_prompt_data)
    lines = [line for line in cleaned_prompt_data.splitlines() if line.strip()]
    actual_hostname = clean_hostname(lines[-1]) if lines else "unknown_host"
    print(f"[+] Connected to host: {actual_hostname}. Executing log sequence...")

    # 9. Fetch and loop through commands array
    commands_to_run = get_commands_for_type(detected_type)
    log_filename = f"{actual_hostname}.log"

    # 2. Final purge of the channel buffer right before starting data collection.
    # This ensures the very first character in the log is your initial clean prompt.
    device_shell.send("\n")
    time.sleep(1.0)
    if device_shell.recv_ready():
        raw_start = device_shell.recv(65535).decode('utf-8', errors='ignore')
        starting_prompt = strip_ansi_and_clean(raw_start)

    with open(log_filename, "w", encoding="utf-8") as log_file:
        # log_file.write(f"=== Capture Log for Device: {actual_hostname} ({device_ip}) ===\n")
        # log_file.write(f"=== Vendor Profile: {detected_type} ===\n\n")
        
        for cmd in commands_to_run:
            print(f"[*] Running: {cmd}")
            log_file.write(starting_prompt)

            # log_file.write(f"\n--- Command: {cmd} ---\n")
            # # Execute command and store response directly
            # cmd_output = send_and_wait(device_shell, cmd, wait_time=2.5)
            # log_file.write(cmd_output)
            # log_file.write("\n")

            # 1. Send the command string
            device_shell.send(f"{cmd}\n")
            
            # 2. Wait for it to process locally on the switch CPU
            time.sleep(2.5)
            
            # 3. Stream all output bytes (includes command echo, text payload, and next prompt)
            cmd_output = ""
            while device_shell.recv_ready():
                cmd_output += device_shell.recv(65535).decode('utf-8', errors='ignore')
            
            # 4. Save the continuous raw terminal interaction to the text file
            log_file.write(strip_ansi_and_clean(cmd_output))
         
            
    print(f"[+] Captures successfully stored in output file: {log_filename}")
    jump_client.close()


