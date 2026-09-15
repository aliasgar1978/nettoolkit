
# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from abc import abstractmethod
import threading
from time import sleep
import logging


from .bldblk import Default
from .fstr import list_of_devices, split_to_group

# -----------------------------------------------------------------------------
#                           Execution secquences                              #
# -----------------------------------------------------------------------------

class Multi_Execution(Default):
	"""Template methods for multi-threaded executions.
	[self.items items are eligible threaded candidates]
	"""

	max_connections = 100
	sleep_by = 0

	def __str__(self): return self._repr()

	def __init__(self, items=None):
		self.items = items
		self.workers = min(self.max_connections, len(self.items))

	def execute_steps(self, multi_thread=True):
		"""steps defining executions

		Args:
			multi_thread (bool, optional): Multithread or Sequencial. Defaults to True.
		"""		
		self.start(multi_thread)

	def start(self, multi_thread=True):
		"""starting up executins either threaded/sequencial

		Args:
			multi_thread (bool, optional): Multithread or Sequencial. Defaults to True.

		Returns:
			None: None
		"""		
		if not self.items: return None 
		logging.info(f"{self} - Starting MT Execution")
		if multi_thread:
			self.execute_mt()
		else: 
			self.execute_sequencial()
		logging.info(f"{self} - Completed MT Execution")

	def end(self):
		"""Closure process"""		
		pass

	def execute_mt(self):
		"""threaded execution in groups 
		(self.max_connections defines max threaded processes) 
		"""
		for items in split_to_group(self.items, self.max_connections):
			self.execute_threads_max(items)

	def execute_threads_max(self, item_list):
		"""threaded execution of a group

		Args:
			item_list (list, set, tuple): items to be iterated on
		"""		
		ts = []
		for hn in item_list:
			t = threading.Thread(target=self.execute, args=(hn,) )
			t.start()
			ts.append(t)
			if self.sleep_by and isinstance(self.sleep_by, (int, float)):
				sleep(self.sleep_by)

		for t in ts: t.join()

	def execute_sequencial(self):
		"""sequencial execution of items
		"""
		for hn in self.items: self.execute(hn)

	@abstractmethod
	@classmethod
	def execute(self, hn): 
		"""abstract class method, to be executed for each item in self.items

		Args:
			hn (str, int, float): individual items to be executed for each
		"""		
		pass


# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------

__all__ = ['Multi_Execution']