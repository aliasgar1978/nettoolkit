
# ===========================================================================
# Imports
# ===========================================================================
import re
from pathlib import Path

from .standardize import cisco_absolute_command, juniper_absolute_command

# ===========================================================================
def parse_network_output_file(file_path: str, cmd_registers: dict) -> dict:
	"""Parses a single Cisco or Juniper log file, removes terminal pagination artifacts,

	and returns a structured dictionary.
	"""
	path = Path(file_path)
	if not path.exists():
		raise FileNotFoundError(f"The file '{file_path}' does not exist.")

	content = path.read_text()

	# Regex extracts: Prompt components, Clean Hostname, and the Show Command
	command_pattern = re.compile(
		r"^(?P<prompt>(?:(?P<user>[\w\-]+)@)?(?P<hostname>[\w\.\-]+)(?:[\s\(\)\w\-]*)[#>])\s*(?P<command>show\s+.+)$",
		re.MULTILINE | re.IGNORECASE,
	)

	matches = list(command_pattern.finditer(content))

	if not matches:
		return {"hostname": "", "make": "", "cmd_op": {}}

	# Extract device metadata from the very first matched command line
	first_match = matches[0]
	device_hostname = first_match.group("hostname").strip()
	has_user_prefix = first_match.group("user") is not None

	# Determine make: Juniper usually includes 'user@hostname' or starts with root
	# Cisco typically defaults to straight 'hostname#'
	if has_user_prefix or "root" in first_match.group("prompt").lower():
		device_make = "juniper"
	else:
		device_make = "cisco"

	# Build the outputs dictionary
	cmd_op_dict = {}

	for i, match in enumerate(matches):
		command = match.group("command").strip()
		start_pos = match.end()

		# Output ends where the next command starts, or at the end of the file
		end_pos = (
			matches[i + 1].start() if i + 1 < len(matches) else len(content)
		)
		raw_output = content[start_pos: end_pos].strip()

		# 1. Clean up: strip out any trailing terminal prompt line at the end of output
		clean_output = re.sub(r"\n.*?[#>]?\s*$", "", raw_output).strip()

		# 2. Clean up: remove '--More--', '---(more)---', and hidden backspace/space characters (\x08 or \x20)
		# This handles lines like " --More--         \x08\x08\x08\x08\x08\x08\x08\x08"
		clean_output = re.sub(
			r"\s*--+\s*[Mm]ore\s*--+[\s\x08]*", "", clean_output
		)
		clean_output = re.sub(
			r"\s*---+\s*\(more\)\s*---+[\s\x08]*", "", clean_output
		)

		if device_make == 'cisco':
			abs_cmd_func = cisco_absolute_command
			cmd_register = cmd_registers['cisco']
		elif device_make == 'juniper':
			abs_cmd_func = juniper_absolute_command
			cmd_register = cmd_registers['juniper']

		cmd_op_dict[abs_cmd_func(command, cmd_register)] = clean_output.strip().split("\n")

	# Construct and return output schema
	return {
		"hostname": device_hostname,
		"make": device_make,
		"cmd_op": cmd_op_dict,
	}

# ===========================================================================
#  Main 
# ===========================================================================
# --- Example Execution ---
if __name__ == "__main__":
	pass

# ===========================================================================

__all__ = ['parse_network_output_file', ]


