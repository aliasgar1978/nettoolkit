Option 2: GUI Execution - Manual XL
==========================================================

Follow below steps for GUI based Execution


-----


Prepare Excel
----------------------

   #. Prepare Excel as per guidelines given in previous **Excel database Preparation page**.
   #. :download:`Sample <samples/Excel-pyvig-sample.xlsx>`. pyVig readable Sample Excel file with Devices and Cablings Tab.


-----

Import and run pyVig_gui from pyVig
------------------------------------------


	.. code-block:: python
	
		from nettoolkit.pyVig import pyVig_gui  ## TBD , update requires
		pyVig_gui()


	Provide the information in selection windows and click Run.


	.. tip::
		
		Do not interrupt the visio application while visio generation is inprogress. 

		Once Finished save the file as required.

		Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.



------------------------------



