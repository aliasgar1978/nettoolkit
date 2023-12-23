
IP Subnets Scanner
============================================


Ping to multiple ip addresses from given subnets and get the report in Excel file

.. code-block:: python
    :emphasize-lines: 4

    >>> from nettoolkit.addressing import Ping
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


-----


.. note::
        
	The feature is made available from the package >= 0.0.23, 

