Version Control
=================================================

.. figure:: images/nettoolkit_logo.jpg
   :scale: 15%
   :alt: Nettoolkit
   :align: right


Nettoolkit keeps updated and released on a regular basis. 

Here is version changes detail.



.. list-table:: Version 1.x updates
   :widths: 10 15 200
   :align: left
   :header-rows: 1


   * - Version
     - Date   
     - Updates

   * - 1.7.3
     - MMM dd, 2024 [TBR]
     - * [TBR]
       * [TBR]
   * - 1.7.2
     - Aug 24, 2024
     - * ``addressing`` a few bug fixes and a few methods added to IP classes.
       * ``gpl.LST`` added a new staticmethod ``longest_str_len``.  **nettoolkit_common.printmsg**, **nettoolkit_common.create_folders** added.
       * ``capture-it`` execution output modified to display better 
   * - 1.7.1
     - Aug 12, 2024
     - * ``facts-finder`` each individual parser return changed from normal dict to op_dict. (respective changes to parent codes)
       * ``NGui`` - New class added to dynamically create custom GUI Frames. Nettoolkit GUI modified to be child of it.
       * ``nettoolkit_db.yaml_to_dict`` : new function added.
   * - 1.7.0
     - Jul 31, 2024
     -  ``capture-it`` version 1.7.0 has changed the implementation of capture-it slightly to incorporate new features.  
        Kindly refer to following documentation pages to understand and co-relate changes.
        Your previous execution codes may fail, and requires to be modified slightly in order to support version 1.7.0 onward.

        Below are brief summary about changes.

          * **capture_by_excel** - added for capturing outputs from standard excel 
          * failed devices *list* added in report
          * **log_summary** method added and incorporated to caputres
          * *Excel log summary* feature added 
          * input **path** argument change to **capture_path**
          * A few Bug fixes.
   * - 1.6.6
     - Jul 26, 2024
     - * capture-it: code enhancements and a few bug fixes.
       * facts-finder: ``remove_cit_bkp`` key added.
   * - 1.6.5
     - Jul 21, 2024
     - explicitly skip load pysimpleGUI module, due to readthedocs incompatibility. it will give further code execution errors if not loaded properly.
   * - 1.6.4
     - Jul 21, 2024
     - removed pywin32 dependancy from setup.py, should be done separately.
   * - 1.6.3
     - Jul 5, 2024
     - * capture-it: added keys (**missing_captures_only**, **append_capture**).
       * configure: module updated with various new parameters
       * compare-it: added (CompareConfig) function
       * nettoolkit_db: addded (read_xl_all_sheet) function
       * Forms: restructured & added configure fuction
       * A few bug fixes.
   * - 1.6.2
     - May 25, 2024
     - * addressing: added get octet method and devide prefix function.
       * j2config: added common function for converting value to string.
       * configure: New draft/beta module added.
   * - 1.6.1
     - Mar 22, 2024
     - capture-it: rewamp code, separate out device detection module. Removed a few extra overhead logging feature. Added failure devices listing.
   * - 1.5.8
     - Mar 08, 2024
     - * pyNetCrypt: bug fix in cpwcracker. File p/w encryption/decryption added in Forms
       * database subnet sort: added nettoolkit_db.sort_dataframe_on_subnet functionality.
       * facts-finder: Juniper static routes - resolve/retain parser added., bug fix on juniper prefix-list parser.
       * capture-it: configure (beta) module added. A few bug fixes. read-timeout increased from 20 to 30
       * addressing: Allocate ( added **iterate_base_ip** argument, in order to change or not to change after each allocation )
   * - 1.5.7
     - Jan 15, 2024
     - pyVig: manually line color map add/edit functionality added.
   * - 1.5.6
     - Jan 15, 2024
     - Version Upload failed.
   * - 1.5.5
     - Jan 12, 2024
     - * capture-it: Fixed, log summary duplication on cross device types.
       * pyVig: change match type to case-insensitive SFP type instead of case sensitive
       * pyVig: Added Line Color & Weight auto selection based on detected Cable type
       * pyVig: custom mandatory functions, dependancy removed.
   * - 1.5.4
     - Jan 10, 2024
     - capture-it: **individual capture** device specific commands capture functionality added, and a few minor flow changes.
   * - 1.5.3
     - Jan 9, 2024
     - * nettoolkit database: Dataframe **sort** functionality based **on subnets** column added.
       * facts-finder: Command parsers added for ``prefix-lists`` (cisco & juniper), parser edited for secondary ip address retrival.
       * addressing: Bug fix on comparision of two IP objects. (equality comparision).  
       * addressing.Allocations added with **allocation_type** property to specify which type of allocation follows.   Added method **add_prefix** to add prefix to allocation.
       * addressing.Allocate instances can be now initialized with an existing Allocations object instead of creating fresh each time.
       * pyvig: update_self_details fixed for singleton.
       * capture-it: added a new propery - **mandatory_cmds_retries**
   * - 1.5.2
     - Jan 2, 2024
     - * Bug fixes: facts-finder juniper static route section
       * capture-it: device log output file name to lower case.
       * addressing: bug fixes, and enhancements to Allocations.  IPv4.ipn method added
   * - 1.5.1
     - Dec 26, 2023
     - * Bug fixes: facts-finder, addressing
       * addressing: Added a few new functionalities
       * Cable-Matrix: Added a few more columns
   * - 1.5.0
     - Dec 23, 2023
     - * Juniper: included the comments in set-converter & facts-finder.
       * addressing: added ipv4 sort functionality (sorted_v4_addresses)
       * capture_it: bug fixes, and log display output modified
       * facts_finder: bug fixes on cisco - cdp neighbor output, and show run for ospf details, added dhcp ip verification (parser verifications display msg updated)
       * facts_finder: bug fixes on juniper - port_type changed to media_type (parser verifications display msg updated)
       * pyVig: cache functionality added for cables and connectors to prepare cable matrix, cabling details revamped to capture more cable and connector information,  bug fix on default line color. 
       * Added a new functionality to get cable-matrix file with more details
   * - 1.4.3
     - Dec 14, 2023
     - Added addressing.recapsulate function
   * - 1.4.2
     - Dec 13, 2023
     - Bug fixes 1.cisco device model capture. 2.cdp neighbor parse enabled and fixed. 3.juniper password capture error fixed for ospf and tacacs.  4.header index capture based on split added.
   * - 1.4.1
     - Dec 9, 2023
     - * Added a new GUI tab for quick show command
       * Added cache functionality for some of GUI fields.
       * Bug fix an import error
   * - 1.4.0
     - Nov 30, 2023
     - * Bug fix for pyVig y-axis alignment error
       * Forms view updated and shuffled form files to its respective parent project folder.
       * compare-it added
   * - 1.3.2
     - Nov 28, 2023
     - Bug fix - for error uploading forms
   * - 1.3.1
     - Nov 28, 2023
     - Error uploading forms
   * - 1.3.0
     - Nov 28, 2023
     - Error uploading forms
   * - 1.2.0
     - Nov 25, 2023
     - * capture-it: updated to delete old log and start logging with fresh file(s), pw input enabled for `*`.
       * GUI: a few bug fixes
       * Direct class/methods import enabled for modules nettoolkit_db, nettoolkit_common, pyNetCrypt, GUI
       * addressing module brought outside of inner nettoolkit package, and relevant changes to other modules
   * - 1.1.0
     - Nov 24, 2023
     - missing form error fixed 
   * - 1.0.0
     - Nov 22, 2023
     - * New Major Release. 
       * Multiple changes. Not compatible with old version.
       * incorporated ( capture-it, facts-finder, j2config, pyVig, pyJUniper, pyNetCrypt ) pacakages in to single package.
       * GUI interface added for a few modules: ( minitools, addressing, capture-it, facts-finder )
       


