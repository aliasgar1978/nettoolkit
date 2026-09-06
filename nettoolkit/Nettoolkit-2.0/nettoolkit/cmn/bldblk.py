
# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from inspect import signature
from abc import ABC, abstractmethod
from collections import OrderedDict

# -----------------------------------------------------------------------------
class Default():
	"""Default class representing class docString template"""
	def __str__(self): return self.__doc__
	def _repr(self):
		fields = signature(self.__init__).parameters
		values = ", ".join(repr(getattr(self, f)) for f in fields)
		return f'{type(self).__name__}({values})'



class Container(ABC):
	"""Abstract base class providing template for standard dunder 
	methods template.  Object should contain objVar property
	"""	

	@abstractmethod
	@property
	def objVar(self): pass
	def __bool__(self): return True if self.objVar else False
	def __len__(self): return len(self.objVar)
	def __dir__(self): return self.objVar # sorted
	def __getitem__(self, i): return self.objVar[i]
	def __setitem__(self, i, v): self.objVar[i] = v
	def __delitem__(self, i): del(self.objVar[i])
	def __contains__(self, i): return i in self.objVar
	def __reversed__(self): 
		if isinstance(self.objVar, dict):
			for k in reversed(tuple(self.objVar.keys())):
				yield (k,self[k])
		else:
			return reversed(self.objVar)
		
	def __missing__(self, i): raise Exception(f'[-] key {i} unavailable') # only for dict subclass
	def __iter__(self):
		if isinstance(self.objVar, (list, tuple, set, str)):
			for line in self.objVar:
				yield line
		elif isinstance(self.objVar, (dict, OrderedDict)):
			for key, value in self.objVar.items():
				yield (key, value)

## TBD / NOT IMPLEMENTED YET ##
# class Numeric():
# 	"""Support Numberic objects"""
# 	def __add__(self): pass
# 	def __sub__(self): pass
# 	def __mul__(self): pass
# 	def __truediv__(self): pass
# 	def __floordiv__(self): pass
# 	def __pow__(self): pass
# 	def __lshift__(self): pass
# 	def __rshift__(self): pass
# 	def __and__(self): pass
# 	def __xor__(self): pass
# 	def __or__(self): pass

# 	def __iadd__(self): pass
# 	def __isub__(self): pass
# 	def __imul__(self): pass
# 	def __itruediv__(self): pass
# 	def __ifloordiv__(self): pass
# 	def __ipow__(self): pass
# 	def __ilshift__(self): pass
# 	def __irshift__(self): pass
# 	def __iand__(self): pass
# 	def __ixor__(self): pass
# 	def __ior__(self): pass

# 	def __neg__(self): pass
# 	def __pos__(self): pass
# 	def __abs__(self): pass
# 	def __invert__(self): pass


# ------------------------------------------------------------------------------
if __name__ == '__main__': pass
# ------------------------------------------------------------------------------
