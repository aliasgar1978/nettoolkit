
Nettoolkits GUI Summary
###############################################


Nettoolkit offers flexibility to access its toolset in various ways.. 
GUI is one of its way. 

   * Get most of Nettoolkit features accessible via GUI now.
   * Custom class inheritance, is feasible via yaml file.
   * Launch GUI with minimal codes.


GUI Launch
============

.. code-block:: python

    from nettoolkit import Nettoolkit
    N = Nettoolkit()
    N(initial_frame='crypt')
    del(N)


* Launch Nettoolkit with your desired page by providing initial_frame name in lower.
* available options are = (addressing, captureit, configure, j2config, crypt, factsgen, juniper, pyvig )
* Launching Nettoolkit without any initial_frame will load load all frames at once and focus on first frame.


----

.. toctree::
   :maxdepth: 4
   :caption: Contents:


   Addressing <img_gallery_addressing>
   Capture-IT <img_gallery_capture_it>
   Configure <img_gallery_configure_it>
   Config Gen <img_gallery_configs_gen>
   Crypt <img_gallery_crypt>
   Facts <img_gallery_facts_gen>
   Juniper <img_gallery_juniper>
   Visio Gen <img_gallery_visio_gen>

