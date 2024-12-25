

Execution Steps - Quick Show Output
=================================================


#. Import the necessary function from module::

    from netoolkit.capture_it import quick_display


#. Set Authentication Parameters (Format=dictionary)::

    auth = {
        'un':'provide username' , 
        'pw':'provide login password', 
        'en':'provide enable password'  
    }
    ## Make sure to use static passwords. Refrain using OTP, as ID may get locked due to multiple simultaneous login.


#. Provide Device ip (Format=string)::

    ip = '192.168.100.1'


#. Command(s) to capture (valid Formats=string,list,tuple,set)::

    # Option 1:  Provide the a single show command
    cmds = 'show version'

    # Option 2:  Provide a list/set of show commands (if multiple)
    cmds = ['show version', 'show lldp neighbor']


#. Start::

    quick_display(ip=ip, auth=auth, cmds=cmds, wait=1)    ## wait argument (integer), number of seconds


.. important::
    
    **Parameters**

    * ``ip``  ip address of device (str)
    * ``auth``  authentication Parameters (dict)
    * ``cmds``  list of commands (str, iterable).
    * ``wait``  number of seconds to be wait before reading output stream. (increase value if output is lengthy) ( default=3 seconds )



get_op()
~~~~~~~~~~~

    * reads the provided log file and retuns matching command output from file
    * filters the command output from given captured file.
    * logs to be captured using capture-it utility from nettoolkit.

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import get_op
        >>> get_op(file="capture.log", cmd='show cdp neighbor')
        output of command.


get_ops()
~~~~~~~~~~~

    * reads the provided log file and retuns matching commands outputs from file
    * filters the commands outputs from given captured file.
    * logs to be captured using capture-it utility from nettoolkit.

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import get_ops
        >>> get_ops(file="capture.log", cmd_startswith='show cdp neighbor')
        output of commands.

get_device_manufacturar()
~~~~~~~~~~~~~~~~~~~~~~~~~~

    * finds out manufacturer (cisco/juniper) from given capture file.
    * in case if not found, it will return as Unidentified.

    .. code-block:: python

        >>> from nettoolkit.nettoolkit_common import get_device_manufacturar
        >>> get_device_manufacturar(file="capture.log")
        "Cisco"

