
Using CleanFacts [Deprycated]
============================================

.. warning::

	* Deprycated method.  Not supported for nettoolkit version >= 0.1.0
	* Use only if you have standalone facts-finder package installed with nettoolkit version <= 0.0.20 


.. admonition:: steps

	#. Import necessary package, modules
	#. Define your input files ( i.e. capture files )
	#. Generate and evaluate database from device
	#. rearrange database columns of Excel

.. important::

	Use this method, if parsed excel device fact also available along with device commands output captures.
	This will enables more advanced technique to modify for the custom variables later on.


Detailed How To  (CleanFacts)
-----------------------------

	#. Import necessary package, modules

		.. code::

			from facts_finder import CleanFacts, rearrange_tables


	#. Define input files ( i.e. captures-log, facts-excel )

		**parsed_excelfile** can be generated using ``capture_it`` utility.  
		Along with device log capture it can generate the device facts by parsing the outputs concurrently..
		It generates a separate sheet for each parsed command output.

		* `see also: CaptureIT Documentation for more <https://capture_it.readthedocs.io>`_


		.. code::

			capture_log_file = "file_with_output_captured.log"		# provide capture file
			capture_xl_facts = "parsed_excelfile.xlsx"              # provide parsed excel fact file.



	#. Clean Facts

		Evaluating the device capture along with the parsed excel file is called **Cleaning**.
		It will automatically generate a new excel file suffixed with `-clean`. 


		.. code:: python
			
			cf = CleanFacts(
				capture_log_file,      ## Text Capture file
				capture_xl_facts,      ## Excel parsed output file
				new_suffix='-clean',   ## new output file to be suffixed with letters (deault: '-clean')
			)
			cf()


		**cf** *instance variable of an CleanFacts* object, has below properties.

			* **hostname**: hostname of the device discovered from config
			* **config**: raw configuration of device. ( for cisco it will be running config, while for juniper it will be set commands configuration )  
			* **dev_type**: detected device type (either `cisco` or `juniper`) string
			* **clean_file**: new output file name 


		.. Note::

			Incase if you have your own custom classes to modify the output database.
			than execute it here. **cf** instance will provide the necessary attributes in order to process the data further.

			see next page for an example of such.


	#. Rearrange columns in excel file in orders [*optional step*]

		Orders are defined as per `rearrange.py` module of the package.

		.. code:: python
			
			rearrange_tables(cf.clean_file)



.. important::
	
	It is imperative to capture output for atleast below set of commands for **Cisco** Devices. Failing may result in incorrect or missing facts or even error while generating facts. 

	* show lldp neighbors
	* show lldp neighbors detail
	* show cdp neighbors
	* show cdp neighbors detail
	* show interfaces
	* show interfaces switchport
	* show interfaces status
	* show interfaces description
	* show ipv6 interface brief
	* show mac address-table
	* show ip arp
	* show etherchannel summary
	* show ip bgp all summary
	* show ip bgp vpnv4 all neighbors
	* show vrf
	* show ip vrf interfaces
	* show route-map
	* show running-config
	* show version

	command output format should be as follows
		
		! ==========================================

		! output for command: show runn

		! ==========================================
		
		<<output of command>> ...

	* No hostname-prompt requires to be mentioned in command line.

.. important::

	It is imperative to capture output for atleast below set of commands for **Juniper** Devices. Failing may result in incorrect or missing facts or even error while generating facts. 

	* show lldp neighbors
	* show configuration
	* show version
	* show interfaces
	* show interfaces descriptions
	* show chassis hardware
	* show lacp interfaces
	* show arp

	command output format should be as follows

		# ===================================================	
		
		# output for command: show configuration | no-more
		
		# ===================================================			
		
		<<output of command>> ...


	* No hostname-prompt requires to be mentioned in command line.


.. admonition:: Notice

	Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work every where, as expected incase if format differs from expectation. 

	Make sure to cross-check the generated facts before using it.

