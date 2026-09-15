
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
import time
import paramiko
from getpass import getpass
import logging

from nettoolkit.cmn.flist import split_to_group
from nettoolkit.cmn.mt import Multi_Execution

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

    def __str__(self):
        return f"JumpServer({self.server})"

    def __post_init__(self):
        self.jump_client = None
        self.jump_client = paramiko.SSHClient()
        self.jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_via_pkey(self):
        logging.info(f"[{self}] Connecting via pkey")
        k = paramiko.RSAKey.from_private_key_file(self.pkey,
                                                  password=self.passphrase or None)
        self.jump_client.connect(hostname=self.server, username=self.user, pkey=k)

    def connect_via_password(self):
        logging.info(f"[{self}] Connecting via static password")
        if not self.password:
            while True:
                self.password = getpass(f"Provide RSA/Password for user: {self.user} to authenticate to Jump Server: ")
                if self.password:
                    break
        self.jump_client.connect(hostname=self.server, username=self.user, password=self.password)

    def connect(self):
        logging.info(f"[{self}] Connect to Jump Server")
        if self.auth_type in ('key', ):
            self.connect_via_pkey()
        elif self.auth_type in ('password', 'rsa'):
            self.connect_via_password()
        else:
            try:
                self.connect_via_pkey()
            except Exception as e:
                logging.warning(f"[{self}]Key auth failed: {e}")
                self.connect_via_password()

    def nlist(self, host):
        logging.info(f"[{self}] Resolving Hostname to IP")
        jump_shell = self.jump_client.invoke_shell()
        time.sleep(1)
        if jump_shell.recv_ready():
            jump_shell.recv(5000)
        device_ip = get_device_ip_using_nlist(jump_shell, host, self)
        jump_shell.close() 
        return device_ip

    def disconnect(self):
        if self.jump_client: 
            logging.info(f"[{self}] Disconnecting from Poller ")
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
        self.hostname = None
        self.ip = None

    def __str__(self):
        return f"Device({self.hostname or self.ip or 'Undetected'})"

    def connect(self, ip, user, pw, jumpserver=None):
        logging.info(f"[{self}] Connecting Device")
        self.ip = ip
        self.initial_time = time.time()
        if jumpserver:
            self.connect_via_jump(ip, user, pw, jumpserver)
        else:
            self.connect_direct(ip, user, pw)
        logging.info(f"[{self}] Authentication completed in {time.time()-self.initial_time:.1f}s")

    def connect_direct(self, ip:str, user:str, pw: str):
        logging.info(f"[{self}] Authenticating session (direct login)...")
        if not pw:
            while True:
                pw = getpass(f"Enter password to login to device for {user}@{ip}: ")
                if pw: break
        logging.info(f"[{self}] Connecting to {ip}...")
        self.device_client = paramiko.SSHClient()
        self.device_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.device_client.connect(hostname=ip, username=user, password=pw)
        self.device_shell = self.device_client.invoke_shell()
        self.wait_for_prompt()

    def connect_via_jump(self, ip: str, user: str, pw: str, jumpserver: JumpServer):
        logging.info(f"[{self}] Authenticating session (via Jump Host)...")
        self.jumpserver = jumpserver
        if not pw:
            while True:
                pw = getpass(f"Enter password to login to device for {user}@{ip}: ")
                if pw: break
        logging.info(f"[{self}] Building TCP Tunnel to {ip}...")
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
        logging.info(f"[{self}] Probing device vendor signature...")
        detected_type, self.paging_cmd = determine_vendor_profile(self.device_shell, self.charasteristics, self)
        self.device_type = detected_type
        logging.info(f"[{self}] Identified Device Type: {detected_type}")
        return detected_type

    def identify_hostname(self):
        logging.info(f"[{self}] Neutralizing paging with: '{self.paging_cmd}'")
        raw_prompt_data = wait_for_output(self.device_shell, self.paging_cmd, self.charasteristics.get('timers'))
        cleaned_prompt_data = strip_ansi_and_clean(raw_prompt_data)
        lines = [line for line in cleaned_prompt_data.splitlines() if line.strip()]
        actual_hostname = clean_hostname(lines[-1]) if lines else "unknown_host"
        self.hostname = actual_hostname
        logging.info(f"[{self}] Connected to host: {actual_hostname}. Executing log sequence...")
        return actual_hostname

    def capture(self, commands_list, to_file, mode='w'):
        logging.info(f"[{self}] Command Output Captures...")
        starting_prompt = strip_ansi_and_clean(drain_buffer(self.device_shell))
        capture_time = datetime.now()
        with open(to_file, mode, encoding="utf-8") as log_file:
            log_file.write(f"{'#'*80}\n"
                           f"# HOSTNAME: {self.hostname}\n"
                           f"# VENDOR: {self.device_type}\n"
                           f"# CAPTURED AT: {capture_time}\n"
                           f"{'#'*80}\n")
            for cmd in commands_list:
                logging.info(f"[{self}] Running: {cmd}")
                cmd_output = wait_for_output(self.device_shell, cmd, self.charasteristics.get('timers'))
                log_file.write(starting_prompt + strip_ansi_and_clean(cmd_output))
        logging.info(f"[{self}] Captures successfully stored in output file: {to_file}")

    def disconnect(self):
        logging.info(f"[{self}] Disconnecting Device...")
        self.device_shell.send("exit\n")
        self.device_shell.close()
        if self.device_transport:
            self.device_transport.close()
        if self.device_client:
            self.device_client.close()
