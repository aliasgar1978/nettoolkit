
A few Other uncategorized mixed functions
==========================================


@decorator: **printmsg**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * Use it as decorator to print some messages before and after a function call.
    * keys to decorator
        #. pre: (default: None) - message to be printed before function call( default min message length = 80 )
        #. post: (default: None) - message to be printed after function call
        #. pre_ends: (default: \n) - default message end character after pre message finish.

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import printmsg
        >>> @printmsg(pre="Some Pre Message" ,pre_ends="\t", post="Some Post Message")
        def SomeFunction():
            print("Function Message")
        
        >>> SomeFunction()
        Some Pre Message                                                                	Function Message
        Some Post Message

remove_domain()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * removes domain entry from fqdn entry

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import remove_domain
        >>> remove_domain("hostname.domain.com")
        "hostname"


read_file()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * reads the provided text file and retuns output in list format

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import read_file
        >>> read_file("sometextfile.txt")
        ['list of lines from text file',...]


standardize_mac()
~~~~~~~~~~~~~~~~~~

    * removes . or : from mac address

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import standardize_mac
        >>> standardize_mac("aa:bb:cc:dd:ee:ff")
        "aabbccddeeff"


mac_2digit_separated()
~~~~~~~~~~~~~~~~~~~~~~~~

    * converts input mac to 2 digit separated mac format, separator=`:`

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import mac_2digit_separated
        >>> mac_2digit_separated("aabb.ccdd.eeff")
        "aa:bb:cc:dd:ee:ff"

mac_4digit_separated()
~~~~~~~~~~~~~~~~~~~~~~~~~

    * converts input mac to 4 digit separated mac format, separator=`.`

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import mac_4digit_separated
        >>> mac_4digit_separated("aa:bb:cc:dd:ee:ff")
        "aabb.ccdd.eeff"

create_folders()
~~~~~~~~~~~~~~~~

    * Creates Folders
    * argument (folders) - can be string or list of strings.
    * argument (silent) - boolean to display messages or not.
    * returns if success or not

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import create_folders
        >>> create_folders([path1, path2], silent=True)


standardize_if()
~~~~~~~~~~~~~~~~~

    * standardizes interface naming
    * expand operator will make it full length name. Default is False.

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import standardize_if
        >>> standardize_if("FastEth1/0")
        "Fa1/0"
        >>> standardize_if("FastEth1/0", expand=True)
        "FastEthernet1/0"


get_file_path
~~~~~~~~~~~~~~~~~

    * returns Path object of provided file string.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import get_file_path
        get_file_path('c:/users/ali/documents/change_batch_1.xlsx')
        WindowsPath('c:/users/ali/documents')

get_file_name
~~~~~~~~~~~~~~~~~

    * returns filename of provided file string.
    * provide ext argument as True to get extension as well. 

    .. code-block:: python

        from nettoolkit.nettoolkit_common import get_file_name
        get_file_name('c:/users/al202t/documents/change_batch_1.xlsx')
        'change_batch_1'
        get_file_name('c:/users/al202t/documents/change_batch_1.xlsx', ext=True)
        'change_batch_1.xlsx'

create_folders
~~~~~~~~~~~~~~~~~

    * Create the folders dynamically via script.
    * provide list of folders create all folders.
    * provide silent=False, to display the activity. (default is True)

    .. code-block:: python

        from nettoolkit.nettoolkit_common import create_folders
        import os
        os.listdir('c:/users/ali/documents/')
        ['A T M', 'change_batch_1.xlsx', 'change_batch_2.xlsx',]

        folders_to_create = ['c:/users/ali/documents/test1', 'c:/users/ali/documents/test2']

        create_folders(folders_to_create)
        OK.
        OK.
        True
        os.listdir('c:/users/ali/documents/')
        ['A T M', 'change_batch_1.xlsx', 'change_batch_2.xlsx', 'test1', 'test2']

        folders_to_create = ['c:/users/ali/documents/test3', 'c:/users/ali/documents/test4']

        create_folders(folders_to_create, silent=False)
        Creating: c:/users/ali/documents/test3	OK.
        Creating: c:/users/ali/documents/test4	OK.
        True
        os.listdir('c:/users/ali/documents/')
        ['A T M', 'change_batch_1.xlsx', 'change_batch_2.xlsx', 'test1', 'test2', 'test3', 'test4']


detect_device_type
~~~~~~~~~~~~~~~~~~~~

    * detect the device type from the output configuration list
    * provide list as argument to function
    * 'Unidentified' will result if device type is not detected.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import detect_device_type

        file = "c:/users/ali/Desktop/some_cisco_output.log"
        with open(file, 'r' ) as f:
            lines = f.readlines()
            detect_device_type(lines)
            
        'Cisco'


        file = "c:/users/ali/Desktop/some_juniper_output.log"
        with open(file, 'r' ) as f:
            lines = f.readlines()
            detect_device_type(lines)
            
        'Juniper'


