
Yaml Facts Generation
============================================

* Use below given sample code/process to generate yaml facts file.
* Configuration capture is required for standard show outputs


.. code-block:: python

    # -------------------------------------------------------------------------------------------------------------
    # Imports
    # -------------------------------------------------------------------------------------------------------------
    from nettoolkit.yaml_facts import YamlFacts

    # -------------------------------------------------------------------------------------------------------------
    # select the configuration capture log file..
    # -------------------------------------------------------------------------------------------------------------
    capture_log_file = 'c:/users/xxxxx/Documents/device_capture.log'
    output_folder = 'c:/users/xxxxx/Documents'

    # -------------------------------------------------------------------------------------------------------------
    # Provide above inputs to YamlFacts class.
    # -------------------------------------------------------------------------------------------------------------
    FR = YamlFacts(
        capture_log_file=capture_log_file,
        output_folder=output_folder
    )



**YamlFacts Object Properties**

    **YamlFacts** object, possess below properties.

        * **capture_log_file**: show commands output capture log file.
        * **output_folder**: output folder where yaml output to be stored.

.. important::
    
    **Required Command Outputs for cisco ios devices**

    * show lldp neighbors
    * show cdp neighbors
    * show interfaces status
    * show interfaces description (optional)
    * show running-config
    * show version

    **Required Command Outputs for juniper junos devices**

    * show lldp neighbors
    * show configuration
    * show version
    * show interfaces descriptions (optional)
    * show chassis hardware

.. admonition:: Notice

    Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work 100% accurate every where as expected, if format differs from expected output. 

    Make sure to cross-check the generated yaml_facts before using it.
