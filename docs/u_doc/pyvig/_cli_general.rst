Option 1: CLI Execution - Manual XL
==========================================================

.. warning::

	* Deprycated method.  Not supported for nettoolkit version >= 0.1.0
	* Use only if you have standalone pyVig package installed with nettoolkit version < 1.0.0 

Follow below steps for Command Line Execution steps


----------------------------

Prepare Excel (CLI)
----------------------

   #. Prepare Excel as per guidelines given in previous **Excel database Preparation Page**.
   #. :download:`Sample <samples/Excel-pyvig-sample.xlsx>`. pyVig readable Sample Excel file with Devices and Cablings Tab.


-----


Prepare python code
------------------------------

	.. code-block:: python
	
		# --------------------------------------------------------------------------------------
		# 1. Import package
		# 2. Call pyVig with necessary inputs ( remove undesired optional input arguments )
		# --------------------------------------------------------------------------------------
		from pyVig import pyVig
		pyVig(
			# ------------- Two Mandatory arguments -------------
			stencil_folder = '/fullpath_stencil_folder',
			data_file = '/fullpath/data_file',

			# ------------- Optional arguments / inputs Follows -------------
			default_stencil = 'Network and Peripherals',    #(default: None)
			op_file = 'output_filename.vsdx',    # (default: None)

			x = 'x',    # (default: 'x-axis', Devices Tab)
			y = 'y',    # (default: 'y-axis', Devices Tab)

			dev_a = 'a',    # (default: 'a_device', Cablings Tab)
			dev_b = 'b',    # (default: 'b_device', Cablings Tab)

			# Additional information from various columns to be merged in device description 
			cols_to_merge = ['device_model', 'serial_number', 'ip_address', .. ],	# (default: [], , Devices Tab)

			# Device icon formatting 
			format_columns = {
				'iconHeight': 1,    # sets default iconHeight (default: 1)
				'iconWidth': 2.5,    # sets default iconWidth (default: 2.5) 
			},

			# Different Filter options
			filter_on_cable = False,    # (filter to drop connected devices only, default: True)
			filter_on_include_col = True,    # (looks for non-empty rows for column 'include' to select cablings; default: False)
			is_sheet_filter = False,    # (Default: True, enables filtering on 'sheet_filters' input,  overrides 'filter_on_include_col')
			sheet_filters = {
				'draw_type': ('core', 'access', ),   ## Here column name = 'draw_type' , matching and filtering rows value as per given in tuple. 
				# Add more filters as required.... 
			},

		)

		# --------------------------------------------------------------------------------------


-----


	.. tip::
		
		* Do not interrupt the visio application while visio generation is inprogress.
		* Once Finished save the file as required.
		* Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.

