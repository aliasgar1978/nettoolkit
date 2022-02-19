
Juniper Configuration - Part 1
============================================

Convert from Standard to Set command
-----------------------------------------

It is ease to convert the Juniper standard (Hierarchical/Bracket) configurations to 
set commands. 

Follow these three simple steps.

	#. Import necessary module from nettoolkit
	#. Define your input/output file.
	#. Convert it.

Explanation in detail with sample code
-----------------------------------------

	Follow this. Create an execution .py file and use below code to run the utility::

		# step 1. - Import::
		from nettoolkit import Juniper

		# step 2. - Providing input and output
		input_file = "input_file_name.txt"
		output_file = input_file + "_set.txt"

		# step 3. - Convert it.
		J = Juniper(input_file, output_file)	# define a Juniper Object
		s = J.convert_to_set(to_file=True)	# convert the Juniper config to set mode.


.. note::
		
	* **to_file** argument (True/False) in the ``convert_to_set`` method will enable or disable writing out output to external file.
	* return from ``convert_to_set()`` method will also be set command output in list format.
	* any error in input file may result the conversion to halt. In this case, get hint on console window; on the line number; where it stops and gt error from input_file.



