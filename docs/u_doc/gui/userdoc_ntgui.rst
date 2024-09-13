
Nettoolkits GUI Summary
###############################################


Nettoolkit offers flexibility to access its toolset in various ways.. 
GUI is one of its way. 

   * Get most of Nettoolkit features accessible via GUI now.
   * **Custom classes** inheritance, is feasible **via yaml** file.
   * ``Launch GUI with minimal code``.


GUI Launch
------------

.. code-block:: python

    from nettoolkit import Nettoolkit     ## import GUI
    N = Nettoolkit()                      ## Define GUI
    N(initial_frame='crypt')              ## Call it with/without initial frame


* Launch Nettoolkit with your desired page by providing initial_frame name in lower.
* *initial_frame* options

   * addressing
   * captureit
   * configure
   * j2config
   * crypt
   * factsgen
   * juniper
   * pyvig

* Launching Nettoolkit without any of above initial_frame; will load all frames and focus on first.

Continue enjoy your exploration with it.

----

**Now lets get familiar with each in some more details...**

.. toctree::
   :maxdepth: 4
   :caption: Contents:


   Addressing Tab <img_gallery_addressing>
   Capture-IT Tab <img_gallery_capture_it>
   Configure Tab <img_gallery_configure_it>
   Config Gen Tab <img_gallery_configs_gen>
   Crypt Tab <img_gallery_crypt>
   Facts Tab <img_gallery_facts_gen>
   Juniper Tab <img_gallery_juniper>
   Visio Gen Tab <img_gallery_visio_gen>

