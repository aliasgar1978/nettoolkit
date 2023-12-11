
IPv6 addressing
============================================

IPv6 Object - Overview:
-----------------------------------------

.. admonition:: Overview
    
    It is used to do various ip addressing operations on IPv6 address. 
    
    Activities that can be done are:
        * get various properties of object (such as: mask, NetworkAddress, subnet, network)
        * get details from various methods of object (such as: len(), NetworkIP(), BroadcastIP(), get_hext(), ipdecmask(), n_thIP(), )
        * get the range of ip addresses from provided subnet
        * break the subnet in to smaller pieces
        * glue two adjacent subnets and get summary out of it (if summarizable).

IPv6 Object - Create:
----------------------------------

See below sample on how to create an IPv6 Object, This is mandatory step in order to work on the respective properties or methods.  It will be used in following steps.	

    .. code:: python
    
        >>> from nettoolkit.addrressing import IPv6   # import IPv6
        >>> subnet = "2002:ABCD:1000:256::/64"        # example ipv6 string 
        >>> s = IPv6(subnet)                          # created IPv6 object with provided prefix.

IPv6 object - Properties:
----------------------------------
Available properties: 

    * version
    * bit_length
    * mask, decmask
    * NetworkAddress
    * subnet
    * network

    .. code:: python
    
        >>> s.version
        6
        >>> s.bit_length
        128
        >>> s.mask
        64
        >>> s.decmask
        '64'
        >>> s.NetworkAddress
        '2002:ABCD:1000:256:0:0:0:0'
        >>> s.subnet
        '2002:ABCD:1000:256:0:0:0:0'
        >>> s.network
        '2002:ABCD:1000:256::'
        >>> s
        2002:ABCD:1000:256:0:0:0:0

    

IPv6 object - methods:
----------------------------------
Available methods: 

    * len()
    * NetworkIP() or subnet_zero()
    * BroadcastIP() or broadcast_address()
    * n_thIP()
    * ipdecmask()
    * get_hext() or getHext()

    .. code:: python

        >>> s.len()				# subnet size
        18446744073709551616
        >>> s.subnet_zero()			# network address with mask(default)
        '2002:ABCD:1000:256:0:0:0:0/64'
        >>> s.subnet_zero(withMask=False)	# network address without mask
        '2002:ABCD:1000:256:0:0:0:0'
        >>> s.broadcast_address()		# broadcast address with mask(default)
        '2002:ABCD:1000:256:ffff:ffff:ffff:ffff/64'
        >>> s.broadcast_address(withMask=False)	# broadcast address without mask
        '2002:ABCD:1000:256:ffff:ffff:ffff:ffff'
        >>> s.n_thIP(5)				# 5th IP with mask(default)
        '2002:ABCD:1000:256:0:0:0:5'
        >>> s.n_thIP(5, withMask=False)		# 5th IP without mask
        '2002:ABCD:1000:256:0:0:0:5'
        >>> s.ipdecmask()			# ip with mask
        '2002:ABCD:1000:256:0:0:0:0/64'
        >>> s.get_hext(3)			# a hextate value
        '1000'


IPv6 object - slices:
-------------------------------------
Given IPv6 subnet object can be sliced and portion can be extracted out of it.
see below for example.

    .. code-block:: python
        :emphasize-lines: 8,10

        >>> s[5]		# 5th  ip of subnet
        '2002:ABCD:1000:256:0:0:0:5'
        >>> s[5:8]		# range of ip addresses from subnet
        ('2002:ABCD:1000:256:0:0:0:5', '2002:ABCD:1000:256:0:0:0:6', '2002:ABCD:1000:256:0:0:0:7')
        >>> s + 2		# ++2th ip from provided ip
        '2002:ABCD:1000:256:0:0:0:2'

        >>> s / 4		# break the subnet to 4 equal subnets
        ('2002:ABCD:1000:256:0:0:0:0/66', '2002:ABCD:1000:256:0:0:0:4000000000000000/66', '2002:ABCD:1000:256:0:0:0:8000000000000000/66', '2002:ABCD:1000:256:0:0:0:c000000000000000/66')
        >>> s / 3		# breaks to nearest possible maximum prefix size.
        ('2002:ABCD:1000:256:0:0:0:0/66', '2002:ABCD:1000:256:0:0:0:4000000000000000/66', '2002:ABCD:1000:256:0:0:0:8000000000000000/66', '2002:ABCD:1000:256:0:0:0:c000000000000000/66')

-----


Bonus IPv6
----------


**Identify, Validate & Create - IPv6 object dynamically**

* Creating IPv4 or IPv6 object dynamically is possible via ``addressing()`` function 
* This is useful if we don't know the version about provided subnet.
* It automatically detects version and returns appropriate object after checking validitiy of input.

Respective operations on returned IPv4 / IPv6 object can be done there after, as mentioned above.

.. code-block:: python

    >>> from nettoolkit.addressing import addressing
    >>> ip = addressing("2620:ABCD:1234::/64")
    >>> type(ip)
    <class 'nettoolkit.addressing.addressing.IPv6'>
    >>> ip.version
    6




