
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

