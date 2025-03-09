GUI Launch
------------

Nettoolkit offers flexibility to access its toolset in various ways.. 
GUI is one of its way. 

   * Get most of Nettoolkit features accessible via GUI now.
   * **Custom classes** inheritance, is feasible **via yaml** file.
   * ``Launch GUI with minimal code``.


.. code-block:: python

    from nettoolkit import Nettoolkit     ## import GUI
    N = Nettoolkit()                      ## Define GUI
    N(initial_frame='crypt')              ## Call it with/without initial frame


* Launch Nettoolkit with your desired page by providing initial_frame name in lower.
* *initial_frame* options

   * addressing
   * captureit
   * facts
   * configgen
   * configure
   * crypt
   * juniper
   * visiogen

* Launching Nettoolkit without any of above or wrong input initial_frame; will load all frames and focus on first.

Continue enjoy your exploration with it.