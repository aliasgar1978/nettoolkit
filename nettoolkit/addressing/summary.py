
import pandas as pd
from dataclasses import dataclass, field
from nettoolkit.addressing import addressing, dec2dotted_ip, inv_subnet_size_to_mask, IPv4
from nettoolkit.nettoolkit_db import sort_dataframe_on_subnet, read_xl_all_sheet, read_an_xl_sheet

# =========================================================================================== 
# Static Global Variable
# =========================================================================================== 
# MASK_RANGE = {2**x:{'net':x , 'host':32-x} for x in range(32)}
MASK_RANGE = {
 1: {'host': 32, 'net': 0},
 2: {'host': 31, 'net': 1},
 4: {'host': 30, 'net': 2},
 8: {'host': 29, 'net': 3},
 16: {'host': 28, 'net': 4},
 32: {'host': 27, 'net': 5},
 64: {'host': 26, 'net': 6},
 128: {'host': 25, 'net': 7},
 256: {'host': 24, 'net': 8},
 512: {'host': 23, 'net': 9},
 1024: {'host': 22, 'net': 10},
 2048: {'host': 21, 'net': 11},
 4096: {'host': 20, 'net': 12},
 8192: {'host': 19, 'net': 13},
 16384: {'host': 18, 'net': 14},
 32768: {'host': 17, 'net': 15},
 65536: {'host': 16, 'net': 16},
 131072: {'host': 15, 'net': 17},
 262144: {'host': 14, 'net': 18},
 524288: {'host': 13, 'net': 19},
 1048576: {'host': 12, 'net': 20},
 2097152: {'host': 11, 'net': 21},
 4194304: {'host': 10, 'net': 22},
 8388608: {'host': 9, 'net': 23},
 16777216: {'host': 8, 'net': 24},
 33554432: {'host': 7, 'net': 25},
 67108864: {'host': 6, 'net': 26},
 134217728: {'host': 5, 'net': 27},
 268435456: {'host': 4, 'net': 28},
 536870912: {'host': 3, 'net': 29},
 1073741824: {'host': 2, 'net': 30},
 2147483648: {'host': 1, 'net': 31}
}

# =========================================================================================== 
# Functions
# =========================================================================================== 
def split_continuous_ranges(int_ranges):
	ranges = []
	for start, end in int_ranges:
		max_mask_range = max(get_range_parts(end-start+1))
		ip = dec2dotted_ip(start)
		for _ in reversed(MASK_RANGE):
			if _ > max_mask_range: continue
			i = addressing( ip + "/" + str(MASK_RANGE[_]['host']))
			if i.NetworkIP() == str(i):
				break
		ranges.append( (i.network_number_int, i.broadcast_number_int) )
		if i.network_number_int == start and i.broadcast_number_int == end:
			continue
		ranges.extend( split_continuous_ranges([(i.broadcast_number_int+1, end),]))
	return ranges


def get_range_parts(diff):
	mask_ranges = set() 
	for k in sorted(MASK_RANGE.keys()):
		if k > diff: break
		mask_ranges.add(k)
	return mask_ranges

def get_masks(lst, diff):
	l = sorted(lst)
	if diff == l[-1]: return {l[-1], }
	for x in l[:-1]:
		if l[-1] + x == diff:
			return {l[-1], x}
	return get_masks(l[:-1], diff-l[-1]) | {l[-1]}

# =========================================================================================== 
# Aggregation Class
# =========================================================================================== 
@dataclass
class Aggregate():
	prefixes: list[str] = field(default_factory=list)

	def __post_init__(self):
		self.sort_prefixes()
		self.pfxs_dict = {}
		self.get_ip_objects()
		self.count_start_stop()
		self.int_ranges = self.get_continuous_ranges()
		self.int_ranges = split_continuous_ranges(self.int_ranges)
		self.get_aggregates_from_ranges()

	def sort_prefixes(self):
		df = pd.DataFrame({'subnets': list(self.prefixes)})
		df = sort_dataframe_on_subnet(df, 'subnets')
		self.prefixes = list(df['subnets'])

	def get_ip_objects(self):
		for pfx in self.prefixes:
			try:
				if isinstance(pfx, str):
					self.pfxs_dict[IPv4(pfx)] = {}
				elif isinstance(pfx, IPv4):
					self.pfxs_dict[pfx] = {}
				else:
					raise Exception(f"Incorrect IP / Format Received {pfx}\n{e}")					
			except Exception as e:
				raise Exception(f"Incorrect IP / Format Received {pfx}\n{e}")


	def count_start_stop(self):
		for pfx in self.pfxs_dict.keys():
			self.pfxs_dict[pfx]['net_num'] = pfx.network_number_int
			self.pfxs_dict[pfx]['bc_num'] = pfx.broadcast_number_int

	def get_continuous_ranges(self):
		ranges = []
		for pfx, pfx_dict in self.pfxs_dict.items():
			if not ranges:
				ranges.append( (pfx_dict['net_num'], pfx_dict['bc_num']) ) 
				continue
			if ranges[-1][-1] + 1 != pfx_dict['net_num']:
				ranges.append( (pfx_dict['net_num'], pfx_dict['bc_num']) ) 
			else:
				ranges[-1] = ( ranges[-1][0], pfx_dict['bc_num'] )
		return ranges

	def get_aggregates_from_ranges(self):
		self._summaries = []
		for start, end in self.int_ranges:
			ip = addressing(f"{dec2dotted_ip(start)}/{inv_subnet_size_to_mask(end-start)}")
			if ip.network_number_int == start and ip.broadcast_number_int == end:
				self._summaries.append(ip)
				continue
			raise Exception(f"Script Error: Invalid Summary Found: {ip}")

	@property
	def aggregates(self):
		return self._summaries

	@property
	def summaries(self):
		return [str(_) for _ in self._summaries]

