
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from netmiko import ConnectHandler
import traceback
from nettoolkit.nettoolkit_common.gpl import STR

from nettoolkit.detect import DeviceType
# -----------------------------------------------------------------------------

class Config_common():

	def get_device_type(self, ip, auth):
		"""detect device type (cisco, juniper)

		Args:
			ip (str): device ip

		Returns:
			str: device type if detected, else None
		"""    		
		try:
			dev = DeviceType(dev_ip=ip, 
				un=auth['un'], 
				pw=auth['pw'],
			)
			self.write_exec_log(ip, f"{ip} - Device Type Detection successful - {dev.dtype}")
			return dev.dtype
		except Exception as e:
			self.write_exec_log(ip, f"{ip} - Device Type Detection Failed with Exception \n{e}")
			return None

	def write_config_log(self, host, log):
		if self.config_log and self.log_folder:
			self.write_exec_log(host, f"writing configuration application log @ {self.log_folder}/{host}-config-apply.log", ends="\t")
			with open(f"{self.log_folder}/{host}-config-apply.log", 'a') as f:
				f.write(log)
			self.write_exec_log(host, f"...done")

	def write_exec_log(self, host, s, ends='\n'):
		if self.exec_display: print(s)
		if self.exec_log and self.log_folder:
			with open(f"{self.log_folder}/{host}-exec.log", 'a') as f:
				f.write(s+ends)


	def send_configuration(self, conf_list):
		self.write_exec_log(self.conn.host, f"applying config to {self.device_type} // {self.conn.host} // {self.ip}", ends="\t")
		try:
			self.op_return = self.conn.send_config_set(conf_list)
			self.write_exec_log(self.conn.host, f"...done")
			return True
		except:
			self.write_exec_log(self.conn.host, f"... Failed")
			return False

	def get_connection(self):
		conn = ConnectHandler(**self.dev_var)
		try:
			conn = ConnectHandler(**self.dev_var)
			self.connectionsuccess = True
			return conn
		except:
			self.write_exec_log(self.ip, f"Connection Failed to establish {self.device_type} // No connection // {self.ip}", ends="\n\n")
			self.connectionsuccess = False
			return None

	def terminate_connection(self):
		try:
			self.conn.disconnect()
		except:
			pass

	def set_hostname(self):
		try:
			self.dev_var['host'] = STR.hostname(self.conn).lower()
		except:
			self.write_exec_log(self.conn.host, f"Hostname Retrival failed for device {self.ip} ")
			self.dev_var['host'] = self.ip
		self.hn = self.dev_var['host']



# ----------------------------------------------------------------------------------------------------


