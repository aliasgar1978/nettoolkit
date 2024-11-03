"""Description: 
"""
from pprint import pprint
# ==============================================================================================
#  Imports
# ==============================================================================================
from dataclasses import dataclass, field
from nettoolkit.nettoolkit_common import CapturesOut
from nettoolkit.yaml_facts.cisco import CiscoParser
from nettoolkit.yaml_facts.juniper import JuniperParser

# ==============================================================================================
#  Local Statics
# ==============================================================================================



# ==============================================================================================
#  Local Functions
# ==============================================================================================



# ==============================================================================================
#  Classes
# ==============================================================================================

@dataclass
class YamlFacts():
	capture_log_file: str
	output_folder: str=''

	parser_cls_map = {
		'Cisco': CiscoParser,
		'Juniper': JuniperParser,
	}

	def __post_init__(self):
		self.captures = CapturesOut(self.capture_log_file)
		self.CP = self.parser_cls_map[self.captures.device_manufacturar](self.captures, self.output_folder)



# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass
	# file = "C:/Users/al202t/Documents/A T M/Captures/530-vua-1f1.log"
	file = "C:/Users/al202t/Documents/A T M/Captures/530-end.log"
	# file = 'C:/Users/al202t/Documents/A T M/Captures/z3o-ecd-b.log'

	FR = YamlFacts(file)	
	# pprint(FR.captures.outputs)
	# pprint(FR.captures.device_manufacturar)
	# print(FR.captures.outputs.keys())
	# pprint(FR.captures.cmd_output("show running-config"))
	# print(FR.captures.has("show version"))

	# print(FR.CP.output_yaml)

# ==============================================================================================
