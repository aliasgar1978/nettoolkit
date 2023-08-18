
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
        >>> P = Ping(iplist)
        >>> P.op_to_xl(output_file)


.. note::

    **inputs**

    * pfxs (list): list of prefixes
    * till (int, optional): how many ips to select. Defaults to 5.

    **returns**
    
    * list: crafted list with first (n) ip addresses from each subnet



GUI Way
-------------------------------

**Steps Involved:**

    * Import necessary class
    * call class
    * Provide inputs on `Subnet Scan` tab  and click 'Go' to execute.
    * delete class instance

    .. code-block:: python
        :emphasize-lines: 2

        >>> from nettoolkit import SubnetScan
        >>> SS = SubnetScan()         ## A new GUI Popup window will open for user inputs. provide inputs on `Subnet Scan` tab and click 'Go' 
        >>> del(SS)


-----


.. note::
        
    The feature is made available from the package >= 0.0.23

