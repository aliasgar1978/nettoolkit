Filters
============================================

Built-in filters
----------------------

Here is list of filters with some examples available to use within your jinja file.

-----

.. list-table:: Built-in Filters
   :widths: 20 50 15 15
   :align: left
   :header-rows: 1


   * - function
     - Description   
     - inputs
     - output

   * - str_to_list
     - splits input string and returns list of items, split delimiters `,` or `Enter`
     - string
     - list
   * - space_separated
     - joins provided list of items by `spaces`
     - iterable
     - string
   * - comma_separated
     - joins provided list of items by `comma`
     - iterable
     - sting    
   * - list_append
     - append an item to list
     - input1: list, input2: item to append
     - list
   * - list_extend
     - Extend the list of items to list
     - input1 - list, input2 - item to append
     - list
   * - list_sorted
     - provided sorted elements in list
     - list
     - list
   * - convert_to_int
     - convert string format digit-elements to integer type in a list.
     - list
     - list
   * - groups_of_nine
     - breaks down provided list in to multiple groups with max. nine elements in each group
     - list
     - list of lists
   * - physical_if_allowed
     - condition check for `filter==physical` and `vlan in vlan_members`
     - input1 - vlan, input2 - table
     - interface if match found else None
   * - remove_trailing_zeros
     - removes the trailing zeros from given ipv6 address
     - str
     - str
   * - nth_ip
     - get n-th ip address of given network.
     - input1-str(subnet), input2-int(nth ip), input3-bool(withMask, optional)
     - nth ip from subnet
   * - mask
     - get the subnet mask for given network (eg: 24)
     - input - str(subnet)
     - int - subnet mask
   * - netmask
     - get network mask for given network (eg: 255.255.255.0)
     - input - str(subnet)
     - str - netmask
   * - invmask
     - get inverse mask for given network (eg: 0.0.0.255)
     - input - str(subnet)
     - str - inverse mask
   * - addressing
     - get the ip of given subnet
     - input - str(subnet)
     - str - ip part of subnet
   * - int_to_str
     - get the actual physical interface value by removing training sub interfaces.
     - str
     - removes anything trailing starting from "."
   * - v4addressing
     - get the IPv4 objetct for given ip/mask (default mask=32)
     - input1 - str (ip /subnet), input2 - int (mask, optional)
     - nettoolkit.addressing.IPv4 object
   * - get_summaries
     - get the summaries for provided prefixes.
     - list (iterable)
     - list
   * - iprint
     - i print function to be use withing jinja template for debug.
     - Any
     - displays on console
   * - get_item
     - get the nth item from list
     - list
     - int (index)
   * - as_path_repeat
     - as-path repeat function ( joins provided string with given int times separated by spaces )
     - str
     - int


Usage of filters
----------------------

  * Built-in filters can be used within jinja file directly.

  .. code-block:: python
    :emphasize-lines: 4

    # a sample code from a jinja file
    # gives 3rd ip and netmask value from provided ip/subnet 

    ip address {{ ip_address | nth_ip(3) }} {{ ip_address | netmask }}


  .. code-block:: python
    :emphasize-lines: 8,10,12


    # a sample code which splits more than 9 vlans in to multiple lines
    # here data is coming from Physical interfaces tab , and it has column named vlan_members
    # And here we are using multiple filters 
    # First str_to_list - puts vlans in to list,
    # than groups_of_nine - splits it in to sub list containing max 9 members 
    # Below there comma_separated - filter again clubs list of members to string

    {% for vlan_group in data.vlan_members | str_to_list | groups_of_nine -%}
    {% if loop.index == 1 -%}
    switchport trunk allowed vlan {{ vlan_group | comma_separated }}
    {% else -%}
    switchport trunk allowed vlan add {{ vlan_group | comma_separated }}
    {% endif -%}
    {% endfor -%}

