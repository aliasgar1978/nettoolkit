
Prefix Operations
============================================

Activities that can be done are:
	* Check that provided prefix is part of another prefix (supernet). 
	* Create Summaries out of provided prefixes.

Check prefix
------------------

**Steps Involved:**

	* import the ``isSubset()`` function from ``nettoolkit.addressing`` to verify whether a prefix is part of supernet or not.
	* First argument for the function is - *prefix that need to be match*
	* Second argument for the function is - *supernet within which the prefix needs to be matched*.

	.. code-block:: python
		:emphasize-lines: 5,7

		>>> from nettoolkit.addressing import isSubset
		>>> prefix1 = "10.10.10.0/24"
		>>> prefix2 = "10.10.100.0/24"
		>>> supernet = "10.10.0.0/19"
		>>> isSubset(prefix1, supernet)
		True			# // Here prefix is part of supernet // #
		>>> isSubset(prefix2, supernet)
		False			# // Here prefix is not part of supernet // #



Create Summaries
------------------

**Steps Involved:**

	* import the ``get_summaries()`` function from ``nettoolkit.addressing`` to summarize provided prefixes.
	* list down all prefixes in an **iterator (list, tuple, set)** that needs to be summarized.
	* execute the ``get_summaries()`` by providing those list of prefixes as arguments. **Kindly note on asterisk sign `*` in argument; if list is directly provided, instead of individual arguments**
	* Function will evaluate all prefixes, generate and return **least possible sumamries** for those prefixes.
	* Incorrect prefix inputs will be excluded.

	.. code-block:: python
		:emphasize-lines: 5

		>>> from nettoolkit.addressing import get_summaries
		>>> networks = (
			"10.10.0.0/24", "10.10.1.0/24", "10.20.6.0/23", 
			"10.10.2.0/23", "10.20.4.0/23", "10.10.4.0/22"  )
		>>> get_summaries(*networks)
		[10.10.0.0/21, 10.20.4.0/22]			# // here is summary created for you // #


Encapsulate subnet
--------------------

  * Use this function to encapsulate the subnet to different sizing.
  * Available only for IPv4 objects for now.
  * available from nettoolkit version **1.4.3** 


	.. code-block:: python
		:emphasize-lines: 3,5

		>>> from nettoolkit.addressing import recapsulate
		s = "10.10.0.5/29"
		>>> recapsulate(s, 27)
		'10.10.0.0/27'
		>>> recapsulate(s, 30)
		'10.10.0.4/30'

