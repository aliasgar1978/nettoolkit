
Using DeviceDB [Deprycated]
=====================================================

.. warning::

	* Deprycated method. Soon will be withdrawn.
	* Use `facts_finder` as a parent package instead of `nettoolkit.factsfinder`, if you have standalone facts-finder package installed with nettoolkit version <= 0.0.20 


.. admonition:: steps

	#. Import necessary package, modules
	#. Define your input files ( i.e. capture files )
	#. Generate and evaluate database from device
	#. Write database to Excel

.. important::

	Use this method-1 (using DeviceDB), if only device commands output captures are availalble.
	
	Go for more advanced method-2 (using CleanFacts), if parsed excel device facts are also available along with device commands output captures.


Detailed How To (DeviceDB)
--------------------------

	#. Import necessary package, modules

		.. code::

			from nettoolkit.facts_finder import DeviceDB
			from nettoolkit.facts_finder import device
			from nettoolkit.nettoolkit import write_to_xl


	#. Define your input files ( i.e. captures )

		.. code::

			file = "file_with_output_captured.log"		# provide capture file 

		.. attention::
			
			* It is advisable to capture command output using **capture_it** package. So manual editing can be avoided.
			* Otherwise modify output as mentioned in information below, such that facts_finder can read it.
			* All commands output should be stored in a single file. 


	#. Generate and evaluate database from device

		.. code::

			_model = device(file)		# select the model based on input file
			device_database = DeviceDB()	# create a new device database object
			df_dict = device_database.evaluate(_model)	# evaluate object by providing necessary model, and return dictionary


	#. Write database to Excel

		.. code::
			
			write_to_xl("output_file.xlsx", df_dict, index=True, overwrite=True)	# write output to Excel

		Parameters:
			* **df_dict:** [mandatory] dictionary extracted after evaluation, to write to excel.
			* **index:** [optional] keep or remove index columns
			* **overwrite:** [optional] overwrite or create a new output excel file.



.. important::
	
	Below are the commands requires to be captured from device for **Cisco** Devices.

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

	Below are the commands requires to be captured from device for **Juniper** Devices.

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

	Make a note that output differs between version to version on devices, and thus it is obvious that parsing may not work every where, incase if format differs from expectation. 

	Make sure to cross-check the generated facts before using it.

