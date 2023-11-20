
IPv4 addressing
============================================

Overview
-----------------------------------------

.. admonition:: Overview
	
	It is used to do various ip addressing operations on IPv4 address. 
	
	Activities that can be done are:
		* get various properties of subnet (ie: mask, inverse_mask, binary_mask)
		* get the desired ip from provided subnet (ie: NetworkIP, BroadcastIP, n-th IP)
		* get the ip/subnet in various format (ie: "address/mask", "address subnet_mask", "address inverse_mask")
		* get the range of ip addresses from provided subnet
		* break the subnet in to smaller pieces
		* club two adjacent subnets and get summary out of it (if summarizable).

How to create an IPv4 Object:
----------------------------------

See below sample on how to create an IPv4 Object, This is mandatory step in order to work on the respective properties or methods.  It will be used in following steps.	

	.. code:: python
	
		>>> from nettoolkit.nettoolkit import IPv4		# import IPv4
		>>> subnet = "10.10.10.10/23"		# example ip string 
		>>> s = IPv4(subnet)			# created IPv4 object with provided prefix.

Properties of IPv4 object:
----------------------------------
Available properties: 

	* version
	* bit_length
	* mask
	* decmask or decimalMask
	* binmask
	* invmask 

	.. code:: python
	
		>>> s.version
		4
		>>> s.bit_length
		32
		>>> s.mask 	# decimal mask
		23
		>>> s.decmask 	# decimal mask
		23
		>>> s.binmask 	# binary mask
		'255.255.254.0'
		>>> s.invmask 	# inverse mask
		'0.0.1.255'
		>>> s 		# provided ip/mask string format
		10.10.10.10/23		

	

Get an IP:
----------------------------------
Available methods: 

	* NetworkIP() or subnet_zero()
	* BroadcastIP() or broadcast_address()
	* n_thIP()

	.. code:: python
	
		>>> s.subnet_zero()			# network ip, with default=with mask
		'10.10.10.0/23'
		>>> s.subnet_zero(withMask=False)	# network ip, without mask
		'10.10.10.0'
		>>> s.broadcast_address()		# broadcast ip, with default=without mask
		'10.10.11.255'
		>>> s.broadcast_address(withMask=True)	# broadcast ip, with mask
		'10.10.11.255/23'
		>>> s.n_thIP(5)				# 5th ip of subnet, with default=without mask
		'10.10.10.5'
		>>> s.n_thIP(5, withMask=True)		# 5th ip of subnet, with mask
		'10.10.10.5/23'


Get ip with mask in various formats:
-------------------------------------
Available methods: 

	* ipbinmask()
	* ipdecmask()
	* ipinvmask()

	.. code:: python

		>>> s.ipbinmask()			# subnet with binary mask
		'10.10.10.0 255.255.254.0'
		>>> s.ipbinmask(n=4)		# an ip with binary mask
		'10.10.10.4 255.255.254.0'
		>>> s.ipdecmask()			# subnet with decimal mask
		'10.10.10.0/23'
		>>> s.ipdecmask(n=4)		# an ip with decimal mask
		'10.10.10.4/23'
		>>> s.ipinvmask()			# subnet with inverse mask
		'10.10.10.0 0.0.1.255'
		>>> s.ipinvmask(n=4)		# an ip with inverse mask
		'10.10.10.4 0.0.1.255'



Get IPv4 Object slices:
-------------------------------------
Given IPv4 subnet object can be sliced and portion can be extracted out of it.
see below for example.

	.. code-block:: python
		:emphasize-lines: 8,10,12

		>>> s[5]		# 5th  ip of subnet
		'10.10.10.5'
		>>> s+5			# ++5th ip from provided ip
		'10.10.10.15'
		>>> s-3			# --3rd ip from provided ip
		'10.10.10.7'

		>>> s[0:5]		# range of ip addresses from subnet
		('10.10.10.0', '10.10.10.1', '10.10.10.2', '10.10.10.3', '10.10.10.4')

		>>> s/4			# break the subnet to 4 equal subnets
		('10.10.10.0/25', '10.10.10.128/25', '10.10.11.0/25', '10.10.11.128/25')
		>>> s/3			# breaks to nearest possible maximum prefix size.
		('10.10.10.0/25', '10.10.10.128/25', '10.10.11.0/25', '10.10.11.128/25')

IPv4 Object addition:
----------------------
Add the two IPv4 Objects to get the summary out of it (if summarizable)
see below for example.

	.. code-block:: python
		:emphasize-lines: 8

		# provided two subnet and created object of it.
		>>> subnet1 = "10.10.10.0/23"	
		>>> subnet2 = "10.10.8.0/23"
		>>> s1 = IPv4(subnet1)
		>>> s2 = IPv4(subnet2)

		# get summary of two subnets
		>>> s1 + s2
		10.10.8.0/22
		
		# notice, return type is IPv4 not a string
		>>> type(s1 + s2)		
		'nettoolkit.addressing.IPv4'


Beware: Non-contiguous or unsummarizable subnets cannot be clubbed this way.

	.. code-block:: python
		:emphasize-lines: 5

		>>> subnet1 = "10.10.10.0/23"
		>>> subnet2 = "10.10.12.0/23"
		>>> s1 = IPv4(subnet1)
		>>> s2 = IPv4(subnet2)
		>>> s1 + s2
		Traceback (most recent call last):
		  File "<pyshell#147>", line 1, in <module>
		    s1 + s2
		  File "C:\...\addressing.py", line 412, in __add__
		    "Inconsistant subnets cannot be added "
		Exception: Inconsistant subnets cannot be added and >2 instances of IPv4/IPv6 Object add not allowed. please check inputs or Use 'get_summaries' function instead




