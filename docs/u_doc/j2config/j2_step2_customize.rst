
Customize
============================================

SO YOU DECIDED TO CUSTOMIZE. HURREY !!!

FOLLOW ALONG.

-----

After Previous First Steps, We can now add custom *classes & modules* as filters to be accessible inside jinja templates.

Refer below on how to use them.

* module import should declare pure methods only. and should be imported as full module 
* Classes should be imported explicitely from diverse modules.


.. code-block:: python

    # -------------------------------------------------------------------------------------------------------------
    # Custom Project Imports (Optional/Additional), sample project imports mentioned as below. (modify as per own)
    # -------------------------------------------------------------------------------------------------------------
    from custom.custom_j2config.classes import Summaries, Vrf, Vlan, Bgp, Physical # filter classes import
    from custom.custom_j2config import module1                                     # import full module(s), consisting filter methods

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

    #. Now you can access custom declared classes/methods from within jinja template as filters. 
    #. And you already override device `var` database using custom regional_file database in previous step.


    It is soleley users responsiblity for providing appropriate filters as **custom_classes** and **custom_modules**, as well as deploying those appropriately in `jinja templates`.


-----

Continue Next Page to start generating config.