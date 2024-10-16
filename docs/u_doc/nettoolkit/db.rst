
A few Database operations
======================================

**Interacting with Excel Database**


Lets first import all available functions from nettoolkit_db

.. code-block:: python
    
    >>> from nettoolkit.nettoolkit_db import *


**Available Functions**


get_merged_DataFrame_of_file()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    * returns merged DataFrame after clubbing all tabs of file
    * all tabs should contain identical columns in order to merge them

    .. code-block:: python

        >>> file = "inputfile.xlsx"
        >>> df = get_merged_DataFrame_of_file(file)


append_to_xl()
~~~~~~~~~~~~~~~

    * appends dictionary of dataframes to an Excel file, existing tabs will be retained, if different
    * overwrite: will append data to existing file, else create a copy and adds data to it
    * index_label: to set the index label for each tab, None else

    .. code-block:: python

        >>> d = {"Sheet_A": DataFrame_A, "Sheet_B": DataFrame_B, "Sheet_C": DataFrame_C,}
        >>> append_to_xl('output_file.xlsx', d)


write_to_xl()
~~~~~~~~~~~~~~~

    * Create a new Excel file with provided dictionary of dataframes
    * overwrite: removes existing file, else create a copy if file exist
    * index: boolean value, to mention about index column requirement
    * index_label: to set the index label for each tab, None else

    .. code-block:: python

        >>> d = {"Sheet_A": DataFrame_A, "Sheet_B": DataFrame_B, "Sheet_C": DataFrame_C,}
        >>> write_to_xl('output_file.xlsx', d)



sort_dataframe_on_subnet()
~~~~~~~~~~~~~~~~~~~~~~~~~~

    * sort provided dataframe on the provided subnet column. default ascending order

    .. code-block:: python

        >>> df = pd.DataFrame({"Col_A":['colA Values', ..], "Subnet":['subnets values', ..],  "Col_C":['colC Values', ..],    })
        >>> sorted_df = sort_dataframe_on_subnet(df, col="Subnet")



read_xl_all_sheet()
~~~~~~~~~~~~~~~~~~~~~~~~~~

    * Read all Excel tabs and return it in dictionary format. 
    * keys will be tab names and values will be tab in DataFrame format

    .. code-block:: python

        >>> file = "c:/users/user/downloads/test.xlsx"
        >>> dfd = read_xl_all_sheet(file)
        >>> print(dfd.keys())
            dict_keys(['var', 'bgp', 'vrf', 'ospf', 'static', 'prefix_list', 'vlan', 'tunnel', 'loopback', 'physical', 'block'])
        >>> for k, v in dfd.items():
                print(type(v))

            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>
            <class 'pandas.core.frame.DataFrame'>

read_an_xl_sheet
~~~~~~~~~~~~~~~~~~~~~~~~~

    * Read an Excel file, which has a single tab in it. 
    * returns DataFrame

    .. code-block:: python

        >>> file = "c:/users/user/downloads/test.xlsx"
        >>> df = read_an_xl_sheet(file)
        >>> print(type(df))
        <class 'pandas.core.frame.DataFrame'>


dict_to_yaml()
~~~~~~~~~~~~~~~~~~~~~~~~~~

    * converts dictionary to yaml format and write it to a yaml file.

    .. code-block:: python

        >>> d = {'a': [1,2,3], 'b': 'some string', 'c': {'ca': 'nested a', 'cb': 'nested b'} }
        >>> dict_to_yaml(d, file='outputfile.yaml', mode='a')
        'a:\n- 1\n- 2\n- 3\nb: some string\nc:\n  ca: nested a\n  cb: nested b\n'
    

    .. code-block::

        # Output yaml file content

        a:
        - 1
        - 2
        - 3
        b: some string
        c:
        ca: nested a
        cb: nested b


yaml_to_dict()
~~~~~~~~~~~~~~~~~~~~~~~~~~

    * Reads yaml database, converts and return content in dictionary format
    * lets use above output yaml file as input to see its content back in dictionary

    .. code-block:: python

        >>> file = "outputfile.yaml"
        >>> d = yaml_to_dict(file)
        >>> print(d)
        {'a': [1, 2, 3], 'b': 'some string', 'c': {'ca': 'nested a', 'cb': 'nested b'}}