.. list-table:: Version 0.x updates
   :widths: 10 15 200
   :align: left
   :header-rows: 1

   * - Version
     - Date   
     - Updates

   * - 0.0.1
     - Nov 10, 2020
     - Initial release on pypi 
   * - 0.0.2
     - Mar 10, 2021
     - Error in upload - skipped
   * - 0.0.3
     - Mar 10, 2021
     - untracked
   * - 0.0.4
     - Mar 10, 2021
     - untracked
   * - 0.0.5
     - May 20, 2021
     - Error in upload - skipped
   * - 0.0.6
     - May 20, 2021
     - untracked
   * - 0.0.7
     - May 20, 2021
     - untracked
   * - 0.0.8
     - Jul 4, 2021
     - untracked
   * - 0.0.9
     - Jul 6, 2021
     - untracked
   * - 0.0.10
     - Jan 3, 2022
     - untracked
   * - 0.0.11
     - Feb 14, 2022
     - jset code reverted, gpl and hierarchy updated 
   * - 0.0.12
     - Feb 16, 2022
     - documentation updates
   * - 0.0.13
     - Mar 5, 2022
     - cisco password cracker added
   * - 0.0.14
     - Mar 5, 2022
     - untracked
   * - 0.0.15
     - Dec 28, 2022
     - j-set bug fix
   * - 0.0.16
     - Dec 31, 2022
     - cisco interface trimming bug fix
   * - 0.0.17
     - Jan 22, 2023
     - database module added, edited gpl, juniper password cracker added. jset incorporated in juniper module
   * - 0.0.18
     - Jan 23, 2023
     - untracked
   * - 0.0.19
     - Feb 2, 2023
     - untracked
   * - 0.0.20
     - Feb 25, 2023
     - update in addressing module
   * - 0.0.21
     - Jun 29, 2023
     - corrected console display message for error writing database.
   * - 0.0.22
     - Jul 12, 2023
     - Feature add: juniper configuration - file passwords decrypt, file passwords mask.
   * - 0.0.23
     - Aug 18, 2023
     - Feature add:
        * ping batch file creations 
        * ip subnet scanner
        * ping responce comparisions
   * - 0.0.24
     - Aug 20, 2023
     - individual GUI Forms clubbed together into a single class ``Nettoolkit``.
   * - 0.0.25
     - Sep 8, 2023
     - added multi-tab ip subnet scanner feature, defult full subnet scan feature.
   * - 0.1.0
     - Sep 10, 2023
     - New Major version change. Multiple changes.  Not compatible with old version.



-----


.. note::

   some of version updates were untracked.

