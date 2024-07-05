
MD5 Generate
============================================

Generate MD5 Hash value for given file.

-----

**Steps Involved:**

	* Import ``get_md5()`` function from ``nettoolkit``.
	* Pass filename string argument to the function

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit.pyNetCrypt import get_md5
		>>> get_md5("c:/users/testuser/desktop/testfile.ext")
		'0df62506324f41584b5643'		## calculated MD5 hash

