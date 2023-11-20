
A few additional String operations
======================================

**Before starting, let's assume we already imported nettoolkit as below.**
it will be used than after for each function.

.. code-block:: python
	
	>>> from nettoolkit.nettoolkit import STR


string functions:
------------------------

There are many string methods available under ``STR`` class in ``nettoolkit``.

Such available functions are:
	* found(), foundPos()
	* find_within(), string_within(), suffix_index_within()
	* find_all(), find_any(), find_multi()
	* update()
	* replace_dual_and_split(), finddualnreplacesingle()
	* indention()
	* is_blank_line()
	* is_hostname_line(), hostname(), hostname_from_cli()
	* shrink_if(), if_prefix()
	* string_concate()
	* right(), mid()
	* delete_trailing_remarks()
	* to_list(), to_set()
	* prepend_bgp_as()


found()
~~~~~~~~~~~~~~~

	* Checks sub-string withing a string and provides True/False based on finding.
	* This is python native str.find() alternative, to use in conditions. b/c native function returns -1 if not found, which becomes True in codition check if not matched exclusively with -1.

	.. code-block:: python

		>>> STR.found("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "A")
		True


foundPos()
~~~~~~~~~~~~~~~

	* Checks sub-string withing a string and returns position index based on finding.
	* This is exactly as native str.find()

	.. code-block:: python

		>>> STR.foundPos("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "A")
		31



find_within()
~~~~~~~~~~~~~~~

	* Finds characters between prefix and suffix substrings from string
	* returns a tuple with ( match string, index )

	.. code-block:: python

		>>> STR.find_within("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "BROWN", "OVER")
		(' FOX JUMP ', 25)	


string_within()
~~~~~~~~~~~~~~~

	* Finds characters between prefix and suffix substrings from string
	* returns only match string

	.. code-block:: python

		>>> STR.string_within("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "BROWN", "OVER")
		' FOX JUMP '

suffix_index_within()
~~~~~~~~~~~~~~~~~~~~~~

	* Finds characters between prefix and suffix substrings from string 
	* returns only match string start index

	.. code-block:: python

		>>> STR.suffix_index_within("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "BROWN", "OVER")
		25

find_all()
~~~~~~~~~~~~

	* Search for multiple substrings (list, tuple, set) within string.
	* all sub-strings should be found in order to return True.
	* additional arguments that can be added are:
		* start = Optional: integer - position/index to start search from
		* count = Optional: integer - count of characters to seach from start index

	.. code-block:: python

		>>> f1 = ("LAZY", "BROWN", "QUICK")
		>>> f2 = ("LAZY", "RED", "QUICK")
		>>> STR.find_all("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f1)
		True
		>>> STR.find_all("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f2)
		False

find_any()
~~~~~~~~~~~~

	* Search for multiple substrings (list, tuple, set) within string.
	* any sub-strings should be found in order to return True.
	* additional arguments that can be added are:
		* start = Optional: integer - position/index to start search from
		* count = Optional: integer - count of characters to seach from start index

	.. code-block:: python

		>>> f1 = ("LAZY", "BROWN", "QUICK")
		>>> f2 = ("LAZY", "RED", "QUICK")
		>>> STR.find_any("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f1)
		True
		>>> STR.find_any("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f2)
		True

find_multi()
~~~~~~~~~~~~~

	* Search for multiple substrings (list, tuple, set) within string.
	* returns Either boolean for each sub-str match or the index values.
	* additional arguments that can be added are:
		* start = Optional: integer - position/index to start search from
		* count = Optional: integer - count of characters to seach from start index
		* index = Optional: Bool - False to get boolean instead of indexes, (default: True)

	.. code-block:: python

		>>> f1 = ("LAZY", "BROWN", "QUICK")
		>>> f2 = ("LAZY", "RED", "QUICK")
		>>> STR.find_multi("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f1)
		[30, 10, 4]
		>>> STR.find_multi("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f2)
		[30, -1, 4]
		>>> STR.find_multi("THE QUICK BROWN FOX JUMP OVER LAZY DOG", f2, index=False)
		[True, False, True]

update()
~~~~~~~~~

	* Updates string for search item with replace item 
	* This is same as native str.replace()

	.. code-block:: python

		>>> STR.update("THE QUICK BROWN FOX JUMP OVER LAZY DOG", "DOG", "GOAT")
		'THE QUICK BROWN FOX JUMP OVER LAZY GOAT'
		
replace_dual_and_split()
~~~~~~~~~~~~~~~~~~~~~~~~~~

	* Finds subsequent characters in string and replace those with single. And splits the string using provided Find character (duo). 

	.. code-block:: python

		>>> s = "SRNO____ITEM_____DESCRIPTION________QTY______AMOUNT"
		>>> STR.replace_dual_and_split(s, " ")
		['SRNO', 'ITEM', 'DESCRIPTION', 'QTY', 'AMOUNT']


finddualnreplacesingle()
~~~~~~~~~~~~~~~~~~~~~~~~~

	* Finds subsequent characters in string and replace those with single.

	.. code-block:: python

		>>> s = "SRNO____ITEM_____DESCRIPTION________QTY______AMOUNT"
		>>> STR.finddualnreplacesingle(s, "_")
		'SRNO_ITEM_DESCRIPTION_QTY_AMOUNT'

indention()
~~~~~~~~~~~~
	
	* get string indention value

	.. code-block:: python

		>>> s = "    this is indented line"
		>>> STR.indention(s)
		4		# there are four spaces there as indention


is_blank_line()
~~~~~~~~~~~~~~~~~
	
	* provided string/line a blank line or not

	.. code-block:: python

		>>> s = "      \n"
		>>> STR.is_blank_line(s)
		True

is_hostname_line()
~~~~~~~~~~~~~~~~~~~~

	* string/line containing hostname of device

	.. code-block:: python

		>>> line = "somehostname> show ip int brie"
		>>> STR.is_hostname_line(line, "somehostname")
		True

hostname()
~~~~~~~~~~

	* returns hostname of device from paramiko netconnection

	.. code-block:: python

		>>> STR.hostname(net_connect)	# where net_connect is active paramiko netconnection
		//hostname//



hostname_from_cli()
~~~~~~~~~~~~~~~~~~~

	* input standard text input line, for which command was entered.
	* hostname from command line

	.. code-block:: python

		>>> cmd = "sh int status"
		>>> line = "somehostname> sh int status"
		>>> STR.hostname_from_cli(line, cmd)
		'somehostname'


shrink_if()
~~~~~~~~~~~~

	* Interface Name shortening, input length will decide number of charactes to be included in shortened output

	.. code-block:: python

		>>> STR.shrink_if("FastEthernet0/1", 2)
		'Fa0/1'


if_prefix()
~~~~~~~~~~~

	* Interface type or beginning prefix

	.. code-block:: python

		>>> STR.if_prefix("FastEthernet0/1")
		'FastEthernet'

string_concate()
~~~~~~~~~~~~~~~~
	
	* Concatenate strings s and s1 with conjuctor conj 

	.. code-block:: python

		>>> s1 = "this is beginning"
		>>> s2 = "this is end"
		>>> conj = " <-> "
		>>> STR.string_concate(s1, s2, conj)
		'this is beginning <-> this is end'

right()
~~~~~~~

	* N-number of characters from right side of string

	.. code-block:: python

		>>> s = "THE QUICK BROWN FOX JUMP OVER LAZY DOG"
		>>> STR.right(s, 10)
		'R LAZY DOG'


mid()
~~~~~
	
	* N-number of characters from given position in string
	* Default n-characters is till end 

	.. code-block:: python

		>>> s = "THE QUICK BROWN FOX JUMP OVER LAZY DOG"
		>>> STR.mid(s, 11, 5)
		'BROWN'
	

delete_trailing_remarks()
~~~~~~~~~~~~~~~~~~~~~~~~~~

	* Deletes trailing remarks from Juniper config line/string

	.. code-block:: python

		>>> s = '  root-authentication encrypted-password "$9$xxxxxxxx";  ## encrypted-pass'
		>>> STR.delete_trailing_remarks(s)
		'  root-authentication encrypted-password "$9$xxxxxxxx";'

to_list()
~~~~~~~~~

	* Returns list for the provided string - s
	* split by Carriage Return

	.. code-block:: python

		>>> multiline_str = """This is line 1
		this one is 2nd
		this is 3rd
		and so on"""
		>>> STR.to_list(multiline_str)
		['This is line 1\n', 'this one is 2nd\n', 'this is 3rd\n', 'and so on\n']



to_set()
~~~~~~~~~~

	* Returns set for the provided string - s
	* split by Carriage Return and Commas

	.. code-block:: python

		>>> list_of_ips = """1.1.1.1
		2.2.2.2,3.3.3.3
		4.4.4.4"""
		>>> 
		>>> STR.to_set(list_of_ips)
		{'1.1.1.1', '3.3.3.3', '2.2.2.2', '4.4.4.4'}
	

prepend_bgp_as()
~~~~~~~~~~~~~~~~~~

	* ‘n’ number of BGP AS Number prepending string

	.. code-block:: python

		>>> STR.prepend_bgp_as("12345", 10)
		'12345 12345 12345 12345 12345 12345 12345 12345 12345 12345'


