
# -----------------------------------------------------------------------------
import pandas as pd
import PySimpleGUI as sg
import nettoolkit as nt
from nettoolkit.addressing import addressing
from nettoolkit.gpl import Multi_Execution
from nettoolkit.forms.formitems import *
from nettoolkit.gpl import IP
from nettoolkit.gpl import nslookup
ping = IP.ping_average

# -----------------------------------------------------------------------------
def get_first_ips(pfxs, till=5):
	"""selects first (n) ips for each subnets from given prefixes

	Args:
		pfxs (list): list of prefixes
		till (int, optional): how many ips to select. Defaults to 5.

	Returns:
		list: crafted list with first (n) ip addresses from each subnet
	"""	
	new_iplist=[]
	for pfx in pfxs:
		subnet = addressing(pfx)
		try:
			hosts = subnet[1:till+1]
		except:
			hosts =subnet[1:len(subnet)]
		new_iplist.extend([host for host in hosts])
	return new_iplist

# -----------------------------------------------------------------------------
class Ping(Multi_Execution):
	"""Multi Ping class

	Args:
		hosts (str): list of ips to be pinged
		concurrent_connections (int, optional): number of simultaneous pings. Defaults to 1000.
	"""	

	def __init__(self, hosts, concurrent_connections=1000):
		"""instance initializer
		"""		
		self.items = hosts
		self.max_connections = concurrent_connections
		self.ping_results = {}
		self.ping_ms = {}
		self.dns_result = {}
		self.result = {'ping_ms': self.ping_ms, 'dns_result': self.dns_result, 'ping_results': self.ping_results} 
		self.start()

	def execute(self, ip):
		"""executor

		Args:
			ip (str): ip address
		"""		
		self.ping_ms[ip] = ping(ip)
		self.ping_results[ip] = True if self.ping_ms[ip]  else False
		self.dns_result[ip] = nslookup(ip)

	def op_to_xl(self, opfile):
		"""write out result of pings to an output file

		Args:
			opfile (str): output excel file 
		"""		
		df = pd.DataFrame(self.result)
		df.to_excel(opfile, index_label='ip')



def compare_ping_sweeps(first, second):
	"""comparision of two ping result excel files 

	Args:
		first (str): ping result excel file-1
		second (str): ping result excel file-2

	Returns:
		None: Returns None, prints out result on console/screen
	"""	
	#
	df1 = pd.read_excel(first, index_col='ip').fillna('')
	df2 = pd.read_excel(second, index_col='ip').fillna('')
	#
	sdf1 = df1.sort_values(by=['ping_results', 'ip'])
	sdf2 = df2.sort_values(by=['ping_results', 'ip'])
	#
	pinging1 = set(sdf1[(sdf1['ping_results'] == True)].index)
	not_pinging1 = set(sdf1[(sdf1['ping_results'] == False)].index)
	pinging2 = set(sdf2[(sdf2['ping_results'] == True)].index)
	not_pinging2 = set(sdf2[(sdf2['ping_results'] == False)].index)

	# -----------------------------------------------------------------------------

	missing = pinging1.difference(pinging2)
	added = pinging2.difference(pinging1)
	if not missing and not added:
		s = f'All ping responce same, no changes'
		print(s)
		sg.Popup(s)
	else:
		if missing:
			s = f'\n{"="*80}\nips which were pinging in first file, but not pinging in second file\n{"="*80}\n{missing}\n{"="*80}\n'
			print(s)
			sg.Popup(s)
		if added:
			s = f'\n{"="*80}\nips which were not-pinging in first file, but it is pinging in second file\n{"="*80}\n{added}\n{"="*80}\n'
			print(s)
			sg.Popup(s)

	return None


# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------
class SubnetScan():
	def __init__(self):
		s = "Deprycated class, use `Nettoolkit` instead"
		print(s)
		sg.Popup(s)


# -----------------------------------------------------------------------------
# Execute
# -----------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ----------------------------------------------------------------------
