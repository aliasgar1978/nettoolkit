
IP Subnet scanner
============================================


CLI Way
------------------

**Steps Involved:**

    * Import necessary function, class
    * call function with two files as arguments

    .. code-block:: python
        :emphasize-lines: 2

        >>> from nettoolkit import get_first_ips, Ping
        >>> iplist = get_first_ips(pfxs, till=5)
        >>>
        >>> # Initiate Ping, and write out Excel
        >>> P = Ping(iplist, concurrent_connections=1000)
        >>> P.op_to_xl(output_file)


.. note::

    **inputs**

    * pfxs (list): list of prefixes
    * till (int, optional): how many ips to select. (Default: 5)
    * iplist (list): list of ips to be pinged (created using get_first_ips function)
    * concurrent_connections (int, optional): number of max sockets to open parallel for ping check. (default: 1000)
    * output_file (str): path/name of excel file where ping responces to be stored.



GUI Way
-------------------------------

**Steps Involved:**

    * Import necessary class
    * call class
    * Provide inputs on `Subnet Scan` tab  and click 'Go' to execute.
    * delete class instance

    .. code-block:: python
        :emphasize-lines: 2

        >>> from nettoolkit import Nettoolkit
        >>> NTK = Nettoolkit()         ## A new GUI Popup window will open for user inputs. provide inputs on `Subnet Scan` tab and click 'Go' 
        >>> del(NTK)


-----


.. note::
        
	The feature is made available from the package >= 0.0.23, 
	And clubbed together in 0.0.24

