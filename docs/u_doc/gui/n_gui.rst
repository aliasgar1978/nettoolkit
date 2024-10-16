
NGui Explained
============================================

You can use the NGui class to do GUI stuff for you. 

   * Declare some variables and frames. Attach those to appropriate structure and boom!!!  NGui interface will be ready for you.
   * Modify as you need to change the appearance. 
   * Bind appropriate methods to run the tasks when an event is called. 


.. figure:: files/NGui.png
   :scale: 25%
   :alt: Nettoolkit
   :align: right


* Follow Below steps in order to create your own GUI Frames in Python using Nettoolkit interface hooks.
* Backend Credit: ``PySimpleGUI``


#. Define a few functions which will return Frames.

    .. code-block:: python

        # -----------------------------------------------------------------------------------
        #  Import form items from nettoolkit
        # -----------------------------------------------------------------------------------
        from nettoolkit.nettoolkit.forms.formitems import *

        # -----------------------------------------------------------------------------------
        #  Define all your frames here 
        # -----------------------------------------------------------------------------------

        ## This is frame 1 of group1 
        def group1_frame1():
            return sg.Frame(title=None, 
                            relief=sg.RELIEF_SUNKEN, 
                            layout=[

                [sg.Text('Group1 - Frame1 Contents and your frame items will go here...'),],
                under_line(80),
                [sg.Button("Click to run", change_submits=True, key='btn1')],
                under_line(80),
                ])


        ## This is frame 2 of group1 
        def group1_frame2():
            return sg.Frame(title=None, 
                            relief=sg.RELIEF_SUNKEN, 
                            layout=[

                [sg.Text('Group1 - Frame2 Contents and your frame items will go here...'),],
                under_line(80),
                [sg.Checkbox('Event which trigger some field update', key='cb1', change_submits=True)],
                [sg.Text("Field which will be updated by below trigger"),sg.InputText(key='txt1')],
                under_line(80),
                ])

        ## This is frame 1 of group2 
        def group2_frame1():
            return sg.Frame(title=None, 
                            relief=sg.RELIEF_SUNKEN, 
                            layout=[

                [sg.Text('Group2 Contents and your frame items will go here...'),],
                under_line(80),
                [sg.Button("Click to run", change_submits=True, key='btn2')],
                under_line(80),
                ])


        ## ... Define more as needed

#.  Now pick EVENT_UPDATORS, EVENT_ITEM_UPDATORS, RETRACTABLES outof these.

    * EVENT_UPDATORS: keys which will trigger an event function.
    * EVENT_ITEM_UPDATORS: keys which will trigger and event function which results change in a form object.
    * RETRACTABLES: keys which values needs to be cleaned up when "Clean" button pressed. 

    .. code-block:: python

        # ---------------------------------- #
        #         EVENT UPDATERS             #
        # ---------------------------------- #

        # ---------------------------------------------------------------------------------------
        #   list down variables which triggers an event function call -- exec_fn(i)
        # ---------------------------------------------------------------------------------------
        EVENT_UPDATERS1 = { 'cb1'}
        EVENT_UPDATERS2 = set()

        # --------------------------------- [ Club ] --------------------------------------------
        EVENT_UPDATORS = set()
        EVENT_UPDATORS = EVENT_UPDATORS.union(EVENT_UPDATERS1)
        EVENT_UPDATORS = EVENT_UPDATORS.union(EVENT_UPDATERS2)
        # ---------------------------------------------------------------------------------------

        # --------------------------------------- #
        #         EVENT ITEM UPDATERS             #
        # --------------------------------------- #

        # ---------------------------------------------------------------------------------------
        #   list down variables which triggers an item update event function -- exec_fn(obj, i)
        # ---------------------------------------------------------------------------------------
        EVENT_ITEM_UPDATORS = set()


        # ---------------------------------- #
        #        RETRACTABLE KEYS            #
        # ---------------------------------- #

        # ---------------------------------------------------------------------------------------
        #  sets of retractable variables , which should be cleared up on clicking clear button
        # ---------------------------------------------------------------------------------------
        G1_RETRACTABLES = set()
        G2_RETRACTABLES = { 'txt1', }

        # --------------------------------- [ Club ] --------------------------------------------
        RETRACTABLES = set()
        RETRACTABLES = RETRACTABLES.union(G1_RETRACTABLES)
        RETRACTABLES = RETRACTABLES.union(G2_RETRACTABLES)
        # -------------------------------------------------------------------------


#. Set Button Pallete, to differenciate the Frames between button clicks.

    .. code-block:: python

        # ---------------------------------------------------------------------------------------
        #  Necessary Project imports
        # ---------------------------------------------------------------------------------------
        from collections import OrderedDict

        # ---------------------------------------------------------------------------------------
        #  Create Frame groups and ascociate frame descriptions for each frames definition to it
        # ---------------------------------------------------------------------------------------
        GROUP1_FRAME = {
            'G1_Frame1_Description': group1_frame1(),
            'G1_Frame2_Description': group1_frame2(),
        }
        GROUP2_FRAME = {
            'G2_Frame1_Description': group2_frame1()
        }
        # ... Add more Frame_Groups as necessary

        # ---------------------------------------------------------------------------------------
        #   Creating 'Buttons' and ascociate each with a group name
        # ---------------------------------------------------------------------------------------
        BUTTUN_PALLETE_DIC = OrderedDict()
        BUTTUN_PALLETE_DIC["btn_grp_1"] = {'key': 'btn1',  'frames': GROUP1_FRAME,  "button_name": "Group1 Frames"}
        BUTTUN_PALLETE_DIC["btn_grp_2"] = {'key': 'btn2',  'frames': GROUP2_FRAME,  "button_name": "Group2 Frames"}
        # ... Add more buttons as necessary

