
Create ping batch script file(s)
============================================


CLI Way
------------------

**Steps Involved:**

    * Import necessary functions
    * execute function by providing necessary input parameters

    .. code-block:: python
        :emphasize-lines: 2

        >>> from nettoolkit import create_batch_file
        >>> create_batch_file(prefixes, names, ip, op_folder)


    .. note::
        
        **inputs**

          * pfxs (list): list of prefixes
          * names (list): list of prefix names
          * ip (list): ip(s) for which batch file(s) to be created
          * op_folder (str): output folder where batch file(s) should be created



GUI Way
-------------------------------

**Steps Involved:**

    * Import necessary class
    * call class
    * Provide inputs on  tab,  click 'Go' to execute.
    * delete class instance

    .. code-block:: python
        :emphasize-lines: 2

        >>> from nettoolkit import CreateBatch
        >>> CB = CreateBatch()
        ## A new GUI Popup window will open for user inputs. provide inputs  on tab and click 'Go' 

        >>> del(CB)


-----


.. note::
        
    The feature is made available from the package >= 0.0.23

