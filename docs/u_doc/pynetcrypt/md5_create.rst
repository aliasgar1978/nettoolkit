
MD5 Generate
============================================


Generate MD5 Hash value for given file.

**Steps Involved:**

	* Import ``get_md5()`` function.
	* Pass filename string argument to the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit.pyNetCrypt import get_md5
		>>> get_md5("c:/users/testuser/desktop/testfile.ext")
		'0df62506324f41584b5643'		## calculated MD5 hash

-----

Generate MD5 Hash value for given string.

**Steps Involved:**

	* Import ``str_hash()`` function.
	* Pass string argument to the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit.pyNetCrypt import str_hash
		>>> str_hash("Some random string")
		'533c8b20aade2aa9a5b31026f865a7a8'	## calculated MD5 hash

