
# -----------------------------------------------------------------------------
import os, csv

from nettoolkit.nettoolkit_common import Multi_Execution, IP, nslookup
from nettoolkit.addressing.addressing import addressing

ping = IP.ping_average

# -----------------------------------------------------------------------------
class Ping(Multi_Execution):
	"""Multi Ping class

	Args:
		pfxs (list): list of prefixes
		till (int, optional): how many ips to select. Defaults to 5.
		concurrent_connections (int, optional): number of simultaneous pings. Defaults to 500.
		create_tabs (bool, optional): want to create individual tab (True) for each subnet or clubbed (False)
	"""	

	def __init__(self, pfxs, till=None, concurrent_connections=500, create_tabs=False):
		"""instance initializer
		"""		
		self.pfxs = pfxs
		self.till = till
		self.max_connections = concurrent_connections
		self.create_tabs = create_tabs
		self.items = self.get_first_ips()
		self.ping_results = {}
		self.ping_ms = {}
		self.dns_result = {}
		self.result = {'ping_ms': self.ping_ms, 'dns_result': self.dns_result, 'ping_results': self.ping_results} 
		self.results_dict = {}
		self.counter = 1
		self.start()

	def get_first_ips(self):
		"""selects ips for each subnets from given prefixes

		Args:

		Returns:
			list: crafted list with first (n)/ all ip addresses from each subnet
		"""	
		new_iplist=[]
		self.pfx_dict={}
		for pfx in self.pfxs:
			subnet = addressing(pfx)
			try:
				if self.till==0:
					hosts = subnet[0]
				elif self.till:
					hosts = subnet[0:int(self.till)+1]
				else:
					hosts =subnet[0:len(subnet)]
			except:
				hosts =subnet[0:len(subnet)]
			self.pfx_dict[pfx] = [host for host in hosts]
			new_iplist.extend(self.pfx_dict[pfx])
		return new_iplist

	def execute(self, ip):
		"""executor

		Args:
			ip (str): ip address
		"""		
		# print(f"pinging -{ip}")
		self.ping_ms[ip] = ping(ip)
		self.ping_results[ip] = True if self.ping_ms[ip]  else False
		self.dns_result[ip] = nslookup(ip)
		self.add_results(ip, self.ping_results[ip], self.ping_ms[ip], self.dns_result[ip])

	def add_results(self, ip, ping_R, ping_ms_R, dns_R):
		"""add ping/dns results to results dictionary

		Args:
			ip (str): ip address
			ping_R (bool): ping result True/False
			ping_ms_R (int): milisecond if True
			dns_R (str): dns result
		"""		
		for pfx, hosts in self.pfx_dict.items():
			if not ip in hosts: continue
			if not self.results_dict.get(pfx):
				self.results_dict[pfx] = {}
			self.results_dict[pfx][ip] = { 'ping_ms': ping_ms_R, 'dns_result': dns_R, 'ping_results': ping_R}
			break

	def op_to_xl(self, opfile):
		"""write out result of pings to an output file

		Args:
			opfile (str): output excel file 
		"""		
		print("DEPRYCATED.., TBD (convert to op_to_csv_files)")

	def op_to_csv_files(self, op_dir):
		"""
		creates a folder and update with individual 
		CSV files for every network prefix available in results_dict.
		"""
		# Ensure the destination directory exists
		os.makedirs(op_dir, exist_ok=True)
		headers = ['ip', 'ping_ms', 'dns_result', 'ping_results']

		# loop over the available prefixes
		for pfx, ipresults in self.results_dict.items():
			# Clean prefix text to create a valid file name (e.g., '10.0.0.0_24.csv')
			filename = f"{pfx.replace('/', '_')}.csv"
			filepath = os.path.join(op_dir, filename)
			
			with open(filepath, mode='w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				writer.writerow(headers)  # header row
				
				for ip, stats in ipresults.items():   # data rows
					writer.writerow([
						ip, 
						stats.get('ping_ms'), 
						stats.get('dns_result'), 
						stats.get('ping_results')
					])


def compare_ping_sweeps(first, second):
	"""comparision of two ping result excel files 

	Args:
		first (str): ping result excel file-1
		second (str): ping result excel file-2

	Returns:
		None: Returns None, prints out result on console/screen
	"""	
	print("DEPRYCATED -- TBD (to be replace by .common.compare_two_ping_files() )")
	#


# -----------------------------------------------------------------------------
# Execute
# -----------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------
