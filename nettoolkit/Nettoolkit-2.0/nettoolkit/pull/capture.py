
from dataclasses import dataclass
from datetime import datetime
import time
import paramiko
from getpass import getpass
import logging


from .vendor import determine_vendor_profile
from .common import get_device_ip_using_nlist, strip_ansi_and_clean, clean_hostname, wait_for_prompt, wait_for_output, drain_buffer
from .commands import get_commands_for_type

# ===================================================================================

@dataclass
class JumpServer():
    server: str
    user: str
    auth_type: str='auto'
    password: str=''
    passphrase: str=''
    pkey: str=''

    def __post_init__(self):
        self.jump_client = None
        self.jump_client = paramiko.SSHClient()
        self.jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_via_pkey(self):
        k = paramiko.RSAKey.from_private_key_file(self.pkey,
                                                  password=self.passphrase or None)
        self.jump_client.connect(hostname=self.server, username=self.user, pkey=k)

    def connect_via_password(self):
        if not self.password:
            while True:
                self.password = getpass(f"Provide RSA/Password for user: {self.user} to authenticate to Jump Server: ")
                if self.password:
                    break
        self.jump_client.connect(hostname=self.server, username=self.user, password=self.password)

    def connect(self):
        if self.auth_type in ('key', ):
            self.connect_via_pkey()
        elif self.auth_type in ('password', 'rsa'):
            self.connect_via_password()
        else:
            try:
                self.connect_via_pkey()
            except Exception as e:
                logging.warning(f"Key auth failed: {e}")
                self.connect_via_password()

    def nlist(self, host):
        jump_shell = self.jump_client.invoke_shell()
        time.sleep(1)
        if jump_shell.recv_ready():
            jump_shell.recv(5000)
        device_ip = get_device_ip_using_nlist(jump_shell, host)
        jump_shell.close() 
        return device_ip

    def disconnect(self):
        if self.jump_client: 
            self.jump_client.close()

# ===================================================================================

class Device():

    def __init__(self):
        self.device_shell = None
        self.paging_cmd = ''
        self.jumpserver = None
        self.device_transport = None
        self.device_client = None
        self.charasteristics = {}

    def connect(self, ip, user, pw, jumpserver=None):
        self.initial_time = time.time()
        logging.info(f"[*] Authenticating session...")
        if jumpserver:
            self.connect_via_jump(ip, user, pw, jumpserver)
        else:
            self.connect_direct(ip, user, pw)
        logging.info(f"[+] Authentication completed in {time.time()-self.initial_time:.1f}s")

    def connect_direct(self, ip:str, user:str, pw: str):
        if not pw:
            while True:
                pw = getpass(f"Enter password to login to device for {user}@{ip}: ")
                if pw: break
        logging.info(f"[*] Connecting to {ip}...")
        self.device_client = paramiko.SSHClient()
        self.device_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.device_client.connect(hostname=ip, username=user, password=pw)
        self.device_shell = self.device_client.invoke_shell()
        self.wait_for_prompt()

    def connect_via_jump(self, ip: str, user: str, pw: str, jumpserver: JumpServer):
        self.jumpserver = jumpserver
        if not pw:
            while True:
                pw = getpass(f"Enter password to login to device for {user}@{ip}: ")
                if pw: break
        logging.info(f"[*] Building TCP Tunnel to {ip}...")
        jump_transport = self.jumpserver.jump_client.get_transport()
        dest_addr = (ip, 22)
        local_addr = (self.jumpserver.server, 22)
        tunnel_channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)
        self.device_transport = paramiko.Transport(tunnel_channel)
        self.device_transport.start_client()        
        self.device_transport.auth_password(username=user, password=pw)
        self.device_shell = self.device_transport.open_session()
        self.device_shell.get_pty(term='vt100', width=200, height=0)
        self.device_shell.invoke_shell()
        self.wait_for_prompt()
        # drain_buffer(self.device_shell)

    def wait_for_prompt(self):
        self.initial_prompt = wait_for_prompt(self.device_shell,     
                                         timers_dict=self.charasteristics.get('timers', {}))

    def identify_device_type(self):
        logging.info("[*] Probing device vendor signature...")
        detected_type, self.paging_cmd = determine_vendor_profile(self.device_shell, self.charasteristics)
        logging.info(f"[+] Identified Device Type: {detected_type}")
        self.device_type = detected_type
        return detected_type

    def identify_hostname(self):
        logging.info(f"[*] Neutralizing paging with: '{self.paging_cmd}'")
        raw_prompt_data = wait_for_output(self.device_shell, self.paging_cmd, self.charasteristics.get('timers'))
        cleaned_prompt_data = strip_ansi_and_clean(raw_prompt_data)
        lines = [line for line in cleaned_prompt_data.splitlines() if line.strip()]
        actual_hostname = clean_hostname(lines[-1]) if lines else "unknown_host"
        logging.info(f"[+] Connected to host: {actual_hostname}. Executing log sequence...")
        self.hostname = actual_hostname
        return actual_hostname

    def capture(self, commands_list, to_file, mode='w'):
        starting_prompt = strip_ansi_and_clean(drain_buffer(self.device_shell))
        capture_time = datetime.now()
        with open(to_file, mode, encoding="utf-8") as log_file:
            log_file.write(f"{'#'*80}\n"
                           f"# HOSTNAME: {self.hostname}\n"
                           f"# VENDOR: {self.device_type}\n"
                           f"# CAPTURED AT: {capture_time}\n"
                           f"{'#'*80}\n")
            for cmd in commands_list:
                logging.info(f"[*] Running: {cmd}")
                cmd_output = wait_for_output(self.device_shell, cmd, self.charasteristics.get('timers'))
                log_file.write(starting_prompt + strip_ansi_and_clean(cmd_output))
        logging.info(f"[+] Captures successfully stored in output file: {to_file}")

    def disconnect(self):
        self.device_shell.send("exit\n")
        self.device_shell.close()
        if self.device_transport:
            self.device_transport.close()
        if self.device_client:
            self.device_client.close()

