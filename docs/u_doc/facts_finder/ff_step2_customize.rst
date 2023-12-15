
Customize CleanFacts
============================================

* Use below given code/process to modify the generated clean facts file.
* There should be custom script/class to do the same.
* Refer previous page to identify the properties of cleaned_fact object in order to process data.


.. code-block:: python

    # -------------------------------------------------------------------------------------------------------------
    # Custom Project Imports (Optional/Additional), a sample project import mentioned as below. (modify as per own)
    # -------------------------------------------------------------------------------------------------------------
    from custom.custom_factsgen import CustomDeviceFacts     ## CustomDeviceFacts is a class to modify output database as per custom requirement.
    from custom.custom_factsgen import FOREIGN_KEYS          ## FOREIGN_KEYS, define dictionary with additional custom columns require in output databse {tab_name : [column names]} format.


    # -------------------------------------------------------------------------------------------------------------
    # Create an instance of custom project class.
    # -------------------------------------------------------------------------------------------------------------
    ADF = CustomDeviceFacts(cleaned_fact)  # cleaned_fact - object instance created from previous page
    ADF.write()                            # method defining overwrite output file with updated data   




.. important::

    **Rearrange**

    * continue next page for adding and re-arranging additional custom colums.


