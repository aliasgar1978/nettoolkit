
1. Generate CleanFacts
============================================


Supported for nettoolkit version >= 0.1.0

-----

Use here given process to generate the clean excel facts file from show commands output captured logs.


.. code-block:: python

    # --------------------------------------------
    # IMPORTS
    # --------------------------------------------
    from nettoolkit.facts_finder import CleanFacts, rearrange_tables

    # -------------------------------------------------------------------------------------------------------------
    # Custom Project Imports (Optional/Additional), sample project import mentioned as below. (modify as per own)
    # -------------------------------------------------------------------------------------------------------------
    from custom.custom_factsgen import CustomDeviceFacts     ## CustomDeviceFacts is a class to modify output database as per custom requirement.
    from custom.custom_factsgen import FOREIGN_KEYS          ## FOREIGN_KEYS, define dictionary with additional custom columns require in output databse {tab_name : [column names]} format.

    # --------------------------------------------
    #    INPUT: captures
    # --------------------------------------------
    capture_log_file = "file_with_output_captured.log"		# provide capture file
    capture_xl_file = "parsed_excelfile.xlsx"              # provide parsed excel fact file.


    # --------------------------------------------
    #    Define CleanFact Instance
    # --------------------------------------------
    cleaned_fact = CleanFacts(
        capture_log_file, 
        capture_xl_file,
        convert_to_cit=True,     # (Default: True)  convert normal capture log file to capture_it output format, useful if capture was taken manually
        skip_txtfsm=True,        # (Default: False) skip evaluation of capture_xl_file. use native facts-finder parsers instead.
        new_suffix='-clean',     # (Default: '-clean') ouptut file suffix.
        use_cdp=False,           # (Default: False) use cdp neighbor (overrides lldp neighbor) 
    )
    cleaned_fact()
    clean_file = cleaned_fact.clean_file


#. **CleanFacts Object Properties**

    **CleanFacts** object, possess below properties.

        * **hostname**: hostname of the device discovered from config
        * **config**: raw configuration of device. ( for cisco it will be running config, while for juniper it will be set commands configuration )  
        * **dev_type**: detected device type (either `cisco` or `juniper`) string
        * **clean_file**: new output file name 



.. important::

    **Customize**

    * If you have your own custom classes to modify the output database, than read next page otherwise skip it.
    * **cleaned_fact** instance generated here, has above properties in order to process and customise data further.


.. important::

    **Rearrange**

    * If you want to arrange colums in particular way, than read following pages on rearrange, otherwise skip it.



.. important::
    
    **Required Command Outputs for cisco ios devices**

    * show lldp neighbors
    * show cdp neighbors
    * show interfaces status
    * show interfaces description
    * show running-config
    * show version

    **Required Command Outputs for juniper junos devices**

    * show lldp neighbors
    * show configuration
    * show version
    * show interfaces descriptions
    * show chassis hardware



.. admonition:: Notice

    Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work every where, as expected incase if format differs from expectation. 

    Make sure to cross-check the generated facts before using it.

