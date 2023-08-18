
Compare two subnet scanner output files
============================================


CLI Way
------------------

**Steps Involved:**

	* Import necessary functions
	* call function with two files as arguments

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import compare_ping_sweeps
		>>> compare_ping_sweeps(first, second)      # where first and second are two excel file(s)



GUI Way
-------------------------------

**Steps Involved:**

	* Import necessary class
	* call class
	* Provide inputs on `Compare Outputs` tab  and click 'Go' to execute.
	* delete class instance

	.. code-block:: python
		:emphasize-lines: 2

		>>> from nettoolkit import SubnetScan
		>>> SS = SubnetScan()      ## A new GUI Popup window will open for user inputs. provide inputs on `Compare Outputs` tab and click 'Go' 
		>>> del(SS)


-----


.. note::
		
	The feature is made available from the package >= 0.0.23

