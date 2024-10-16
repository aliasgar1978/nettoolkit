
Prefix Operations
============================================



Check prefix
------------------

**Steps Involved:**

    * import the ``isSubset()`` function from ``nettoolkit.addressing`` to verify whether a prefix is part of supernet or not.
    * First argument for the function is - *prefix that need to be match*
    * Second argument for the function is - *supernet within which the prefix needs to be matched*.

    .. code-block:: python
        :emphasize-lines: 5,7

        from nettoolkit.addressing import isSubset
        prefix1 = "10.10.10.0/24"
        prefix2 = "10.10.100.0/24"
        supernet = "10.10.0.0/19"
        isSubset(prefix1, supernet)
        True			# // Here prefix is part of supernet // #
        isSubset(prefix2, supernet)
        False			# // Here prefix is not part of supernet // #

-----

Create Summaries
------------------

**New Latest, efficient, and Fast summaries:**

    * import the ``Aggregate`` from ``nettoolkit.addressing.summary``.
    * Call it with list of prefixes.
    * Object Instance Properties:
        * prefixes: provided prefixes in ordered way.
        * aggregates: Summarized IPv4 objects.
        * summaries: Summarized prefixes (string).

    .. code-block:: python

        from nettoolkit.addressing.summary import Aggregate
        networks = (
            "10.10.0.0/24", "10.10.1.0/24", "10.20.6.0/23", 
            "10.10.2.0/23", "10.20.4.0/23", "10.10.4.0/22"  
        )
        Agg = Aggregate(networks)
        # -- below are sorted input prefixes -- 
        Agg.prefixes
        ['10.10.0.0/24', '10.10.1.0/24', '10.10.2.0/23', '10.10.4.0/22', '10.20.4.0/23', '10.20.6.0/23']
        # -- below is list of aggregate object(s) --
        Agg.aggregates
        [10.10.0.0/21]
        # -- below is list of aggregate strings --
        Agg.summaries
        ['10.10.0.0/21']
        # -- check below  to see type of object in list --
        for agg in Agg.aggregates:
            print(type(agg))

        <class 'nettoolkit.addressing.addressing.IPv4'>
        # -- check below  to see type of object in list --
        for agg in Agg.summaries:
            print(type(agg))
            
        <class 'str'>


create summaries with minimum prefix length
--------------------------------------------

    * import the ``calc_summmaries`` from ``nettoolkit.addressing.summary``.
    * Call it with arguments = **1.**min_subnet_size & **2.**list of prefixes.

    .. code-block:: python

        from nettoolkit.addressing.summary import calc_summmaries
        prefixes = (
            "10.10.0.0/24", "10.10.1.0/24", "10.20.6.0/23", 
            "10.10.2.0/23", "10.20.4.0/23", "10.10.4.0/22"  
        )
        calc_summmaries(min_subnet_size=19, prefixes=prefixes)
        ['10.10.0.0/19']
        ## See here even though summary can be /21, it has summarized to 19. ##




**Deprycated**

    **Steps Involved:**

    * import the ``get_summaries()`` function from ``nettoolkit.addressing`` to summarize provided prefixes.
    * list down all prefixes in an **iterator (list, tuple, set)** that needs to be summarized.
    * execute the ``get_summaries()`` by providing those list of prefixes as arguments. **Kindly note on asterisk sign `*` in argument; if list is directly provided, instead of individual arguments**
    * Function will evaluate all prefixes, generate and return **least possible sumamries** for those prefixes.
    * Incorrect prefix inputs will be excluded.

    .. code-block:: python
        :emphasize-lines: 5

        from nettoolkit.addressing import get_summaries
        networks = (
            "10.10.0.0/24", "10.10.1.0/24", "10.20.6.0/23", 
            "10.10.2.0/23", "10.20.4.0/23", "10.10.4.0/22"  )
        get_summaries(*networks)
        [10.10.0.0/21, 10.20.4.0/22]			# // here is summary created for you // #







-----


Encapsulate subnet
--------------------

    * Use this function to encapsulate the subnet to different sizing.
    * Available only for IPv4 objects for now.
    * available from nettoolkit version **1.4.3** 

    .. code-block:: python
        :emphasize-lines: 3,5

        from nettoolkit.addressing import recapsulate
        s = "10.10.0.5/29"
        recapsulate(s, 27)
        '10.10.0.0/27'
        recapsulate(s, 30)
        '10.10.0.4/30'


-----

