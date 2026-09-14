
from dataclasses import dataclass
import time
import paramiko
from getpass import getpass


from nettoolkit._detect.vendor import send_and_wait, determine_vendor_profile, clear_buffer
from .common import get_device_ip_using_nlist, strip_ansi_and_clean, clean_hostname
from .commands import get_commands_for_type

# ===================================================================================

@dataclass
class JumpServer():
    server: str
    user: str
    password: str=''
    passphrase: str=''
    pkey: str=''

    def __post_init__(self):
        self.jump_client = None

    def connect(self):
        self.jump_client = paramiko.SSHClient()
        self.jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(self.pkey)
        self.jump_client.connect(hostname=self.server, username=self.user, pkey=k)

    def __str__(self):
        return self.jump_client

    def nlist(self, host):
        jump_shell = self.jump_client.invoke_shell()
        time.sleep(1)
        jump_shell.recv(5000)
        device_ip = get_device_ip_using_nlist(jump_shell, host)
        jump_shell.close() 
        return device_ip

    def disconnect(self):
        if self.jumpserver: 
            self.jumpserver.close()

# ===================================================================================
class Device():

    def __post_init__(self):
        self.device_shell = None
        self.paging_cmd = ''
        self.jumpserver = None

    def __str__(self): 
        return self.device_shell

    def connect_via_jump(self, ip: str, user: str, pw: str, jumpserver: JumpServer):
        self.jumpserver = jumpserver
        if pw.lower() in ('rsa', 'interactive'):
            pw = getpass(f"Enter password to login for {user}@{ip}: ")
        print(f"[*] Building TCP Tunnel to {ip}...")
        jump_transport = self.jumpserver.get_transport()
        dest_addr = (ip, 22)
        local_addr = (self.jumpserver.server, 22)
        tunnel_channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)
        print(f"[*] Authenticating session...")
        device_transport = paramiko.Transport(tunnel_channel)
        device_transport.start_client()
        device_transport.auth_password(username=user, password=pw)
        self.device_shell = device_transport.open_session()
        self.device_shell.get_pty(term='vt100', width=200, height=0)
        self.device_shell.invoke_shell()
        clear_buffer(self.device_shell)

    def identify_device_type(self):
        print("[*] Probing device vendor signature...")
        probe_output = send_and_wait(self.device_shell, "show version", wait_time=2.5)
        probe_lower = probe_output.lower()
        self.device_shell.send("\x03") 
        time.sleep(1)
        if self.device_shell.recv_ready():
            self.device_shell.recv(65535) # Clear the buffer post-break
        detected_type, self.paging_cmd = determine_vendor_profile(self.device_shell)
        print(f"[+] Identified Device Type: {detected_type}")
        self.device_type = detected_type
        return detected_type

    def identify_hostname(self):
        print(f"[*] Neutralizing paging with: '{self.paging_cmd}'")
        raw_prompt_data = send_and_wait(self.device_shell, self.paging_cmd, wait_time=1.0)
        cleaned_prompt_data = strip_ansi_and_clean(raw_prompt_data)
        lines = [line for line in cleaned_prompt_data.splitlines() if line.strip()]
        actual_hostname = clean_hostname(lines[-1]) if lines else "unknown_host"
        print(f"[+] Connected to host: {actual_hostname}. Executing log sequence...")
        self.hostname = actual_hostname
        return actual_hostname

    def capture(self, commands_list, to_file, mode='w'):
        starting_prompt = strip_ansi_and_clean(clear_buffer(self.device_shell))
        with open(to_file, mode, encoding="utf-8") as log_file:
            for cmd in commands_list:
                print(f"[*] Running: {cmd}")
                log_file.write(starting_prompt)
                self.device_shell.send(f"{cmd}\n")
                time.sleep(2.5)
                cmd_output = ""
                while self.device_shell.recv_ready():
                    cmd_output += self.device_shell.recv(65535).decode('utf-8', errors='ignore')
                log_file.write(strip_ansi_and_clean(cmd_output))
        print(f"[+] Captures successfully stored in output file: {to_file}")

    def disconnect(self):
        self.device_shell.send("exit\n")

# ===================================================================================

if __name__ == "__main__":
    pass
    jumpserver = JumpServer(server='rlpv123456', user='al2025', pkey='c:/abcd/abcd/abcd/privatekey', passphrase='mostsecurepw')
    jumpserver.connect()
    device_ip = jumpserver.nlist(host='ABCDEFG')
    device = Device()
    device.connect_via_jump(ip=device_ip, user='al2026', pw='securepw', jumpserver=jumpserver)
    device_type = device.identify_device_type()
    hostname = device.identify_hostname()
    commands_list = get_commands_for_type('commands_lists_yaml_file.yaml', device_type=device_type)
    device.capture(commands_list, to_file=f'{hostname}.log', mode='w')
    device.disconnect()
    jumpserver.disconnect()

    # JUMP_SERVER_IP = "rlpv13447.gcsc.att.com"
    # JUMP_SERVER_IP = "rlpv12149.gcsc.att.com"
    # JUMP_SERVER_IP = "rlpv10188.gcsc.att.com"
    # JUMP_SERVER_USER = "al202t"
    # PRIVATE_KEY_PATH = "C:/Users/al202t/OneDrive - AT&T Services, Inc/Documents/Identity2048"
    # DEVICE_USER = "al202t"
    # # DEVICE_USER = "root"
    # DEVICE_USER = "admin"
