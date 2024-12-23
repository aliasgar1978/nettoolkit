# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
from dataclasses import dataclass, field
from nettoolkit.nettoolkit_common.gpl import STR

# ---------------------------------------------------------------------------- 
# J-Set
# ----------------------------------------------------------------------------
@dataclass
class JSet(STR):
	input_file: str = ''
	input_list: list[str,] = field(default_factory=list)

	def __post_init__(self):
		self.output = []
		self.err = False
		self._set_input_lists()
		self._validate_input_list()

	def __call__(self):
		self.convert_to_set()
		return self.output

	@property
	def objVar(self): return self.output

	def _set_input_lists(self):
		"""set input list from either provided input.
		input file is prefereed over input list.
		"""		
		if self.input_file:
			self._read_input_file()
		if not self.input_list:
			raise Exception(f"No input detected, Requires One\n  Got input_file:{self.input_file}, input_list:{self.input_list}")

	def _read_input_file(self):
		"""Reads input file and set input list

		Raises:
			Exception: InputFileReadError
		"""		
		try:
			with open(self.input_file, "r") as f:
				self.input_list = f.readlines()
		except:
			raise Exception(f"InvalidInputError: input file invalid or read error - {self.input_file}")

	def _validate_input_list(self):
		"""Reads input list as input list

		Raises:
			Exception: InputListReadError
		"""		
		if not isinstance(self.input_list, (list, tuple)):
			raise Exception(f"InputListReadError: must if of type either list or tuple, got {type(self.input_list)}")

	def convert_to_set(self):
		"""reads juniper standard config and convert it to set, store it to output
		"""
		line_counter = 0
		multiline_string_prev_line = ''
		_set = 'set'
		left_str = ''
		bt_item_in_orders = []
		self.annotation = ''
		undefined_line_printed = False

		for line in self.input_list:
			line_counter += 1
			stripped_line = line.strip()

			### --- Terminated Multiline string --- ###
			multiline_string_prev_line, terminate = self._get_multiline_str(multiline_string_prev_line, stripped_line)
			if not terminate: continue
			if multiline_string_prev_line:
				stripped_line, multiline_string_prev_line = multiline_string_prev_line, ''
			### ----------------------------------- ###

			stripped_line = self.delete_trailing_remarks(stripped_line) 		       # Remove Trailing remarks				
			stripped_line_length = len(stripped_line)
			if self.is_remarked_line(stripped_line): continue
			if self.is_blank_line(stripped_line): continue
			annotation_line = self.save_last_annotation(stripped_line)
			if annotation_line: continue

			if self.is_brckt_start(stripped_line):
				bt_item_in_orders.append(left_str)
				left_str += " " + stripped_line[:-1].strip() 
				continue

			if self.is_brckt_end(stripped_line):
				left_str = bt_item_in_orders[-1]
				bt_item_in_orders.pop()
				continue

			if self.is_end_of_line(stripped_line):
				if self.is_multisection_inputs(stripped_line):
					self.output.extend(self.get_extended_output_lines(left_str, stripped_line))
				else:
					self.output.append(self.get_output_line(left_str, stripped_line))

				# Add comments if any
				if self.annotation:
					self.output[-1] += self.annotation
					self.annotation = ''
				continue

			if undefined_line_printed: continue
			print(f"[-] Juniper set converter: Skipping one or more un-identified Line(s).")
			undefined_line_printed = True



	@staticmethod
	def _get_multiline_str(multiline_string_prev_line, current_line):
		## Broken line: start..
		if current_line.find("[ ") > -1 and not current_line.endswith("];"):
			return (current_line, False)

		## Broken lines: middle and end
		if multiline_string_prev_line:
			new_line = multiline_string_prev_line + " " + current_line
			return (new_line, current_line.endswith('];'))

		## Normal lines..
		return ('', True)

	@staticmethod
	def is_remarked_line(line):
		return line.startswith("#")

	@staticmethod
	def is_blank_line(line):
		return not line

	@staticmethod
	def get_line_items(line):
		return line.split()

	def save_last_annotation(self, line):
		if line.endswith("/") :        # /comment/ lines
			self.annotation = "  ## comment: " + line.strip()
			return True

	@staticmethod
	def is_brckt_start(line):
		return line.endswith("{")

	@staticmethod
	def is_brckt_end(line):
		return line.endswith("}")

	@staticmethod
	def is_end_of_line(line):
		return line.endswith(";")

	@staticmethod
	def is_multisection_inputs(line):
		return line[:-1].rstrip().endswith("]")

	@staticmethod
	def get_output_line(left_str, line):
		return f'set {left_str.strip()} {line[:-1]}'

	@staticmethod
	def get_extended_output_lines(left_str, line):
		bracket_start_pos, bracket_end_pos = line.find("["), line.find("]")
		bracket_items = line[bracket_start_pos+1: bracket_end_pos].strip().split()
		prefix_str = line[:bracket_start_pos].strip()
		return [f"set {left_str.strip()} {prefix_str} {item}" for item in bracket_items]


	## for backward compatibility ##
	@property
	def to_set(self):
		return self()

	def remove_remarks_from_config(self):
		"""reads juniper standard config and removes remarks of it
		"""
		end_chars = ( "{", "}", ";" )
		plain_config_list = []
		multiline_string_prev_line = ''
		for line in self.input_list:
			stripped_line = self.delete_trailing_remarks(line.strip())
			annotation_line = self.save_last_annotation(stripped_line)
			multiline_string_prev_line, terminate = self._get_multiline_str(multiline_string_prev_line, stripped_line)
			#
			if stripped_line.endswith(end_chars) or annotation_line or terminate or multiline_string_prev_line:
				plain_config_list.append(line.rstrip('\n'))
		return plain_config_list

# =============================================================================================
#  Main
# =============================================================================================
if __name__ == '__main__':
	pass
# =============================================================================================
