

import pyfiglet
from colorama import Fore
from tabulate import tabulate
 
DEBU = Fore.CYAN
INFO = Fore.GREEN
WARN = Fore.BLUE
ERRO = Fore.YELLOW
CRIT = Fore.RED
NORM = Fore.WHITE

fore_color_map = {
	'cyan': Fore.CYAN,
	'green': Fore.GREEN,
	'blue': Fore.BLUE,
	'yellow': Fore.YELLOW,
	'red': Fore.RED,
	'white': Fore.WHITE,
	None: Fore.WHITE,
	'black': Fore.BLACK,
	'magenta': Fore.MAGENTA,

}

def print_banner(banner, color):
	try:
		banner = pyfiglet.figlet_format(banner, font='doom')
		print(fore_color_map[color] + '\n' + banner)
		print(Fore.WHITE + "")
	except:
		pass
# --------------------------------------------------------------------
## REPLACED with below dic_to_table()
## INSTEAD OF PRINT IT DOES RETURN - print requires exclusively
## Eample:  print(dic_to_table(device_log_dict))
# --------------------------------------------------------------------
# def print_table(df, tablefmt='rounded_outline'):
# 	try:
# 		printable = tabulate(df, headers='keys', tablefmt=tablefmt)
# 		print(printable)
# 	except:
# 		print(f"[-] Unable to print table.")
# --------------------------------------------------------------------


def dic_to_table(data_dict, tablefmt='rounded_outline'):
    try:
        # Create rows by merging the outer key (e.g., Device ID) with its inner data
        table_data = []
        headers = ["Device"]  # Label for the outer dictionary keys
        
        # Get headers from the first item's keys
        first_key = next(iter(data_dict))
        headers.extend(data_dict[first_key].keys())
        
        for key, details in data_dict.items():
            row = [key] + list(details.values())
            table_data.append(row)
            
        # Print using tabulate
        printable = tabulate(table_data, headers=headers, tablefmt=tablefmt)
        return  printable
    except Exception as e:
        print(f"[-] Unable to convert table. Error: {e}")