
Nt Capture-it - Devices Group by Excel tabs
==================================================================

.. note::

    * This feature made available from nettoolkit version 1.7.0 onwards.
    * original **capture_individual** - deprycated and replced with **capture_by_excel**


.. important::

    * Use the below explained Excel method if you have multiple groups of devices, And you want to run a particuar set of show commands for each groups.
    * Use the previous page method if you have list of devices where, you want to capture the same show commands output from all of devices.


#. **Execution Steps**

    .. code-block:: python

        # --------------------------------------------
        # 1. IMPORT NECESSARY PACKAGE/MODULES
        # --------------------------------------------
        from nettoolkit.capture_it import capture_by_excel

        # -------------------------------------------------------------------------------------------------------------
        # 2. Custom Project Imports (Optional/Additional), a sample project import mentioned as below. (modify as per own)
        # -------------------------------------------------------------------------------------------------------------
        from custom.custom_captureit.cisco_bgp import BgpAdv     ## **BgpAdv** class should have a **cmds** property to return custom show commands
        from custom.custom_factsgen import CustomDeviceFacts     ## **CustomDeviceFacts** class is to modify output excel database as per custom requirement.
        from custom.custom_factsgen import FOREIGN_KEYS          ## **FOREIGN_KEYS**, dictionary has custom columns example: {tab_name : [column names]} format.

        # --------------------------------------------
        # 3. INPUT: Credentials
        # --------------------------------------------
        auth = {
            'un':'provide username' , 
            'pw':'provide login password', 
            'en':'provide enable password'  
        }

        # -------------------------------------------------------------------
        # 4. INPUT: Excel file, group of devices:commands separated by tabs.
        #    Sample file attached below. 
        # -------------------------------------------------------------------
        dev_cmd_xl_file = f'devices_cmds.xlsx'

        # --------------------------------------------
        #  7. INPUT: Provide Output paths
        # --------------------------------------------
        capture_path     = './captures/'
        exec_log_path    = './logs/'

        # --------------------------------------------
        # 8. Define capture Object as cap
        # --------------------------------------------
        cap = capture_by_excel(
            auth=auth,
            input_file=dev_cmd_xl_file,
            capture_path=capture_path,
            exec_log_path=exec_log_path,
        )

        # -------------------------------------------------------------------------
        # 9. Optional: capture keys modifications
        # -------------------------------------------------------------------------
        cap.standard_output = True   # default: False ( options: True, False )
        cap.max_connections = 500    # default: 100 ( Options: number input ) ( Use 1 for sequencial )
        cap.tablefmt = 'outline' # default: 'pretty' ( Options: see below** )

        # -----------------------------------------------------------------------------
        # 10. Optional dynamic custom commands.
        #     Remove if not importing custom captureit class in step 2
        # -----------------------------------------------------------------------------
        cap.dependent_cmds(custom_dynamic_cmd_class=BgpAdv)  # BgpAdv is custom class

        # -------------------------------------------------------------------------------
        # 11.Optional to generate Facts
        #    Remove arguments in generate_facts if not importing custom class in step 2
        # --------------------------------------------------------------------------------
        cap.generate_facts(
            CustomDeviceFactsClass=CustomDeviceFacts,  ## custom, optional
            foreign_keys=FOREIGN_KEYS,                 ## custom, optional
        )

        # -----------------------------------------------------------------------------
        # 12. Start Capture
        # -----------------------------------------------------------------------------
        cap()

        # -----------------------------------------------------------------------------
        # 13. Log-Summary ( Modify as require )
        # -----------------------------------------------------------------------------
        txt_log_file = exec_log_path + "/" + "summary_log.txt"
        xl_log_file  = exec_log_path + "/" + "summary_log.xlsx"
        cap.log_summary(
            on_screen_display=True,                   # on screen display
            to_file=txt_log_file,                     # to text file
            excel_report_file=xl_log_file,            # to excel file
        )

        # -----------------------------------------------------------------------------


----


.. important::
    
    **Parameters for capture_by_excel**

    * ``input_file``  excel file name which contains information on ips and their related commands to capture 
    * ``auth``  authentication Parameters
    * ``capture_path``  output path for commands captures ( use "." for storing in same relative folder )
    * ``exec_log_path`` output path for execution logs ( use "." for storing in smae relative folder )
    * ``max_connections``  (numeric) (Default: 100), change the number of simultaneous device connections as per link connection and your pc cpu processng performance.
    * ``standard_output``  (Options: True, False) (Default: False) capture to be done in capture it format or normal standard capture format.
    * ``on_screen_display`` (bool): displays result summary on screen. Defaults to False.
    * ``to_file`` (str): text filename, writes summary result summary to text file. Defaults to None 
    * ``excel_report_file`` (str): excel filename, writes summary result summary to excel file. Default to None 
    * ``tablefmt`` ( Options:
        'rounded_outline', 'simple_outline', 'heavy_outline', 'mixed_outline', 'double_outline', 'fancy_outline',
        'presto', 'outline', 'pipe',
        'pretty',  'psql',  
        'orgtbl', 'jira', 'textile', 'html', 'latex' )


.. note::
    
    * We provide, all device types commands column wise for all model devices
    * Script identifies device type ``Cisco/Juniper/Arista`` and push appropriate list of commands to respective device.
    * Imp: This methods always implement output captures in append mode. So beware of capture locations if any already contains previous captures.



.. Tip::

    #. Multiple devices can be inserted on a single excel tab.
    #. A device can appear on multiple tabs as well. Respective all tab commands will be captured one by one.
    #. Grouping
        #. Create separate group of commands based on device functionality (as mentioned in sample template attached). 
        #. Add group of devices to each necessary tabs based on device functionality.  


A Sample Excel
------------------------------------------

:download:`Sample Excel <files/devices_cmds.xlsx>`. Sample excel template file used in above example.



-----------------------

Watch out for the terminal if any errors and see your output in given output path.



