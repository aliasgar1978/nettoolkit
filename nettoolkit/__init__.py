__doc__ = '''Networking ToolSet
'''

__all__ = [

	#gui
	"Nettoolkit",


	]

__version__ = "0.1.2"

from .gui import Nettoolkit


def version():
	return __version__