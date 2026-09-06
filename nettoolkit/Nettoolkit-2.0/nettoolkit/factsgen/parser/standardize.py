
# ===========================================================================
# Imports
# ===========================================================================

# ===================================================================================
#  GET Cisco ABSOLUTE COMMAND 
# ===================================================================================
def cisco_absolute_command(cmd, cmd_register):
	"""returns absolute full command for shorteened cmd
	if founds an entry in cmd_parser_map keys.

	Args:
		cmd (str): executed/ captured command ( can be trunked or full )

	Returns:
		str: cisco command - full untrunked
	"""
	spl_cmd = cmd.split()
	for c_cmd in cmd_register:
		spl_c_cmd = c_cmd.split()
		if len(spl_cmd) == len(spl_c_cmd):
			for i, word in enumerate(spl_cmd):
				try:
					word_match = spl_c_cmd[i].startswith(word)
					if not word_match: break
				except:
					word_match = False
					break
			if word_match: break
		else:
			word_match = False
	if word_match:  return c_cmd
	return cmd
# ===================================================================================

def juniper_absolute_command(cmd, cmd_register, op_filter=False):
	"""returns absolute truked command if any filter applied
	if founds an entry in juniper_commands_parser_map keys.

	Args:
		cmd (str): executed/ captured command ( can be trunked or full )
		op_filter (bool, optional): to be remove any additional filter from command or not. Defaults to False.

	Returns:
		str: juniper command - trunked
	"""    	
	cmd = cmd.replace("| no-more", "").strip()
	if op_filter:
		cmd = cmd.split("|")[0].strip()
	for j_cmd in cmd_register:
		exact_match = cmd == j_cmd
		if exact_match: break
	if exact_match:  return cmd
	return cmd


# ===================================================================================

# ===========================================================================
#  Main 
# ===========================================================================
# --- Example Execution ---
if __name__ == "__main__": pass
# ===========================================================================

__all__ = ['cisco_absolute_command', 'juniper_absolute_command']