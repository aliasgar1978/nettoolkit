
IP Subnet scanner
============================================


CLI Way
------------------

**Steps Involved:**

    * Import necessary class
    * call function with two files as arguments

    .. code-block:: python
        :emphasize-lines: 4

        >>> from nettoolkit import Ping
        >>>
        >>> # Initiate Ping, and write out Excel
        >>> P = Ping(pfxs, till=5, concurrent_connections=1000, create_tabs=True)
        >>> P.op_to_xl(output_file)


.. note::

    **inputs**

    * pfxs (list): list of prefixes
    * till (int, optional): how many ips to select. (Default: 5)
    * concurrent_connections (int, optional): number of max sockets to open parallel for ping check. (default: 1000)
    * create_tabs (bool, optional): whether to create individual tabs for each subnet or not (default: False)
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

