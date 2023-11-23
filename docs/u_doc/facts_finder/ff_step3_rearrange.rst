
2. Rearrange CleanFacts
============================================


_ continued from previous page.


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