# =========================================================================================== 
def calc_summmaries(min_subnet_size, prefixes):
	"""summarize the provided network prefixes, provide all networks as arguments.
	minimum subnet summarized to provided min_subnet_size parameter

	Args:
		min_subnet_size (int): minimuze subnet mask to be summarized up on
		prefixes (list): networks 

	Returns:
		list: summaries
	"""    	
	summaries = Aggregate(prefixes).summaries
	nset = set()
	for subnet in summaries:
		if isinstance(subnet, IPv4) and subnet.mask > min_subnet_size:
			nset.add(subnet.expand(min_subnet_size))
		elif isinstance(subnet, str) and int(subnet.split("/")[-1]) > min_subnet_size:
			nset.add(IPv4(subnet).expand(min_subnet_size))
	summaries.extend(nset)
	nSummaries = Aggregate(summaries).summaries
	return nSummaries

# =========================================================================================== 

if __name__ == "__main__":
	pass
	from pprint import pprint
	# s = ['10.10.11.0/24', '10.10.13.0/24', '10.10.10.0/24', '10.10.14.0/24',]
	# # s = ['10.10.10.0/32', '10.10.10.1/32', '10.10.10.3/32','10.10.10.4/32']
	# # s = ['10.10.10.64/27', '10.10.10.32/27', '10.10.10.0/27', '10.10.10.128/27', '10.10.10.160/27',]
	# # s = ['10.10.10.64/27', '10.10.10.32/28', '10.10.10.48/29', '10.10.10.56/29', '10.10.10.16/28', '10.10.10.128/27', '10.10.10.160/27',]
	# s = ['9.240.192.0/23', '9.240.190.0/23', '9.240.194.0/23']
	# s = list({'9.239.250.64/26', '9.239.24.0/21', '9.236.130.0/23', '9.240.24.0/22', '9.239.250.128/25', '9.239.250.0/26'})
	# s = {'9.240.209.0/24', '9.240.80.0/23', '9.239.34.0/23', '9.240.152.0/22', '9.239.42.0/24', '9.239.36.0/22', '9.239.40.0/23'}
	# s = {'9.236.206.0/23', '9.236.202.0/22', '9.240.201.0/24'} 
	# s = {'9.233.10.0/23', '9.233.0.0/21'}

	# Agg = Aggregate(s)
	# print(Agg.prefixes)
	# print(Agg.summaries)
	# # print(Agg.aggregates)



	# file = "C:/Users/al202t/Documents/acc.y1_172.x_files/results - iga-accy1 - Legacy/2024-09-25/2.database/0. cur_networks.xlsx"
	# dfd = read_xl_all_sheet(file)
	# ndf = {}
	# for reso, df in dfd.items():
	# 	# if reso not in ("4an", "aag", "act","c4p", "cbo","d3f","d4t","e2s","f2w","hke","hur","svl",): continue
	# 	if reso != 'hke': continue
	# 	Agg = Aggregate(list(df['subnets']))
	# 	ndf[reso] = Agg.summaries
	# 	pprint(Agg.prefixes)

	# pprint(ndf)



	# from nettoolkit.nettoolkit_common import LST

	# folder = "C:/Users/al202t/Documents/iga-iiw 172.x Reip/results/2.database/"

	# fileold = f"{folder}0. cur_summaries - users - Copy.xlsx"
	# filenew = f"{folder}0. cur_summaries - users.xlsx"
	# old_df = read_an_xl_sheet(fileold)
	# new_df = read_an_xl_sheet(filenew)
	# for col in new_df:
	# 	new = set(LST.remove_empty_members( list(new_df[col] )))
	# 	old = set(LST.remove_empty_members( list(old_df[col]) ))
	# 	if old== new: continue
	# 	print(col, old, '\t', new)






