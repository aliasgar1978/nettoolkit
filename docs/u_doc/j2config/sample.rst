
Sample Execution Code
===================================================



A Sample Execution File
----------------------------------------------


:download:`Sample Execution File <files/exec-j2config.py>`. A sample execution file will look similar to this

Given script follows below file tree structure.


-----


Folder Tree Structure
----------------------------------------------

	#. Either maintain the tree structure as mentioned here or modify the code as per your requirement::

		Parent
		|
		| - + myPrograms
		|   | - exec-j2config.py
		|
		| - + captures ( contains all Excel clean files )
		|   | - xxx1-clean.xlsx
		|   | - xxx2-clean.xlsx
		|   | - xxx3-clean.xlsx
		|
		| - + jtemplates   ( containing all jinja template files, and global variable file )
		|   | - jinja_template1.j2
		|   | - jinja_template2.j2
		|   | - jinja_template3.j2
		|   | - global.xlsx
		|
		| - + j2-outputs   ( folder where outputs will be stored )
		    | - generated config will appear here.


-----


* If you are changing the Tree structure, than modify your execution script accordingly to read the files from appropriate path.