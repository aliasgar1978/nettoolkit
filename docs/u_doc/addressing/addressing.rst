
addressing - module functions
============================================

**import addressing module from nettoolkit as below.**

Functions of addressing will be available to be used than after.

.. code-block:: python
	
	>>> from nettoolkit.addressing import *


* There are few addressing functions - which can be used without creating IPv4 or IPv6 Object. These are  desscribed as below.


-----



bin_mask()
------------------------
	* converts and provides binary mask

	.. code-block:: python

		>>> bin_mask(24)
		'255.255.255.0'


to_dec_mask()
------------------------

	* exactly opposite of above

	.. code-block:: python

		>>> to_dec_mask("255.255.255.0")
		24


bin2dec()
------------------------

	* decimal number of mask for provided binary mask input

	.. code-block:: python

		>>> bin2dec('11111111111111111111111111110000')
		4294967280

bin2decmask()
------------------------

	* subnet-mask for provided binary mask input

	.. code-block:: python

		>>> bin2decmask('11111111111111111111111111110000')
		28

binsubnet()
------------------------

	* binary representation of given subnet

	.. code-block:: python

		>>> binsubnet('10.10.10.0/24')
		'00001010000010100000101000000000'

dec2dotted_ip
-------------

	* converts decimal ip address to dotted decimal ip notation

	.. code-block:: python

		>>> n = 183490304
		>>> dec2dotted_ip(n)
		'10.239.215.0'


subnet_size_to_mask
-------------------

	* converts subnet size to get subnet mask value

	.. code-block:: python

		>>> subnet_size_to_mask(256)
		24
		>>> subnet_size_to_mask(512)
		23

inv_subnet_size_to_mask
-----------------------

	* converts inverse subnet to get subnet mask value

	.. code-block:: python

		>>> inv_subnet_size_to_mask(255)
		24
		>>> inv_subnet_size_to_mask(511)
		23

get_subnet
----------

	* get subnet/mask from decimal network ip and size of subnet (unvalidated)

	.. code-block:: python

		>>> get_subnet(183490304, 256)
		'10.239.215.0/24'
		>>> get_subnet(183490304, 512)
		Invalid subnet/mask cannot return 10.239.215.0/23
		''

ipv4_octets
-----------

	* get octets in a list for provided ip/subnet

	.. code-block:: python

		>>> ipv4_octets("10.11.12.0/24")
		{'octets': ['10', '11', '12', '0'], 'mask': 24}



range_subset
------------

	* check whether range1 is a subset of range2

	.. code-block:: python

		>>> range_subset(range(0,50), range(0,100))
		True
		>>> range_subset(range(0,120), range(0,100))
		False



-----


ns-lookup
------------------------

	* Use the ``nslookup()``  to get the dns name programatically.

	.. code-block:: python

		>>> nslookup("8.8.8.8")
		'dns.google'


IP.ping
------------------------

	* Use the ``IP.ping_average()`` from nettoolkit to get the average responce time (in ms) for given ip.

	.. code-block:: python

		>>> IP.ping_average("8.8.8.8")
		289

