
Customize
============================================

SO YOU DECIDED TO CUSTOMIZE.  FOLLOW BELOW STEPS AND YOU ARE ON. HERE IT IS HOW

-----

After Previous First Steps: 
	* We can now add filters as custom *classes, modules* to be accessible inside jinja templates.
	* To override *var* tab databse define a separate custom class (ex: Region) to work with custom (regional_file) database.

Refer below on how to use them.

* Full module import should declare pure methods only.  
* Classes should be imported explicitely from diverse modules.


.. code-block:: python

    # -------------------------------------------------------------------------------------------------------------
    # Custom Project Imports (Optional/Additional), sample project imports mentioned as below. (modify as per own)
    # -------------------------------------------------------------------------------------------------------------
    from custom.custom_j2config.classes import Summaries, Vrf, Vlan, Bgp, Physical # filter classes import
    from custom.custom_j2config import module1                                     # import full module(s), consisting filter methods
    from custom.custom_j2config.regional import Region      # Regional class definition, works with regional_file provided in step1. And override device 'var' data

    # -------------------------------------------------------------------------------------------------------------
    # Input all Additional filter classes as a Dictionary, can be called using their Key.
    # -------------------------------------------------------------------------------------------------------------
    custom_classes = {
        'Summaries': Summaries, 
        'Vrf': Vrf,
        'Vlan': Vlan,
        'Bgp': Bgp, 
        'Physical': Physical,
        ## add more classes as necessary, after import ##
    }

    # -------------------------------------------------------------------------------------------------------------
    # Input all Additional filter modules containing methods to a set.
    # -------------------------------------------------------------------------------------------------------------
	custom_modules = {module1, }						## add more modules as necessary, after import

    # -------------------------------------------------------------------------------------------------------------
    # Add all custom classes and modules to PrepareConfig object instance using below methods.
    # -------------------------------------------------------------------------------------------------------------
	PrCfg.custom_class_add_to_filter(**custom_classes)
	PrCfg.custom_module_methods_add_to_filter(*custom_modules)


.. note:: Congratulations!!!

	#. Hurrey!!! Now you can access custom declared classes/methods from within jinja template. 
	#. And you can override device `var` database using custom regional_file database.


	It is soleley users responsiblity for providing appropriate filters as ``custom_classes`` and ``custom_modules``, as well as deploying those appropriately in `jinja templates`.


-----

Continue Next Page to start generating config.