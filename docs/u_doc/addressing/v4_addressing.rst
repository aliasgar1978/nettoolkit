
IPv4 addressing
============================================

IPv4 Object - Overview:
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

IPv4 Object - Create:
----------------------------------

See below sample on how to create an IPv4 Object, This is mandatory step in order to work on the respective properties or methods.  
It will be used in following steps.	

    .. code-block:: python
    
        >>> from nettoolkit.addressing import IPv4   # import IPv4
        >>> subnet = "10.10.10.10/23"                # example ip string 
        >>> s = IPv4(subnet)                         # created IPv4 object with provided prefix.

IPv4 object - Properties:
----------------------------------

    version

        .. code-block:: python

            >>> s.version
            4
    
    bit_length

        .. code-block:: python

            >>> s.bit_length
            32

    subnet, net, mask

        .. code-block:: python

            >>> s.subnet
            '10.10.10.10/23'
            >>> s.net
            '10.10.10.10'
            >>> s.mask 	# decimal mask
            23


    decmask or decimalMask

        .. code-block:: python

            >>> s.decmask 	# decimal mask
            23


    binmask

        .. code-block:: python

            >>> s.binmask 	# binary mask
            '255.255.254.0'

    invmask

        .. code-block:: python

            >>> s.invmask 	# inverse mask
            '0.0.1.255'


    ip_number

        .. code-block:: python

            >>> s.ip_number
            10

    

IPv4 object - methods:
----------------------------------

    NetworkIP() or subnet_zero()

        .. code-block:: python

            >>> s.subnet_zero()
            '10.10.10.0/23'
            >>> s.subnet_zero(withMask=False)
            '10.10.10.0'

    BroadcastIP() or broadcast_address()

        .. code-block:: python

            >>> s.broadcast_address()
            '10.10.11.255'
            >>> s.broadcast_address(withMask=True)
            '10.10.11.255/23'


    n_thIP()

        .. code-block:: python

            >>> s.n_thIP(5)
            '10.10.10.5'
            >>> s.n_thIP(5, withMask=True)
            '10.10.10.5/23'


    expand()
    
        .. code-block:: python

            >>> s.expand(22)
            '10.10.8.0/22'

    ipbinmask(), ipdecmask(), ipinvmask()

        .. code-block:: python
    
            >>> s.ipbinmask()
            '10.10.10.0 255.255.254.0'
            >>> s.ipbinmask(5)
            '10.10.10.5 255.255.254.0'
            >>> s.ipdecmask()
            '10.10.10.0/23'
            >>> s.ipdecmask(5)
            '10.10.10.5/23'
            >>> s.ipinvmask()
            '10.10.10.0 0.0.1.255'
            >>> s.ipinvmask(5)
            '10.10.10.5 0.0.1.255'



IPv4 Object - slices:
-------------------------------------

IPv4 object can be sliced and portion can be extracted out of it.

    .. code-block:: python
        :emphasize-lines: 1,3,5,8,10,12

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


IPv4 Object - addition:
-----------------------

Two adjacent IPv4 Objects can be clubbed together to get the summary out of it (if summarizable)

    .. code-block:: python
        :emphasize-lines: 8,12

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


*Non-contiguous*, *un-summarizable*, *greater than 2* - subnets **cannot club** this way.  Refer *Create Summaries* section on *Prefix Operation* page for more.

    .. code-block:: python
        :emphasize-lines: 10,11

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



-----

Bonus IPV4
----------

**Identify, Validate & Create - IPv4 object dynamically**

* Creating IPv4 or IPv6 object dynamically is possible via ``addressing()`` function
* This is useful if we don't know the version about provided subnet.
* It automatically detects version and returns appropriate object after checking validitiy of input.

Respective operations on returned IPv4 / IPv6 object can be done there after, as mentioned above.

    .. code-block:: python

        >>> from nettoolkit.addressing import addressing
        ip = addressing("10.10.10.0/24")
        >>> type(ip)
        <class 'nettoolkit.addressing.addressing.IPv4'>
        >>> ip.version
        4