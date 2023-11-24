
Generate Visio
==============

Supported for nettoolkit version >= 0.1.0

-----

.. Note::

    * update **dic** dictionary in below snippet, with necessary 'sheet_filters' & 'is_sheet_filter' key/values, if executing standlone.
    * updation of **dic** dictionary in below snippet will automatically happen, if beow script will continue with preivous page snippet.


Lets start by defining a few more required static inputs. Modify it as needed.


.. code-block:: python


  # --------------------------------------------
  #  INPUTS
  # --------------------------------------------
  STENCIL_FOLDER = 'path/where/stencilfiles/stored'
  VISIO_OP_FILE = 'output.vsd'


  # ----------------------------------------------------------------------------------
  # update input Dictionary
  # ----------------------------------------------------------------------------------
  dic = {
    # Mandatory
    'stencil_folder': STENCIL_FOLDER,
    'data_file': CABLE_MATRIX_OP_FILE,
    'op_file': VISIO_OP_FILE,

    # Optional
    'default_stencil': DEFAULT_STENCIL,

    # Optional /  list of additional columns to be merged with device details., example given below.
    # modify as needed
    'cols_to_merge': ['ip_address', 'device_model', 'serial_number' ],
  }
  dic.update(sheet_filter_dict)

  # ----------------------------------------------------------------------------------
  # Create Visio
  # ----------------------------------------------------------------------------------
  pyVig(**dic)

