
# ==========================================================================================
#  Imports
# ==========================================================================================

import os
from  pathlib import Path

# ==========================================================================================
# Functions
# ==========================================================================================

def get_file_path(file):
	"""returns folder of given file path

	Args:
		file (str): full string length file path

	Returns:
		str: folder location of file
	"""    	
	p = Path(file)	
	return p.parent

def get_file_name(file, ext=False):
	"""returns file name of given file path

	Args:
		file (str): full string length file path
		ext (bool, optional): include extension or not. Defaults to False.

	Returns:
		str: file name
	"""    	
	p = Path(file)	
	return p.name if ext else p.stem


def create_folders(folders, *, silent=True):
	"""Creates Folders

	Args:
		folders (list,str): folder(s)
		silent (bool, optional): Create without prompt. Defaults to True.

	Returns:
		bool: Success/Fail
	"""    	
	cf = 1
	if isinstance(folders, str):
		folders = [folders,]
	for folder in folders:
		if not os.path.exists(folder):
			if not silent: print(f"Creating: {folder}", end="\t")
			try:
				os.makedirs(folder)
				print("OK.")
			except:
				print("Failed.")
				cf = 0
	return bool(cf)
