
Customize
============================================

SO YOU DECIDED TO CUSTOMIZE. HURREY !!! LETS DO IT !!!

-----

Customize ( Legacy Way - Deprycated )
-------------------------------------

After Previous First Steps, We can now add custom *classes & modules* as filters to be accessible inside jinja templates.

Refer below on how to fork them in.

* Functions import should be done via full module(s) import.
* Classes can be imported from diverse modules as individual entity.


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
    # Fork in all custom classes and modules to PrepareConfig object instance using below methods.
    # -------------------------------------------------------------------------------------------------------------
    PrCfg.custom_class_add_to_filter(**custom_classes)
    PrCfg.custom_module_methods_add_to_filter(*custom_modules)


.. note:: Congratulations!!!

    #. Now you can access **custom declared classes/methods** from **within jinja template** as **filters**. 


    It is soleley users responsiblity for providing appropriate filters as **custom_classes** and **custom_modules**, as well as deploying those appropriately in `jinja templates`.


Refer to ``Filters`` and ``Table Classes`` Section for more details. 


-----

Customize ( New Way - Preffered )
-------------------------------------

First define your custom classes and filters.
Than create a yaml file summarizing your custom classes and filters

.. code-block:: yaml

    ## content of file: custom.yaml

    j2_class_filters:
        Summaries: !!python/name:custom_j2config.classes_module.Summaries ''

    j2_functions_filters:
        private_summaries: !!python/name:custom_j2config.filters_module.private_summaries ''


You can now call it from your exec script, or provide the same yaml file in GUI mode as a custom yaml file input.

.. code-block:: python

    from nettoolkit.nettoolkit_common import read_yaml_mode_us
    from nettoolkit.j2config import PrepareConfig

    ## Read custom yaml file
    custom_file = "custom.yaml"
    custom = read_yaml_mode_us(custom_file)

    ## Define object instance of PrepareConfig
    PrCfg = PrepareConfig(
        data_file=data_file,               # your data excel
        jtemplate_file=template_file,      # your jinja template
        output_folder=output_folder,
    )

    ## Now fork in custom classes and filter functions to it
    custom_classes = {k: v for k, v in custom['j2_class_filters'].items() }
    custom_funcs = { v for k, v in custom['j2_functions_filters'].items() }
    PrCfg.custom_class_add_to_filter(**custom_classes)
    PrCfg.custom_module_methods_add_to_filter(*custom_funcs)

    ## start preparing
    PrCfg.start()


-----

Continue Next Page to start generating config.
