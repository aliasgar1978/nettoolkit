
Generate Visio
==============

Available for nettoolkit version >= 0.1.0

-----

.. Note::

    * update **dic** dictionary in below snippet, with necessary 'sheet_filters' & 'is_sheet_filter' key/values, if executing standlone.
    * updation of **dic** dictionary in below snippet will automatically happen, if beow script will continue with preivous page snippet.


Lets start by defining a few more required static inputs. Modify it as needed.


.. code-block:: python


  # --------------------------------------------
  #  INPUTS - modify as desired
  # --------------------------------------------
  STENCIL_FOLDER = 'path/where/stencilfiles/stored'
  VISIO_OP_FILE = 'output.vsd'


  # ----------------------------------------------------------------------------------
  # update input Dictionary
  # ----------------------------------------------------------------------------------
  dic = {
    # Mandatory
    'data_file': CABLE_MATRIX_OP_FILE,
    'op_file': VISIO_OP_FILE,
    'stencil_folder': STENCIL_FOLDER,

    # Optional
    'default_stencil': DEFAULT_STENCIL,

    # Optional /  list of additional columns to be merged with device details., example given below.
    # modify and add more custom columns as needed
    'cols_to_merge': [ 'device_model', 'serial_number' ],
  }

  # ----------------------------------------------------------------------------------
  # Update sheet_filter_dict ( either manually or from previous page )
  # ----------------------------------------------------------------------------------
  # a sample sheet_filter_dict will be as follows (if manually providing)
  sheet_filter_dict = {
    'is_sheet_filter': True, 
    'sheet_filters': {
        'wireless block': 'wireless block', 
        'core': 'core', 
        'private boarder blocks': 'private boarder blocks', 
        # ... add more as needed ... #
    }, 
  }

  # update dic with above additional filter dict
  dic.update(sheet_filter_dict)   # sheet_filter_dict >> from previous page

  # ----------------------------------------------------------------------------------
  # Create Visio
  # ----------------------------------------------------------------------------------
  pyVig(**dic)

-----

Enjoy!