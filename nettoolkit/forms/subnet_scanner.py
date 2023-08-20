

import PySimpleGUI as sg

from nettoolkit.gpl import STR, LOG
from nettoolkit.forms.formitems import *
from nettoolkit.subnetscan import get_first_ips, Ping


def subnet_scanner_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['op_folder'] != '' and i['pfxs'] != "":
			file = 'ping_scan_result_'
			op_file = f"{STR.get_logfile_name(i['op_folder'], file, ts=LOG.time_stamp())[:-4]}.xlsx"
			pfxs = get_list(i['pfxs'])
			try:
				concurrent_connections = int(i['sockets'])
			except:
				concurrent_connections = 1000
			#
			new_iplist = get_first_ips(pfxs, i['till'])
			P = Ping(new_iplist, concurrent_connections)
			P.op_to_xl(op_file)
			sg.Popup("Scan completed, \nFile write completed, \nVerify output")
			return True
	except:
		return None

def subnet_scanner_frame():
	"""tab display - subnet scanner

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('IP Subnet Scanner', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('select output folder :',  text_color="yellow"), 
			sg.InputText('', key='op_folder'),   sg.FolderBrowse(),
		],
		# under_line(80),
		[sg.Text("Prefixes - enter/comma separated", text_color="yellow")],
		[sg.Multiline("", key='pfxs', autoscroll=True, size=(30,14), disabled=False) ],
		# under_line(80),
		[sg.Text('[n]', text_color="yellow"), sg.InputCombo(list(range(1,256)), key='till', size=(20,1)),  
		sg.Text('Concurrent connections', text_color="yellow"), sg.InputText(1000, key='sockets', size=(20,1))],  
		under_line(80),
		[sg.Button("Start", change_submits=True, key='go_subnet_scanner')],

		])

