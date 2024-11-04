"""Description: 
"""

# ==============================================================================================
#  Imports
# ==============================================================================================
from dataclasses import dataclass, field
from pathlib import Path
import sys, os
import textfsm
from nettoolkit.nettoolkit_common import get_file_name, get_file_path, DIC
from nettoolkit.nettoolkit_db import dict_to_yaml

merge_dict = DIC.merge_dict

# ==============================================================================================
#  Local Statics
# ==============================================================================================


# ==============================================================================================
#  Local Functions
# ==============================================================================================
def parse_to_list_cmd(abs_cmd, data_list, cmd_parser_file_map):
	template_file = get_template_file(abs_cmd, cmd_parser_file_map)
	return parse_to_list(template_file, data_list)

def parse_to_dict_cmd(abs_cmd, data_list, cmd_parser_file_map):
	template_file = get_template_file(abs_cmd, cmd_parser_file_map)
	return parse_to_dict(template_file, data_list)

def parse_to_list(template_file, data_list):
	data = "\n".join(data_list)
	with open(template_file) as f:
		textfsm_parser = textfsm.TextFSM(f)
		parsed_data = textfsm_parser.ParseText(data)
	return parsed_data

def parse_to_dict(template_file, data_list):
	data = "\n".join(data_list)
	with open(template_file) as f:
		textfsm_parser = textfsm.TextFSM(f)
		parsed_data = textfsm_parser.ParseTextToDicts(data)
	return parsed_data



def get_template_dir():
	folder = ""
	for path in sys.path:
		p = Path(path)
		if not p.is_dir(): continue
		if p.name == "site-packages" :
			folder = p
			break
	if not folder:
		print(f"Could not locate ntc template directory...")
	template_dir = p.resolve().parents[0].joinpath("site-packages/ntc_templates/templates")
	return template_dir

def get_template_file(abs_cmd, cmd_parser_file_map):
	p = get_template_dir()
	if not cmd_parser_file_map.get(abs_cmd): return ""
	return str(p.joinpath(cmd_parser_file_map[abs_cmd]))


# ==============================================================================================
#  Classes
# ==============================================================================================
@dataclass
class CommonParser():
	captures: any
	output_folder: str=''

	def __post_init__(self):
		self.device_dict = {}
		self.parse()
		self.set_output_yaml_filename()
		self.write_yaml()

	@property
	def output_yaml(self):
		return self._yaml_file

	def set_output_yaml_filename(self):
		try:
			if not self.output_folder:
				self.output_folder = get_file_path(self.captures.capture_log_file)
			else:
				self.output_folder = Path(self.output_folder)
			hostname = get_file_name(self.captures.capture_log_file)
			self._yaml_file = self.output_folder.joinpath(hostname + ".yaml")
		except:
			raise Exception(f"Error determining output yaml file, either input is invalid.")

	def write_yaml(self):
		dict_to_yaml(self.device_dict, file=self.output_yaml, mode='w')

	def parse(self):
		for cmd, funcs in self.cmd_fn_parser_map.items():
			cmd_output = self.captures.cmd_output(cmd)
			if not cmd_output: 
				print(f"{self.captures.name}: [{cmd}] output missing")
				continue
			for fn in funcs:
				self.parse_func(fn, cmd_output)


	def parse_func(self, fn, cmd_output):
		parsed_fields = fn(cmd_output)
		self.add_parsed_fields_to_device_dict(parsed_fields)

	def add_parsed_fields_to_device_dict(self, parsed_fields):
		merge_dict(self.device_dict, parsed_fields)


# ==============================================================================================
#  Main
# ==============================================================================================
if __name__ == '__main__':
	pass

# ==============================================================================================
