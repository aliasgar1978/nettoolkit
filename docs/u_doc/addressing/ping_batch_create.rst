
ping batch-file prepare
============================================

Create batch file(s) for each ip's for the given prefixes and its names

.. code-block:: python
    :emphasize-lines: 2

    >>> from nettoolkit.addressing import create_batch_file
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
