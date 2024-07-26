# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from time import sleep
from nettoolkit.nettoolkit_common import STR, IP
from dataclasses import dataclass

from copy import deepcopy
import nettoolkit.facts_finder as ff
from nettoolkit.detect import DeviceType
from .conn import conn
from .captures import Captures
from .common import cmd_line_pfx

# -----------------------------------------------------------------------------
# Execution of Show Commands on a single device. 
# -----------------------------------------------------------------------------
@dataclass(init=True, repr=False, eq=False)
class Execute_Device():
	"""Execute a device capture

	Args:
		log_key (str): device ip
		auth (dict): authentication parameters
		cmds (list, set, tuple): set of commands to be executed.
		output_path (str): path where output to be stored
		cumulative (bool, optional): True,False,both. Defaults to False.
		forced_login (bool): True will try login even if device ping fails.
		parsed_output (bool): parse output and generate Excel or not.
		CustomClass(class): Custom class definition to provide additinal custom variable commands
		fg(bool): facts generation
		mandatory_cmds_retries(int): number of retries for missing mandatory commands captures
		append_capture(bool): append capture to existing file instead of creating new.
		missing_captures_only(bool): capture only missing command outputs from existing output
	"""    	
	log_key               : str
	auth                  : dict
	cmds                  : list
	output_path           : str
	cumulative            : bool 
	forced_login          : bool
	parsed_output         : bool
	CustomClass           : 'typing.Any'
	fg                    : bool
	mandatory_cmds_retries: int
	append_capture        : bool
	missing_captures_only : bool

	def __post_init__(self):
		ip = self.log_key
		self.all_cmds = {'cisco_ios': set(), 'juniper_junos':set(),}
		self.cumulative_filename = None
		self.delay_factor, self.dev = None, None
		self.cmd_exec_logs = []
		self.failed_reason = ''
		#
		ip = ip.strip()
		if not ip:
			self.failed_reason = f"Missing device ip: [{ip}]"
			print(f"{self.failed_reason} - skipping it")
			return None
		#
		self.pinging = self._check_ping(ip)
		self._start_execution(ip)

	def _check_ping(self, ip):
		"""check device reachability

		Args:
			ip (str): device ip

		Returns:
			int: delay factor if device reachable,  else False
		"""    		
		try:
			print(f"{ip} - Checking ping response")
			self.delay_factor = IP.ping_average (ip)/100 + 3
			print(f"{ip} - Delay Factor={self.delay_factor}")
			return self.delay_factor
		except:
			print(f"{ip} - Ping was unsuccessful")
			return False

	def _start_execution(self, ip):
		if not (self.forced_login or self.pinging): return
		if not self.pinging:
			print(f"{ip} - Trying for Forced login")
		dtype_result = self._get_device_type(ip)
		if not dtype_result: return
		if self.dev is None: return
		try:
			self._execute(ip)
		except:
			if self.dev.dtype != 'cisco_ios': return
			print(f"{ip} - sleeping progress for 65 seconds due to known cisco ios bug")					
			sleep(65)
			self._execute(ip)

	def _get_device_type(self, ip):
		"""detect device type (cisco, juniper)

		Args:
			ip (str): device ip

		Returns:
			str: device type if detected, else None
		"""    		
		try:
			self.dev = DeviceType(dev_ip=ip, 
				un=self.auth['un'], 
				pw=self.auth['pw'],
			)
			return self.dev
		except Exception as e:			
			self.failed_reason = f"[{ip}] - Device Type Detection Failed with Exception \n{e}"
			print(f"{'- '*40}\n{self.failed_reason}\n{'- '*40}")
			return None

	def _is_not_connected(self, c, ip):
		"""check if connection is successful

		Args:
			c (conn): connection object
			ip(str): ip address of connection

		Returns:
			conn: connection object if successful, otherwise None
		"""
		connected = True
		if STR.found(str(c), "FAILURE"): connected = None
		if c.hn == None or c.hn == 'dummy': connected = None
		return not connected

	def _execute(self, ip):
		"""login to given device(ip) using authentication parameters from uservar (u).
		if success start command captuers

		Args:
			ip (str): device ip
		"""
		print(f"{ip} - Initializing")

		with conn(	ip=ip, 
					un=self.auth['un'], 
					pw=self.auth['pw'], 
					en=self.auth['en'], 
					delay_factor=self.delay_factor,
					devtype=self.dev.dtype,
			) as c:
			# ------------------------------------------------------------------
			if self._is_not_connected(c, ip):
				self.failed_reason = self.failed_reason or "Connection Failure"
				return None
			# ------------------------------------------------------------------
			self.hostname = c.hn
			c.output_path = self.output_path
			c.dev_type = self.dev.dtype

			# -- get the missing commands list if it is to do only missing captures
			if self.missing_captures_only:
				if isinstance(self.cmds, dict):
					missed_cmds = self.get_missing_commands(c, set(self.cmds[self.dev.dtype]))
					self.cmds[self.dev.dtype] = missed_cmds
				elif isinstance(self.cmds, (list, set, tuple)):
					missed_cmds = self.get_missing_commands(c, set(self.cmds))
					self.cmds = missed_cmds
				if missed_cmds:
					print(f"{c.hn} : INFO: Missed Cmds = ", missed_cmds)
				else:
					print(f"{c.hn} : INFO: No missing Command found in existing capture..")

			cc = self.command_capture(c)
			cc.grp_cmd_capture(self.cmds)
			if self.cmds: self.add_cmd_to_all_cmd_dict(self.cmds)

			# -- for facts generation -- presence of mandary commands, and capture if not --
			if self.fg or self.mandatory_cmds_retries:
				missed_cmds = self.check_facts_finder_requirements(c)
				self.retry_missed_cmds(c, cc, missed_cmds)
				self.add_cmds_to_self(missed_cmds)
				if missed_cmds: self.add_cmd_to_all_cmd_dict(missed_cmds)

			# -- custom commands -- only log entries, no parser --
			if self.CustomClass:
				CC = self.CustomClass(c.output_path+"/"+c.hn+".log", self.dev.dtype)
				cc.grp_cmd_capture(CC.cmds)
				self.add_cmds_to_self(CC.cmds)
				if CC.cmds: self.add_cmd_to_all_cmd_dict(CC.cmds)


			# -- add command execution logs dataframe --
			cc.add_exec_logs()

			# -- write facts to excel --
			if not self.cumulative_filename: self.cumulative_filename = cc.cumulative_filename 
			if self.parsed_output: 
				self.xl_file = cc.write_facts()

			# -- add command execution logs
			self.cmd_exec_logs = cc.cmd_exec_logs

	def add_cmd_to_all_cmd_dict(self, cmds):
		"""add command to all cmd dictionary

		Args:
			cmds (str, list, tuple, set, dict): commands in any format
		"""    	
		if self.dev.dtype not in self.all_cmds.keys():
			self.all_cmds[self.dev.dtype] = set()
		if isinstance(cmds, (set, list, tuple)):
			self.all_cmds[self.dev.dtype] = self.all_cmds[self.dev.dtype].union(set(cmds))
		elif isinstance(cmds, dict):
			for dt, _cmds in cmds.items():
				if dt != self.dev.dtype: continue
				self.add_cmd_to_all_cmd_dict(_cmds)
		elif isinstance(cmds, str):
			self.all_cmds[self.dev.dtype].add(cmds)

	def add_cmds_to_self(self, cmds):
		"""add additional commands to cmds list

		Args:
			cmds (list): list of additinal or missed mandatory cmds to be captured 
		"""		
		if isinstance(self.cmds, list):
			for cmd in cmds:
				if cmd not in self.cmds:
					self.cmds.append(cmd)
		elif isinstance(self.cmds, set):
			for cmd in cmds:
				if cmd not in self.cmds:
					self.cmds.add(cmd)
		elif isinstance(self.cmds, tuple):
			for cmd in cmds:
				if cmd not in self.cmds:
					self.cmds = list(self.cmds).append(cmd)
		elif isinstance(self.cmds, dict):
			for cmd in cmds:
				if cmd not in self.cmds[self.dev.dtype]:
					self.cmds[self.dev.dtype].append(cmd)
		else:
			print(f"Non standard command input {type(self.cmds)}\n{self.cmds}")

	def command_capture(self, c):
		"""start command captures on connection object

		Args:
			c (conn): connection object
		"""
		print(f"{c.hn} : INFO : Starting Capture in `{'append' if self.append_capture else 'add'}` mode")

		cc = Captures(
			conn=c, 
			cumulative=self.cumulative,
			parsed_output=self.parsed_output,
			append_capture=self.append_capture,
			)
		return cc



	def missed_commands_capture(self, c, cc, missed_cmds, x=""): 
		"""recaptures missed commands

		Args:
			c (conn): connection object
			cc(Captures): Capture / Command line processing object
			missed_cmds (set): list/set of commands for which output to be recapture
			x (int, optional): iteration value
		"""		
		print(f"{c.hn} - Retrying missed_cmds({x+1}): {missed_cmds}")
		cc.grp_cmd_capture(missed_cmds)

	def is_any_ff_cmds_missed(self, c):
		"""checks and returns missed mandatory capture commands

		Args:
			c (conn): connection object

		Returns:
			set: missed mandatory commands
		"""		
		necessary_cmds = ff.get_necessary_cmds(self.dev.dtype)
		return self.get_missing_commands(c, necessary_cmds)

	def check_facts_finder_requirements(self, c):
		"""checks and returns missed mandatory capture commands
		clone to is_any_ff_cmds_missed

		Args:
			c (conn): connection object

		Returns:
			set: missed mandatory commands
		"""		
		return self.is_any_ff_cmds_missed(c)

	def retry_missed_cmds(self, c, cc, missed_cmds):
		"""retry missed commands captures

		Args:
			c (conn): connection object instance
			cc(Captures): Capture / Command line processing object
			missed_cmds (set): missed commands

		Returns:
			None: No retuns
		"""		
		for x in range(self.mandatory_cmds_retries):
			if not missed_cmds: return None
			self.missed_commands_capture(c, cc, missed_cmds, x)
			missed_cmds = self.is_any_ff_cmds_missed(c)
		if missed_cmds:	
			print(f"{c.hn} - Error capture all mandatory commands, try do manually..")

	def get_missing_commands(self, c, cmds):
		"""checks and returns missed capture commands

		Args:
			c (conn): connection object
			cmds (list): list of commands to check

		Returns:
			set: missed mandatory commands
		"""		
		try:
			file = c.output_path+"/"+c.hn+".log"
			with open(file, 'r') as f:
				log_lines = f.readlines()
		except:
			print(f'Cumulative capture file is required for Facts-Finder File not found {c.output_path+"/"+c.hn+".log"}')
			return []
		captured_cmds = set()
		for log_line in log_lines:
			if log_line[1:].startswith(cmd_line_pfx):
				captured_cmd = ff.get_absolute_command(self.dev.dtype, log_line.split(cmd_line_pfx)[-1])
				captured_cmds.add(captured_cmd.strip())
		missed_cmds = cmds.difference(captured_cmds)
		return list(missed_cmds)