#. Event Functions.

Here are few **EVENT_UPDATORS** functions and **EVENT_ITEM_UPDATORS** functions.

    .. code-block:: python

        # ================================================================================
        #  // EVENT_ITEM_UPDATORS //
        #    these functions will accept two arguments. first is NGui object iself and
        #    second will be [i] item list of object
        # ================================================================================

        def g1_f2_cb1_executor(obj, i):
            s = "You have presesed a button from Group 1 Frame 2, text box value will be append with X"
            print(s)
            new_text = i['txt1'] + "X"
            obj.event_update_element(txt1={'value': new_text})		

        # ================================================================================
        #  // EVENT_UPDATORS //
        #   Such functions will accept only [i] item list of NGui object. 
        # ================================================================================

        def g1_f1_btn1_executor(i):
            ## Your execution code will reside here ##
            s = "You have presesed a button from Group 1 Frame 1"
            print(s)
            sg.Popup(s)

        def g2_f1_btn2_executor(i):
            ## Your execution code will reside here ##
            s = "You have presesed a button from Group 2 Frame 1"
            print(s)
            sg.Popup(s)

        #  // Tie all these functions together to appropriate keys of Frames //

        EVENT_FUNCTIONS = {
            'cb1' : g1_f2_cb1_executor,
            'btn1': g1_f1_btn1_executor,
            'btn2': g2_f1_btn2_executor,
        }

#. We are all set, Get Ready For The Show. Its time to tie all above together.

    .. code-block:: python

        # --------------------------------------------
        # IMPORT NGui
        # --------------------------------------------
        from nettoolkit import NGui

        # ----------------------------------------------------------------------------------
        #  Create an Instance of NGui
        #  Options can be sent while object initialization or can be set as propery as well 
        #  after instance is created. 
        # ----------------------------------------------------------------------------------
        NG = NGui(
            header = "My Custom Project - X",
            banner = "Project X - Which does something",
            form_width = 800,
            form_height = 400,
            event_updaters      = EVENT_UPDATORS,
            event_item_updaters = EVENT_ITEM_UPDATORS,
            retractables        = RETRACTABLES,
            event_catchers      = EVENT_FUNCTIONS,
            button_pallete_dic  = BUTTUN_PALLETE_DIC,
        )

        # ----------------------------------------------------------------------------------
        #  Optional: Define maximum Buttons in a row in button pallete. (if more buttons)
        # ----------------------------------------------------------------------------------
        NG.max_buttons_in_a_row = 6

        # ----------------------------------------------------------------------------------
        #  Call for an instance, by providing optional initial frame group definition
        #  no initial frame group will show all frames at initialization
        # ----------------------------------------------------------------------------------
        NG('btn_grp_1')



.. important::
    
    **Parameters for NGui**

    * ``header`` **(string)** Header for the window (default: None)
    * ``banner`` **(string)** Banner to display in window (default: None)
    * ``form_width`` **(integer)** Form width (default: 700)
    * ``form_height`` **(integer)** Form Height (default: 1440)
    * ``event_updaters`` **(set)** Set of event updator element keys (default: None)
    * ``event_item_updaters`` **(set)** Set of event item updator element keys (default: None)
    * ``retractables`` **(set)** Set of element keys which can be cleanup when pressing clean button.
    * ``event_catchers`` **(set)** Dictionary of event function keys and its respective functions (default: None)
    * ``button_pallete_dic`` **(dict)** Dictionary which defines Button pallete buttons ( Default: None )

    * ``max_buttons_in_a_row`` **(int)** maximum Buttons in a row in button pallete. (if more buttons)


.. note::
    
    **Parameters for NGui**

    * All these arguments are optionals to declare whilst creating the object instance. And can be later define  by propery assignment ( ex: **NG.header = "Some header"** ).
    * Although all of these are optionals to declare at beginning, some of the arguments are required ones to provide before calling the NGui class in order to work properly.. 
    * If you call NGui, without providing ``button_pallete_dic`` . GUI will rendered with all frames with no buttons on button pallete.
    * Calling NGui without any initial button key or wrong button key; renders all frames while loading new window.

------

**@Decorator popupmsg()**

* ``pre`` **(str, optional)**: Popup Message to display before function execution. Defaults to None.
* ``post`` **(str, optional)**: Popup Message to display after function execution. Defaults to None.

.. code-block:: python

    from nettoolkit.nettoolkit.forms.formitems import popupmsg

    @popupmsg(pre="Popup msg before bfunction run", 
                post="Popup msg after function run")
    def foo():
        pass




