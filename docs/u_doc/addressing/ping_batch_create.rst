
ping batch-script prepare
============================================

* Import necessary functions
* execute function by providing necessary input parameters

.. code-block:: python
    :emphasize-lines: 2

    >>> from nettoolkit.nettoolkit import create_batch_file
    >>> create_batch_file(prefixes, names, ip, op_folder)


.. note::
    
    **inputs**

        * pfxs (list): list of prefixes
        * names (list): list of prefix names
        * ip (list): ip(s) for which batch file(s) to be created
        * op_folder (str): output folder where batch file(s) should be created

-----


.. note::
        
	The feature is made available from the package >= 0.0.23, 
	And clubbed together in 0.0.24

