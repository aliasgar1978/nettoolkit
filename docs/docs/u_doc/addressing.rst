
A few more addressing functions
============================================

**Before starting, let's assume we already imported nettoolkit as below.**
it will be used than after for each function.

.. code-block:: python
	
	>>> import nettoolkit as nt


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

		>>> nt.bin_mask(24)
		'255.255.255.0'


to_dec_mask()
~~~~~~~~~~~~~~~

	* exactly opposite of above

	.. code-block:: python

		>>> nt.to_dec_mask("255.255.255.0")
		24


bin2dec()
~~~~~~~~~~~~~~~

	* decimal number of mask for provided binary mask input

	.. code-block:: python

		>>> nt.bin2dec('11111111111111111111111111110000')
		4294967280

bin2decmask()
~~~~~~~~~~~~~~~

	* subnet-mask for provided binary mask input

	.. code-block:: python

		>>> nt.bin2decmask('11111111111111111111111111110000')
		28

binsubnet()
~~~~~~~~~~~~~~~

	* binary representation of given subnet

	.. code-block:: python

		>>> nt.binsubnet('10.10.10.0/24')
		'00001010000010100000101000000000'



ns-lookup:
------------------------

Use the ``nslookup()``  to get the dns name programatically.

.. code-block:: python

	>>> nt.nslookup("8.8.8.8")
	'dns.google'


IP.ping:
-----------------

Use the ``IP.ping_average()`` from nettoolkit to get the average responce time (in ms) for given ip.

.. code-block:: python

	>>> nt.IP.ping_average("8.8.8.8")
	289


create IPv4 or IPv6 object dynamically:
-------------------------------------------

	* Creating IPv4 or IPv6 object dynamically is possible via ``addressing()``.  
	* This is useful if we don't know the version about provided subnet.
	* It automatically detects version and returns appropriate object after checking validitiy of input.

Respective operations on returned IPv4 or IPv6 object can be done there after, as mentioned in previous pages.

.. code-block:: python

	# // check below with ipv4 input // #
	>>> ip = nt.addressing("10.10.10.0/24")
	>>> type(ip)
	'nettoolkit.addressing.IPv4'
	>>> ip.version
	4

	# // check below with ipv6 input // #
	>>> ip = nt.addressing("2620:ABCD:1234::/64")
	>>> type(ip)
	'nettoolkit.addressing.IPv6'
	>>> ip.version
	6
