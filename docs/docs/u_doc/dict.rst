
A few additional Dictionary operations
======================================



Dictionary functions:
------------------------

**Before starting, let's assume we already imported nettoolkit as below.**
it will be used than after for each function.

.. code-block:: python
	
	>>> from nettoolkit import DIC


There are many dictionary methods available under ``DIC`` class in ``nettoolkit``.

Such available functions are:

	* merge_dict()
	* recursive_dic()

merge_dict()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	* Merges two dictionaries for identical keys 
	* with deep inspection

	.. code-block:: python

		>>> d1 = {"interfaces": {"FA1": {"description":"description of FA1"},
				     "FA2": {"description":"description of FA2"},
				     "FA3": {"description":"description of FA3"},}}
		>>> d2 = {"interfaces": {"FA1": {"ip":"ip of FA1"},
				     "FA2": {"ip":"ip of FA2"},
				     "FA3": {"ip":"ip of FA3"},}}

		>>> DIC.merge_dict(d1, d2)
		{'interfaces': {'FA1': {'description': 'description of FA1', 
		                        'ip': 'ip of FA1'},
		                'FA2': {'description': 'description of FA2', 
		                        'ip': 'ip of FA2'},
		                'FA3': {'description': 'description of FA3',
		                        'ip': 'ip of FA3'}}}




recursive_dic()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	* convert dictionary (dic) to string. 
	* recursive dictionary increases indention
	* second argument is number of characters for indention

	.. code-block:: python

		>>> d = {'interfaces': {'FA1': {'description': 'description of FA1', 
				                        'ip': 'ip of FA1'},
				                'FA2': {'description': 'description of FA2', 
				                        'ip': 'ip of FA2'},
				                'FA3': {'description': 'description of FA3',
				                        'ip': 'ip of FA3'}}}

		>>> print(DIC.recursive_dic(d, 4))
		    interfaces
		     FA1
		      description
		         description of FA1
		      ip
		         ip of FA1
		     FA2
		      description
		         description of FA2
		      ip
		         ip of FA2
		     FA3
		      description
		         description of FA3
		      ip
		         ip of FA3


For More Details check out the API docuementation for DIC class.

	* `DIC <https://nettoolkit.readthedocs.io/en/latest/docs/t_doc/__gpl.html#nettoolkit.gpl.DIC>`_


Dictionary Differences:
------------------------

	* This is a class which classify difference between two dictionary objects.
	* use +/- for checking adds/removes


	.. code-block:: python

		# Step 1.  Import necessary class
		>>> from nettoolkit import DifferenceDict

		# Step 2.  provide the two dictionaries to be compare, say pre and post activitites.
		>>> pre = {
			"FA1": {
				'vlans': {11,12, 13},
				'mode': 'trunk',
				'ip': '1.1.1.1/24',
			},
			"FA2": {
				'vlans': {21, 22, 23},
				'mode': 'trunk',
				'ip': '2.2.2.2/24',
			},
			"FA3": {
				'vlans': {31, 32, 33},
				'mode': 'access',
				'ip': '3.3.3.3/24',
			},
		}

		>>> post = {
			"FA1": {
				'vlans': {11,12, 13},
				'mode': 'trunk',
				'ip': '1.121.1.121/24',
			},
			"FA2": {
				'vlans': {21, 22, 25},
				'mode': 'trunk',
				'ip': '2.2.2.2/24',
			},
			"FA3": {
				'status': 'admin down',
				'mode': 'access',
				'ip': '3.3.3.3/24',
			},
			"FA4": {
				'status': 'up',
				'mode': 'new born',
			},
			
		}

		# Step 3. Create necessary objects out of dictionary
		>>> predd = DifferenceDict(pre)
		>>> postdd = DifferenceDict(post)

		# Step 4. Get the differences
		>>> predd - postdd				# removals from pre
		{'FA1': {'ip': '- 1.1.1.1/24'}, 'FA2': {'vlans': {'- 23'}}, 'FA3': {'- vlans': {'- 32', '- 33', '- 31'}}}
		>>> postdd + predd				# adds to post
		{'FA1': {'ip': '+ 1.121.1.121/24'}, 'FA2': {'vlans': {'+ 25'}}, 'FA3': {'+ status': '+ admin down'}, '+ FA4': {'+ status': '+ up', '+ mode': '+ new born'}}

		# Extra Steps:: convert dictionary to string to see hierachical data
		>>> deltadd = postdd + predd
		>>> print(DIC.recursive_dic(deltadd))
		FA1
		 ip
		    + 1.121.1.121/24
		FA2
		 vlans
		+ 25
		FA3
		 + status
		    + admin down
		+ FA4
		 + status
		    + up
		 + mode
		    + new born

		>>> deltaremoves = predd - postdd
		>>> print(DIC.recursive_dic(deltaremoves))
		FA1
		 ip
		    - 1.1.1.1/24
		FA2
		 vlans
		- 23
		FA3
		 - vlans
		- 32
		- 33
		- 31

