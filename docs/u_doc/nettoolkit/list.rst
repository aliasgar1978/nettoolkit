
A few additional List operations
======================================

**Before starting, let's assume we already imported nettoolkit as below.**
it will be used than after for each function.

.. code-block:: python
	
	>>> from nettoolkit.nettoolkit import LST


List functions:
------------------------

There are many list methods available under ``LST`` class in ``nettoolkit``.

Such available functions are:

	* remove_empty_members()
	* expand_vlan_list()
	* convert_vlans_list_to_range_of_vlans_list()
	* list_variants()
	* list_of_devices()
	* split()
	* list_to_octet()

remove_empty_members()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	* This is a kind of house keeping of list, it removes empty members from list.

	.. code-block:: python

		>>> l = ['this', '', 'is', '', 'a', '', 'test', '', 'list']
		>>> LST.remove_empty_members(l)
		['this', 'is', 'a', 'test', 'list']


expand_vlan_list()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	* Expands Vlan list from given ranges.  (if any within). And returns new set of vlans with all individal vlan numbers.

	.. code-block:: python

		>>> vlan_list = [ '10-14', 17, '25-30' ]
		>>> LST.expand_vlan_list(vlan_list)
		{10, 11, 12, 13, 14, 17, 25, 26, 27, 28, 29, 30}


convert_vlans_list_to_range_of_vlans_list()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	* Compress list of vlans to a possible range of vlans. i.e. Reverse action of above.

	.. code-block:: python

		>>> vlans = [501,502,503,504,505,490,491,492,300,493,299]
		>>> LST.convert_vlans_list_to_range_of_vlans_list(vlans)
		['299-300', '490-493', '501-505']


list_variants()
~~~~~~~~~~~~~~~

	* list of vlans in different format
		* list of vlans, (str_list)
		* space separated string, (ssv_list)
		* comma separated string, (csv_list)

	.. code-block:: python


		>>> vlans = [501,502,503,504,505,490,491,492,300,493,299]
		>>> LST.list_variants(vlans)
		{'str_list': ['299-300', '490-493', '501-505'], 
		 'ssv_list': '299-300 490-493 501-505', 
		 'csv_list': '299-300,490-493,501-505'}

list_of_devices()
~~~~~~~~~~~~~~~~~~

	* get hostnames (first index item) from list of files.

	.. code-block:: python

		>>> filenames = ["/usr/abc/hostname1.log", "c:/path2/hostname2.log", "somewhere/hostname3.log"]
		>>> LST.list_of_devices(filenames)
		{'hostname3', 'hostname1', 'hostname2'}

split()
~~~~~~~~~~~~~~~

	* yield provided list with group of n number of items

	.. code-block:: python

		>>> lst = [1,2,3,4,5,6,7,8,9,10]
		>>> for x in LST.split(lst, 3):
			print(x)

		(1, 2, 3)
		(4, 5, 6)
		(7, 8, 9)
		(10,)
		>>> for x in LST.split(lst, 4):
			print(x)
			
		(1, 2, 3, 4)
		(5, 6, 7, 8)
		(9, 10)



list_to_octet()
~~~~~~~~~~~~~~~~

	* joins and return string with provided list with '.'
	* helpful in creating ipv4 string with list of 4 numeric items

	.. code-block:: python

		>>> lst = [192, 168, 1, 1]
		>>> LST.list_to_octet(lst)
		'192.168.1.1'