class Configure(Config_common):

	def __init__(self, ip, auth, 
		conf_list=None, 
		conf_file=None, 
		log_folder=None,
		config_log=True,
		exec_log=True,
		exec_display=True,
		):
		self.ip = ip
		self.auth = auth
		self.conf_list = conf_list
		self.conf_file = conf_file       # prefered
		self.log_folder = log_folder
		self.config_log = config_log
		self.exec_log = exec_log
		self.exec_display = exec_display
		self._get_conf_list_from_file()

	def _get_conf_list_from_file(self):
		if self.conf_file:
			try:
				with open(self.conf_file, 'r') as f:
					conf_list = f.readlines()
			except:
				self.write_exec_log(self.conn.host, f"Error Reading file {self.conf_file}", ends="\n\n")
				return None
			if self.conf_list and conf_list:
				_d = input(f"BEWARE: DUAL INPUT DETECTED, conf_list as well as conf_file. configuration file will override list. Continue [Y/N]")
				if _d.upper() != 'Y': quit()
			if conf_list:
				self.conf_list = conf_list

	def apply(self):
		if not self.conf_list:
			self.write_exec_log(self.conn.host, f"No configurations to apply for {self.ip} // configuration=[{self.conf_list}]")
		if isinstance(self.conf_list, str):
			self.conf_list = [self.conf_list, ]
		self.device_type = self.get_device_type(self.ip, self.auth)
		self.dev_var = {'device_type': self.device_type, 
			'ip': self.ip,
			'username': self.auth['un'],
			'password': self.auth['pw'],
			'secret': self.auth['en'] if self.auth.get('en') else self.auth['pw'],
		}
		self._start_push()

	def _start_push(self):
		if self.device_type == 'juniper_junos':  self.juniper_push()
		elif self.device_type == 'cisco_ios':  self.cisco_push()
		else: print(f"Undetected device {self.ip}")

	## -------------- Juniper ------------------

	def juniper_push(self):
		if self.conf_list[-1] != 'commit check': 
			self.conf_list.append("commit check")
		#
		self.conn = self.get_connection()
		if not self.connectionsuccess: return False
		self.set_hostname()
		#
		send_conf = self.send_configuration(self.conf_list)
		if not send_conf:
			self.write_exec_log(self.conn.host, f"Termination without configuration apply for {self.device_type} // {self.conn.host} // {self.ip}", ends="\n\n")
			self.terminate_connection()
			return None
		self.write_config_log(self.conn.host, self.op_return)
		#
		check = self.juniper_verify_push_op(self.op_return)
		if not check: 
			self.write_exec_log(self.conn.host, f"ERROR: Termination without configuration apply for {self.device_type} // {self.conn.host} // {self.ip}", ends="\n\n")
			self.terminate_connection()
			return None
		#
		commit_return = self.juniper_commit()
		self.juniper_verify_commit_op(commit_return)
		#
		self.terminate_connection()


	def juniper_verify_push_op(self, op):
		check = False
		self.write_exec_log(self.conn.host, f"checking applied configuration for {self.device_type} // {self.conn.host} // {self.ip}", ends="\t" )
		for line in op.splitlines():
			if line.strip().startswith('syntax error'): break
			check = line == "configuration check succeeds"
			if check: break
		if check:
			self.write_exec_log(self.conn.host, f"...done")
		else:
			self.write_exec_log(self.conn.host, f"...Failed\n.  Re-Check configuration manually before commit\nGot:\n{self.op_return}")
		return check

	def juniper_verify_commit_op(self, op):
		self.write_exec_log(self.conn.host, f"verifying configuration commit to {self.device_type} // {self.conn.host} // {self.ip}", ends="\t")
		check = 0
		for line in op.splitlines():
			if (line.strip().startswith("configuration check succeeds") 
				or line.strip().startswith("commit complete")
				):
				check+=1 
		#
		if check == 2:
			self.write_exec_log(self.conn.host, f"...done")
		else:
			self.write_exec_log(self.conn.host, f"...Failed\nGot\n{op}")

	def juniper_commit(self):
		self.write_exec_log(self.conn.host, f"commiting configurations to {self.device_type} // {self.conn.host} // {self.ip}", ends="\t")
		try:
			commit_return = self.conn.commit()
			self.write_exec_log(self.conn.host, f"...done")
			return commit_return
		except:
			self.write_exec_log(self.conn.host, f"...failed\nGot\n{commit_return}")
			return False

	## -------------- Cisco ------------------

	def cisco_enable(self):
		if any( [
			self.device_type == 'cisco_ios'
			] ):
			for tries in range(3):
				try:
					self.net_connect.enable(cmd="enable")
					break
				except:
					self.write_exec_log(self.hn, f"{self.hn} - enable failed on attemp {tries}")
					continue

	def cisco_push(self):
		self.conn = self.get_connection()
		if not self.connectionsuccess: return False
		self.set_hostname()
		self.cisco_enable()
		#
		send_conf = self.send_configuration(self.conf_list)
		if not send_conf:
			self.write_exec_log(self.conn.host, f"Termination without configuration apply for {self.device_type} // {self.conn.host} // {self.ip}", ends="\n\n")
			self.terminate_connection()
			return None
		#
		self.write_config_log(self.conn.host, self.op_return)
		#
		check = self.cisco_verify_push_op(self.op_return)
		if not check: 
			self.write_exec_log(self.conn.host, f"ERROR: Termination without configuration apply for {self.device_type} // {self.conn.host} // {self.ip}", ends="\n\n")
			self.terminate_connection()
			return None
		#
		_return = self.cisco_commit()
		self.terminate_connection()


	def cisco_verify_push_op(self, op):
		error = False
		self.write_exec_log(self.conn.host, f"checking applied configuration for {self.device_type} // {self.conn.host} // {self.ip}", ends="\t" )
		for line in op.splitlines():
			error = line.strip().startswith("^")
			if error: break
		#
		if error:
			self.write_exec_log(self.conn.host, f"...Failed\n.  Re-Check configuration manually and reapply\nGot:\n{self.op_return}")
		else:
			self.write_exec_log(self.conn.host, f"...done")
		return error


	# save config
	def cisco_commit(self):
		self.write_exec_log(self.conn.host, f"saving configurations for {self.device_type} // {self.conn.host} // {self.ip}", ends="\t")
		try:
			_return = self.conn.save_config()
			self.write_exec_log(self.conn.host, f"...done")
			return _return
		except:
			self.write_exec_log(self.conn.host, f"...failed\nGot\n{_return}")
			return False

