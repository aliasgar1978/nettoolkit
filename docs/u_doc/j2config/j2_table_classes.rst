
Table Classes
============================================

Built-in Table Classes
-----------------------------

list of available tabular classes.

  * Vrf
  * Vlan
  * Bgp
  * Physical
  * Aggregated
  * Loopback
  * Static
  * Ospf


.. note::

  * These classes can be inherited from *nettoolkit.j2config.func* module and modified further as needed.
  * In the excel database create a respective tab ( optional: preferablly same tab name ).
  * Such Tab should have a column name ``filter`` with the value same as class name. ( case insensitive )



--------

Custom Tabular Classes
-----------------------------
 
  * To add new additional custom tabs in to database and use it within jinja, it requires to create a custom class and accordingly it has to be forked in.
  * Excel tab should have a column named ``filter`` with the value same as class name ( case insensitive )
  * class should inherite *nettoolkit.j2config.func.Common* class.

**Create your own class(es)**

  .. code-block:: python

    # file: j2conf_custom_classes.py

    from nettoolkit.j2config.func import Common

    class Rip(Common):

      def vrf_data(self):
        for data in self:
          if data['vrf'] != "":       ## checking, some random column called vrf is not none. 
            yield data

      ## add more methods as you require.


**Create/Append your yaml file referencing custom classes ( if it is structured, provide full path )**

  .. code-block:: yaml

    # file: custom.yaml

    j2_class_filters:
      Rip: !!python/name:j2conf_custom_classes ''


**While configuration generation, fork in custom.yaml**

  .. code-block:: python
    :emphasize-lines: 7,17

    from nettoolkit.nettoolkit_common import read_yaml_mode_us
    from nettoolkit.j2config import PrepareConfig

    ### read custom yaml and custom classes
    custom_yaml_file = 'custom.yaml'
    custom = read_yaml_mode_us(custom_yaml_file)
    custom_classes = {k: v for k, v in custom['j2_class_filters'].items() }
    
    ## create PrepareConfig instance object
    PrCfg = PrepareConfig(
      data_file=data_file,               ### this is your excel data file
      jtemplate_file=template_file,      ### this is your jinja template file
      output_folder=output_folder,       ### location to save output configuration file
    )

    ### Fork in custom classes
    PrCfg.custom_class_add_to_filter(**custom_classes)

    ### Start config gen
    PrCfg.start()

------

Usage of Table Classes
----------------------

  * Classes can be imported as below in to Jinja file and stored under a variable.
  * Which then can be used to filter and retrive data from Excel.
  * Either built-in or forked-in custom classes, both works same way.
  * below example explains about just a Vlan class and its one of usage.

  .. code-block:: jinja
    :emphasize-lines: 2,5

    # a sample code from a jinja file, defining Vlan class as variables.
    {% set Vlan = table | Vlan -%}

    ## Printing vlans and its description ( data will be a row values from excel )
    {% for data in Vlan -%}
    vlan {{ data.int_number }}
     name {{ data.description }}
    !
    {% endfor -%}

