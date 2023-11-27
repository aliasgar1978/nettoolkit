
addressing - module functions
============================================

**import addressing module from nettoolkit as below.**

Functions of addressing will be available to be used than after.

.. code-block:: python
	
	>>> from nettoolkit.addressing import *


addressing functions:
------------------------

There are a few addressing functions which can be used without creating IPv4 or IPv6 Object as mentioned in previous pages.

Such available functions are:
	* bin_mask()
	* to_dec_mask()
	* bin2dec()
	* bin2decmask()
	* binsubnet


bin_mask()
~~~~~~~~~~~~~~~

	* converts and provides binary mask

	.. code-block:: python

		>>> bin_mask(24)
		'255.255.255.0'


to_dec_mask()
~~~~~~~~~~~~~~~

	* exactly opposite of above

	.. code-block:: python

		>>> to_dec_mask("255.255.255.0")
		24


bin2dec()
~~~~~~~~~~~~~~~

	* decimal number of mask for provided binary mask input

	.. code-block:: python

		>>> bin2dec('11111111111111111111111111110000')
		4294967280

bin2decmask()
~~~~~~~~~~~~~~~

	* subnet-mask for provided binary mask input

	.. code-block:: python

		>>> bin2decmask('11111111111111111111111111110000')
		28

binsubnet()
~~~~~~~~~~~~~~~

	* binary representation of given subnet

	.. code-block:: python

		>>> binsubnet('10.10.10.0/24')
		'00001010000010100000101000000000'


-----


ns-lookup
~~~~~~~~~~~~~~~

Use the ``nslookup()``  to get the dns name programatically.

.. code-block:: python

	>>> nslookup("8.8.8.8")
	'dns.google'


IP.ping
~~~~~~~~~~~~~~~

Use the ``IP.ping_average()`` from nettoolkit to get the average responce time (in ms) for given ip.

.. code-block:: python

	>>> IP.ping_average("8.8.8.8")
	289

