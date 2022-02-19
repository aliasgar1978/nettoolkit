
Juniper Configuration - Part 2
============================================

Convert from set commands to standard hierachical commands
----------------------------------------------------------------

It is used to convert the Juniper set commands output/configuration to standard (Hierarchical/Bracket) configurations. 

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
		output_file = input_file + "_bracket.txt"

		# step 3. - Convert it.
		J = Juniper(input_file, output_file)	# define a Juniper Object
		s = J.convert_to_hierarchy(to_file=True)	# convert the Juniper config to hierachical mode.


.. note::
		
	* **to_file** argument (True/False) in the ``convert_to_hierarchy`` method will enable or disable writing out output to external file.
	* return from ``convert_to_hierarchy()`` method will also be hierachical command output in list format.
	* any error in input file may result the conversion to halt. In this case, get hint on console window; on the line number; where it stops and gt error from input_file.



