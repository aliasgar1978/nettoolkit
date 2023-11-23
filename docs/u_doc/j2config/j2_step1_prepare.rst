
Prepare Config Building Instance
============================================


.. code-block:: python

    # --------------------------------------------
    # IMPORTS
    # --------------------------------------------
    from nettoolkit.j2config import PrepareConfig

    # --------------------------------------------
    # Provide necessary inputs
    # --------------------------------------------
    data_file = "excel-datafile.xlsx"       # provide Excel database file 
    template_file = "text_template.j2"      # provide text jinja template file.
    output_path = "./output/"               # provide path where new config to be stored.(optional)

    # --------------------------------------------
    #    Define PrepareConfig class instance
    # --------------------------------------------
    PrCfg = PrepareConfig(
        data_file=data_file,          # (str): Excel database
        jtemplate_file=template_file, # (str): Jinja Template
        output_folder=output_path,    # (str, optional): output path. (default: ".")
		regional_file=None,           # (str, optional): custom static regional variable file. Defaults to None.
		regional_class=None,          # (class, optional): custom class returning frames to be merge with device var .
    )


.. attention::
    
    **Excel Data File**

    * It is advisable to generate the facts using  **facts_finder** package. So manual editing will be minimal. Otherwise a fresh manually prepared database will work either.
    * There must be a ``var`` tab in excel file. with **var** as jinja variable and **default** as replacement value of the jinja variable.
        * multiple values for a single variable can be added in a same cell by separating either by ``comma`` or ``enter``
    * There must be atleast one tabular column consisting interfaces details.
        * multiple type interface details can be in separate sheet as well. sheet name can be arbitrary any thing.
    * There can be a ``vrf`` tab consisting of instances details of device.
    * There can be a ``bgp`` tab consisting of bgp and its properties of device.


    * **regional_file** can be identical to ``var`` tab of data file, with two columns as **var** and **default**.



Make a Note of above Instance variable ``PrCfg``. We are going to use it in next steps.

-----


Continue Next page to customize jinja filters, skip the step otherwise.