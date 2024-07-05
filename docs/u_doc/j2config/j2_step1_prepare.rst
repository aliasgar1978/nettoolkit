
Prepare Config Building Instance
============================================


* We will start by building an object instance of PrepareConfig.
* Keep a few things handy like ( excel database, jinja template, )
* To override *var* tab databse, we will need a custom (regional_file) database, and a regional_class (ex: Region) to work on it.
* custom **regional_class** should inherit **ABSRegion** class from ``j2config`` package.  And must define a property called **frames** which should return a list containing pandas DataFrame object


.. code-block:: python

    # --------------------------------------------
    # IMPORTS
    # --------------------------------------------
    from nettoolkit.j2config import PrepareConfig

    # -----------------------------------------------------------------------------------------------------------------------------
    # Custom Regional information & Imports (Optional/Additional), sample project imports mentioned as below. (modify as per own)
    # -----------------------------------------------------------------------------------------------------------------------------
    from custom.custom_j2config.regional import Region      # Regional class definition, works with regional_file provided in step1. And override device 'var' data
    regional_file = 'global.xlsx'                           # regional file defining static var variable/values

    # --------------------------------------------
    # Provide necessary inputs
    # --------------------------------------------
    data_file = "excel-datafile.xlsx"       # provide Excel database file  ( Mandatory )
    template_file = "text_template.j2"      # provide text jinja template file. ( Mandatory )
    output_path = "./output/"               # provide path where new config to be stored.(Default: ".") Folder must exist if provided.

    # --------------------------------------------
    #    Define PrepareConfig class instance
    # --------------------------------------------
    PrCfg = PrepareConfig(
        data_file=data_file,          # (str): Excel database
        jtemplate_file=template_file, # (str): Jinja Template
        output_folder=output_path,    # (str, optional): output path. (default: ".")
        # provide below to custom regional data override 
        regional_file=regional_file,  # (str, optional): custom static regional variable file. (Default: None).
        regional_class=Region,        # (class, optional): custom class returning frames to be merge with device var . (Default: None)
    )


.. attention::
    
    **Excel Data File**

    * It is advisable to generate the facts using  ``nettoolkit.facts_finder`` package. So manual editing will be minimal. Alternatively a fresh manually prepared database will work either.

    **Requirements:**
    * There must be a ``var`` tab in excel file. with **var** as jinja variable and **default** as replacement value of the jinja variable.
    * multiple values for a single variable can be added in a same cell by separating either by ``comma`` or ``enter``
    * There must be atleast one tab with tabular column consisting interfaces details.
    * multiple type interface details can be in separate sheet as well. sheet name can be arbitrary any thing.
    * example1: There can be a ``vrf`` tab consisting of instances details of device.
    * example2: There can be a ``bgp`` tab consisting of bgp and its properties of device.
    * Check nettoolkit.facts_finder generated clean.xlsx file for samples.
    * **regional_file** should be identical to ``var`` tab of data file, with two ``columns`` as **var** and **default**.
    * Remember, custom **regional_file** database will override variables in device **var** tab. 



Make a Note of above Instance variable ``PrCfg``. We are going to use it in next steps.

-----


Continue Next page to ``customize jinja filters``, skip the step otherwise.