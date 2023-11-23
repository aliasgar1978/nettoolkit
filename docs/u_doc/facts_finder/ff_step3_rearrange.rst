
2. Rearrange CleanFacts
============================================


* Use below code snippet to update clean facts file columns in specifc order.
* foreign_keys defines custom columns arrangement.


#. **Rearrange**

    .. code-block:: python


        # --------------------------------------------
        # IMPORTS
        # --------------------------------------------
        from nettoolkit.facts_finder import rearrange_tables

        # -------------------------------------------------------------------------------------------------------------
        # Rearrange tables.  
        # -------------------------------------------------------------------------------------------------------------
        rearrange_tables(   
            clean_file,                #  (str) generated clean file from previous step 
            foreign_keys=FOREIGN_KEYS  #  (dict) Custom {sheet: [columns]}  keys to define sequence of columns 
        )