CapturesOut
~~~~~~~~~~~~~~~~~~~~

    * CapturesOut is a class providing multiple usefull methods and properties on a device commands capture output
    * provide the device log file as input to class
    * see some of properties and its method listed below.
    * There are many more, explore and identify more in detail.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import CapturesOut

        file1 = "c:/users/ali/Desktop/hostname-a.log"

        CO = CapturesOut(file1)
        CO.name
        'hostname-a'

        CO.device_type
        'Juniper'

        CO.has("show version")
        True
        CO.cmd_output("show version")
        ['#================================================================================', '', 'fpc0:', '--------------------------------------------------------------------------',  'Model: qfx5100-48s-6q', ...output trunked...]


        file2 = "c:/users/ali/Desktop/hostname-b.log"
        CO = CapturesOut(file2)
        CO.name
        'hostname-b'

        CO.device_type
        'Cisco'

        CO.has("show bgp summary")
        False
        CO.has("show version")
        True
        CO.has("sh ver")              ## Trunked commands also will accpet
        True

        CO.cmd_output("show version")
        ['!================================================================================', '', 'Cisco IOS XE Software, Version 17.06.04', 'Cisco IOS Software [Bengaluru], ...output trunked... ]

-------


add_blankdict_key
~~~~~~~~~~~~~~~~~~~~

    * Add a blank dictionary with provided key to provided dictionary.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import add_blankdict_key

        d = {'interfaces': {}}
        add_blankdict_key(d['interfaces'], 'Fa0/0')
        print(d)
        {'interfaces': {'Fa0/0': {}}}


add_blankset_key
~~~~~~~~~~~~~~~~~~~~

    * Add a blank set with provided key to provided dictionary.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import add_blankset_key

        tacacs = {}
        add_blankset_key(tacacs, 'servers')
        print(tacacs)
        {'servers': set()}

add_blanklist_key
~~~~~~~~~~~~~~~~~~~~

    * Add a blank list with provided key to provided dictionary.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import add_blanklist_key

        tacacs = {}
        add_blanklist_key(tacacs, 'servers')
        print(tacacs)
        {'servers': []}

add_blanktuple_key
~~~~~~~~~~~~~~~~~~~~

    * Add a blank tuple with provided key to provided dictionary.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import add_blanktuple_key

        tacacs = {}
        add_blanktuple_key(tacacs, 'servers')
        print(tacacs)
        {'servers': ()}

add_blanknone_key
~~~~~~~~~~~~~~~~~~~~

    * Add a blank None with provided key to provided dictionary.

    .. code-block:: python

        from nettoolkit.nettoolkit_common import add_blanknone_key

        intf_dict = {}
        add_blanknone_key(intf_dict, 'management')
        print(intf_dict)
        {'management': None}

update_key_value
~~~~~~~~~~~~~~~~~~~~

    * updates a key value pair to given dictionary only if the key is not exist.
    * syntex : update_key_value(dic, key, value)

    .. code-block:: python

        from nettoolkit.nettoolkit_common import update_key_value

        tacacs = {}
        update_key_value(tacacs, 'server', '10.10.10.1')
        print(tacacs)
        {'server': '10.10.10.1'}
        update_key_value(tacacs, 'server', '10.10.10.5')
        print(tacacs)
        {'server': '10.10.10.1'}

get_vlans_cisco
~~~~~~~~~~~~~~~~~~~~

    * get the vlan information from provided cisco input

    .. code-block:: python

        from nettoolkit.nettoolkit_common import get_vlans_cisco

        get_vlans_cisco("switchport trunk allowed vlan 10,20,30-34")
        {'vlan_members': '10,20,30-34', 'access_vlan': None, 'voice_vlan': None, 'native_vlan': None}
        get_vlans_cisco("switchport access vlan 201")
        {'vlan_members': set(), 'access_vlan': '201', 'voice_vlan': None, 'native_vlan': None}
        get_vlans_cisco("switchport voice vlan 201")
        {'vlan_members': set(), 'access_vlan': None, 'voice_vlan': '201', 'native_vlan': None}

trunk_vlans_cisco
~~~~~~~~~~~~~~~~~~~~

    * get the trunk vlans from provided cisco input

    .. code-block:: python

        from nettoolkit.nettoolkit_common import trunk_vlans_cisco

        trunk_vlans_cisco("switchport trunk allowed vlan 10,20,30-34")
        {32, '10', 33, 34, '20', 30, 31}


get_vrf_cisco
~~~~~~~~~~~~~~~~~~~~

    * get the vrf name from provided cisco input

    .. code-block:: python

        from nettoolkit.nettoolkit_common import get_vrf_cisco

        get_vrf_cisco(" vrf forwarding 100")
        '100'