def get_charasteristics(yaml_ref_file):
    from pathlib import Path
    from nettoolkit.cmn.fio import read_yaml

    yaml_ref_file_path = Path(__file__).with_name(yaml_ref_file)
    return read_yaml(yaml_ref_file_path)

def start_logging(charasteristics):
    logging_file = charasteristics.get('log_file', None)
    log_level = charasteristics.get('log_level', 'INFO')
    handlers = [ logging.StreamHandler(),]

    if logging_file:
        handlers.append( logging.FileHandler(logging_file) )

    logging.basicConfig(
        level=getattr(logging,
                      log_level.upper(),
                      logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
    )


# ===================================================================================

if __name__ == "__main__":
    pass

    charasteristics_file = 'characteristics.yaml'
    commands_list_file   = 'commands_lists_yaml_file.yaml'

    charasteristics = get_charasteristics(charasteristics_file)
    start_logging(charasteristics.get('logging', {}))

    jumpserver = JumpServer(server='rlpv123456', user='al2025', pkey='c:/abcd/abcd/abcd/privatekey', passphrase='mostsecurepw')
    jumpserver.connect()
    device_ip = jumpserver.nlist(host='ABCDEFG')
    # -----------------
    device = Device()
    device.charasteristics = charasteristics
    device.connect(ip=device_ip, user='al2026', pw='securepw', jumpserver=jumpserver)
    device_type = device.identify_device_type()
    hostname = device.identify_hostname()
    commands_list = get_commands_for_type(commands_list_file, device_type=device_type)
    device.capture(commands_list, to_file=f'{hostname}.log', mode='w')
    device.disconnect()
    # ----------------- 
    jumpserver.disconnect()

    # JUMP_SERVER_IP = "rlpv13447.gcsc.att.com"
    # JUMP_SERVER_IP = "rlpv12149.gcsc.att.com"
    # JUMP_SERVER_IP = "rlpv10188.gcsc.att.com"
    # JUMP_SERVER_USER = "al202t"
    # PRIVATE_KEY_PATH = "C:/Users/al202t/OneDrive - AT&T Services, Inc/Documents/Identity2048"
    # DEVICE_USER = "al202t"
    # # DEVICE_USER = "root"
    # DEVICE_USER = "admin"
