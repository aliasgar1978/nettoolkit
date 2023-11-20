
Custom Modifications
===================================================

Apart from usual previous steps: 
	* We can now add the custom *classes, modules* to be accessible over jinja templates.
	* We can now override device *var* databse with custom (regional_file) database.

Refer below details on how to use them.

* Full module import should declare pure methods only.  
* Classes should be imported explicitely from diverse modules.

-----


**Detailed How To**


	#. Import necessary custom class(es) from module, and/or import necessary module(s).

		**Below depicts a Sample Code.** 
		Modify it as per your custom class(es) requirements.

		.. code::

			# Imports
			from custom_j2config.classes import Summaries, Vrf, Vlan, Bgp, Physical
			from custom_j2config import module1
			from custom_j2config.regional import Region    # available for j2config verion > 0.0.6 

			# Custom global/Regional static variable excel database to override device local variables (optional)
			regional_file = 'global.xlsx'                # point to custom file



	#. Include all imported classes and modules in to a dictionary and set respectively as given sample below.

		.. code::

			custom_classes = {           ### add all impored classes here ###
				'Summaries': Summaries,
				'Vrf': Vrf,
				'Vlan': Vlan,
				'Bgp': Bgp,
				'Physical': Physical
			}
			custom_modules = {module1, }  ### add all imported modules here ###


	#. Modify PrepareConfig instance filters (created in previous page)

		.. code:: python

			### From previous step ###
			PrCfg = PrepareConfig(
				data_file=data_file, 
				jtemplate_file=template_file, 
				output_folder=output_path,             ## optional (default: ".")
				regional_file=regional_file,           ## default: None
				regional_class=Region                  ## default: None
			)

			### Add below two additional steps to include custom class/module methods as filter to jinja processsing.
			### 1. Add Custom classes to above instance using `custom_class_add_to_filter`.
			PrCfg.custom_class_add_to_filter(**custom_classes)

			### 2. Add Custom modules to above instance using `custom_module_methods_add_to_filter`.
			PrCfg.custom_module_methods_add_to_filter(*custom_modules)


	#. Start configuration generation

		.. code:: python

			PrCfg.start()


-----


.. note:: Congratulations!!!

	#. Hurrey!!! Now you can access custom declared classes/methods from within jinja template. 
	#. And you can override device `var` database using custom regional_file database.



.. admonition:: Notice

	* Make a note that output generates based on jinja template and template variables.		
	* It is soleley users responsiblity for providing appropriate filters as ``custom_classes`` and ``custom_modules``, as well as using those in `jinja templates`.
	* Make sure to cross-check the generated facts before using it.

