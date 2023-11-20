
Using j2config
============================================

	#. import necessary module
	#. define inputs
	#. prepare configurations using inputs.


-----


**Detailed How To**

	#. Import necessary package, modules

		.. code::

			from nettoolkit.j2config import PrepareConfig


	#. Define your input files ( i.e. captures )

		.. code::

			data_file = "excel-datafile.xlsx"       # provide Excel database file 
			template_file = "text_template.j2"      # provide text jinja template file.
			output_path = "./output/"               # provide path where new config to be stored.(optional)


		.. attention::
			
			**Excel Data File**

			* It is advisable to generate the facts using  **facts_finder** package. So manual editing will be minimal. Otherwise a fresh manually prepared database will work either.
			* There must be a ``var`` tab in excel file. with **var** as jinja variable and **default** as replacement value of the jinja variable.
				* multiple values for a single variable can be added in a same cell by separating either by ``comma`` or ``enter``
			* There must be atleast one tabular column consisting interfaces details.
				* multiple type interface details can be in separate sheet as well. sheet name can be arbitrary any thing.
			* There can be a ``vrf`` tab consisting of instances details of device.
			* There can be a ``bgp`` tab consisting of bgp and its properties of device.


			* global variable file should be identical to ``var`` tab of data file. with two columns as **var** and **default**.



	#. Generate Config from database and template

		.. code:: python

			PrCfg = PrepareConfig(
				data_file=data_file,
				jtemplate_file=template_file,
				output_folder=output_path,             ## optional (default: ".")
			)


	#. Start configuration generation

		.. code:: python

			PrCfg.start()


-----


.. admonition:: Notice

	* Make a note that output generates based on jinja template and template variables.		
	* Make sure to cross-check the generated facts before using it.