Subnet allocations
--------------------

    We can allocate the subnets from given pool dynamically.  Follow below steps.


    1. Import necessary class from addressing module and initialize it.    

    .. code-block:: python

        from nettoolkit.addressing import Allocations
        Alloc = Allocations()
        Alloc.allocation_type = 'comparative'
        Alloc.display_warning = False        # Turn off dispay of warning messages if you want

    allocation_type: options are 

        * **comparative** - prefers first assignment whatever made.
        * **additive** - keeps all assignment type, duplicate assignment will happen
        * **override** - prefers last assignment type

    2. Add Prefix(es) 

        There are many ways we can add the prefix to the allocations. Here are listed two methods.

        2.1. Load from Excel 

        As an example here, lets first load prefixes from an existing excel file; where subnets (row values) are allocated to multiple locations (defined by column header). 
        And than allocating each prefix to Allocation (Alloc) object

        .. code-block:: python

            import pandas as pd
            alloted_summary_df = pd.read_excel("summary_file.xlsx").T.fillna("")
            for place, pfxs in alloted_summary_df.iterrows():
                for pfx in pfxs:
                    if not pfx: continue
                    Alloc.add_prefix(pfx, place)

        2.2. Add an individual prefix manually

        * A few things require for that

            * **base ip** ( from where allocation should start seeking availability ) 
            * **prefix size** to be alloted, along with it's description/usage

        .. code-block:: python

            from nettoolkit.addressing import Subnet_Allocate

            base_ip = "172.16.20.0"
            prefix_size = 24
            description = "Store-User-3rdFloor"

            SA = Subnet_Allocate(f'{base_ip}/{prefix_size}', description)
            SA.verification(Alloc)    # this will verify next available slot and allocate.


    3. And Lastly, allocated prefixes can be retrived from **Alloc.assignment_dict** property.

    .. code-block:: python

        from pprint import pprint
        pprint(Alloc.assignment_dict)
        ## output not displayed here ##


-----


sort list of addresses
-----------------------

    * Use this function to sort the ip addresses in desired order.
    * Available only for IPv4 objects for now.
    * available from nettoolkit version **1.5.0** 
    * use ascending=False for reversed order, Specify list for multiple sort orders
    * Use ``sort_by_size()`` for sorting the prefixes by mask.

    .. code-block:: python
        :emphasize-lines: 18,32,46,60

        from nettoolkit.addressing import sorted_v4_addresses, sort_by_size
        from pprint import pprint
        list_of_ips = [
            "10.10.10.0/25",
            "10.10.2.0/24",
            "10.20.10.0/24",
            "10.10.5.0/24",
            "10.10.10.128/25",
            "10.1.10.0/24",
            "10.10.7.0/24",
            "10.10.1.0/24",
            "100.10.10.0/24",
            "192.168.10.0/24",
            "192.168.1.0/24",
            "172.16.10.0/24",
            "172.16.2.0/24",
        ]
        pprint(sorted_v4_addresses(list_of_ips))
        ['10.1.10.0/24',
        '10.10.1.0/24',
        '10.10.2.0/24',
        '10.10.5.0/24',
        '10.10.7.0/24',
        '10.10.10.0/25',
        '10.10.10.128/25',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.2.0/24',
        '172.16.10.0/24',
        '192.168.1.0/24',
        '192.168.10.0/24']
        pprint(sorted_v4_addresses(list_of_ips, ascending=False))
        ['192.168.10.0/24',
        '192.168.1.0/24',
        '172.16.10.0/24',
        '172.16.2.0/24',
        '100.10.10.0/24',
        '10.20.10.0/24',
        '10.10.10.128/25',
        '10.10.10.0/25',
        '10.10.7.0/24',
        '10.10.5.0/24',
        '10.10.2.0/24',
        '10.10.1.0/24',
        '10.1.10.0/24']
        pprint(sorted_v4_addresses(list_of_ips, ascending=[True,True,False,False,True]))
        ['10.1.10.0/24',
        '10.10.10.128/25',
        '10.10.10.0/25',
        '10.10.7.0/24',
        '10.10.5.0/24',
        '10.10.2.0/24',
        '10.10.1.0/24',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.10.0/24',
        '172.16.2.0/24',
        '192.168.10.0/24',
        '192.168.1.0/24']
        pprint(sort_by_size(list_of_ips))
        ['10.1.10.0/24',
        '10.10.1.0/24',
        '10.10.2.0/24',
        '10.10.5.0/24',
        '10.10.7.0/24',
        '10.20.10.0/24',
        '100.10.10.0/24',
        '172.16.2.0/24',
        '172.16.10.0/24',
        '192.168.1.0/24',
        '192.168.10.0/24',
        '10.10.10.0/25',
        '10.10.10.128/25']



