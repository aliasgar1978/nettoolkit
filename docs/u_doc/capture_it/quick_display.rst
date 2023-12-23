

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



