
# import pandas as pd
# from dataclasses import dataclass, field
# from nettoolkit.addressing import addressing
# # from nettoolkit.addressing import addressing, dec2dotted_ip, inv_subnet_size_to_mask, IPv4
# # from nettoolkit.nettoolkit_db import sort_dataframe_on_subnet, read_xl_all_sheet, read_an_xl_sheet
# from nettoolkit.addressing.summary import MASK_RANGE

# # =========================================================================================== 
# # Static Global Variable
# # =========================================================================================== 

# # =========================================================================================== 
# # Functions
# # =========================================================================================== 

# # =========================================================================================== 
# # Aggregation Class
# # =========================================================================================== 

# @dataclass
# class Allocate():
# 	prefix_size: int
# 	within_prefix: str
# 	container: bool = True
# 	subnet: bool = False
# 	# allocations: any = field(default_factory=None)

# 	def __post_init__(self):
# 		if not self.container and not self.subnet:
# 			raise Exception(f"Please provide Allocation type either container or subnet")
# 		#
# 		rpfx = addressing(within_prefix)		
# 		self.alloc_rng_start = rpfx.network_number_int
# 		self.alloc_rng_end   = rpfx.broadcast_number_int
# 		self.allocated_ranges = {}

# 	# def __call__(self):
# 	# 	self.allocate()


# 	def get_allocation_eligible_container(self):
# 		for range_tuple, dic in self.allocated_ranges.items():
# 			start = range_tuple[0]
# 			end = range_tuple[1]
# 			if start >= self.alloc_rng_start and end <= self.alloc_rng_end:
# 				container_for_allocation = dic
# 				return container_for_allocation
# 		return {}


# 	def create(self):
# 		for k, v in container_for_allocation.items():
# 			if k.get("container"):
# 				pass



# prefix_size = 27
# within_prefix = '10.10.10.0/24'

# A = Allocate(prefix_size, within_prefix)
# # print(A.alloc_rng_start, A.alloc_rng_end)
# gaec = A.get_allocation_eligible_container()
# print(gaec)