# ===================================================================================

def get_charasteristics(yaml_ref_file):
    from pathlib import Path
    from nettoolkit.cmn.fio import read_yaml

    yaml_ref_file_path = Path(__file__).with_name(yaml_ref_file)
    return read_yaml(yaml_ref_file_path)

def start_logging(charasteristics):
    logging_file = charasteristics.get('log_file', None)
    log_level = charasteristics.get('log_level', 'INFO')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    handlers = [ 
        console_handler,
    ]

    if logging_file:
        handlers.append( logging.FileHandler(logging_file) )

    logging.basicConfig(
        level=getattr(logging,
                      log_level.upper(),
                      logging.INFO),
        format="%(asctime)s %(threadName)s %(levelname)s %(message)s",
        handlers=handlers,
    )

# ===================================================================================
@dataclass
class CaptureManager(Multi_Execution):
    user: str
    password: str=''
    pkey: str=''
    passphrase: str=''
    targets: list = field(default_factory=list)
    jumpserver_host: str=''
    jumpserver_auth_type: str='auto'
    output_path: str="."
    commands_list_file: str = ''
    charasteristics_file: str = ''

    def __str__(self):
        return f"CaptureManager"

    def __post_init__(self):
        self.exec_result = {}
        self.charasteristics = get_charasteristics(self.charasteristics_file)
        start_logging(self.charasteristics.get('logging', {}))
        super().__init__(self.targets)
        self.sleep_by = 45

    def capture_targets(self):
        logging.info(f"[{self.user}] - Initiated")
        try:
            if self.jumpserver_host:
                self.connect_jump_server()
            self.get_ip_addresses()
            self.start()
        finally:
            if self.jumpserver_host:
                self.disconnect_jump_server()

    def connect_jump_server(self):
        self.jumpserver = JumpServer(server=self.jumpserver_host, 
                                     user=self.user, 
                                     pkey=self.pkey, 
                                     passphrase=self.passphrase,
                                     auth_type=self.jumpserver_auth_type)
        self.jumpserver.connect()

    def disconnect_jump_server(self):
        self.jumpserver.disconnect()

    def get_ip_addresses(self):
        logging.info(f"[{self}] Prepare for MT...")
        self.items = {}
        if self.jumpserver_host:
            for target in self.targets:
                device_ip = self.jumpserver.nlist(host=target)
                self.items[device_ip] = target
        else:
            self.items = {x:x for x in self.targets}

    def execute(self, device_ip):
        try:
            self.capture_device(device_ip)
        except Exception:
            logging.exception(f"[{self}] worker failed: {device_ip}")


    def capture_device(self, device_ip):
        logging.info(f"[{self}] Initiating -> {device_ip}...")
        device = Device()
        device.charasteristics = self.charasteristics
        try:
            device.connect(ip=device_ip, user=self.user, pw=self.password, jumpserver=self.jumpserver)
            device_type = device.identify_device_type()
            hostname = device.identify_hostname()
            commands_list = get_commands_for_type(self.commands_list_file, device_type=device_type)
            device.capture(commands_list, to_file=f'{self.output_path}/{hostname}.log', mode='w')
            self.exec_result[self.items[device_ip]] = 'success'
        except Exception as e:
            logging.error(f"[{self}] Capture failed for {self.items[device_ip]} with error {e}")
            self.exec_result[self.items[device_ip]] = 'failed'
        finally:
            try:
                device.disconnect()
            except:
                pass

    def print_summary(self):
        logging.info(f"[{self}] Summary: {str(self.exec_result)}")
        print(f"DEVICE\t\tRESULT")
        for target, result in self.exec_result.items():
            print(f"{target}\t{result}")

# ===================================================================================

if __name__ == "__main__":
    pass

    # ## EXAMPLE USAGE ##
    cm = CaptureManager(
        user='al202t',
        pkey='C:\\Users\\al202t\\OneDrive - AT&T Services, Inc\\Documents\\Identity2048',
        passphrase='',
        jumpserver_host='rlpv13464',
        targets=["ID-SUB-00123-SDW-01", "IN-BOM-00506-SDW-02", "US-ELP-10079-SDW-02"],
        output_path=".",
        commands_list_file='commands_lists_yaml_file.yaml',
        charasteristics_file='characteristics.yaml',
    )
    cm.capture_targets()
    cm.print_summary()

# ===================================================================================
