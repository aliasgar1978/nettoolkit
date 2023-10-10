
Juniper Configuration - Part 3
============================================

Remove the remarks and make clean configuration
----------------------------------------------------------------

It is used to remove the remarks from the Juniper output/configuration

Follow these three simple steps.

	#. Import necessary module from nettoolkit
	#. Define your input/output file.
	#. remove remarks.

Explanation in detail with sample code
-----------------------------------------

	Follow this. Create an execution .py file and use below code to run the utility::

		# step 1. - Import::
		from nettoolkit import Juniper

		# step 2. - Providing input and output
		input_file = "input_file_name.txt"
		output_file = input_file + "_clean.txt"

		# step 3. - Convert it.
		J = Juniper(input_file, output_file)	# define a Juniper Object
		s = J.remove_remarks(to_file=True)	# remove remarks from config


.. note::
		
	* **to_file** argument (True/False) in the ``remove_remarks`` method will enable or disable writing out output to external file.
	* return from ``remove_remarks()`` method will also be output in list format.



