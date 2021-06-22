==================
Run Scale as Class
==================

.. figure:: ../figures/11horiz_scale_class.png
    :align: center
    :width: 493
    :height: 101
    :alt: horizontal scale from class
    
    Horizontal ttk Scale as class
    
    Slider shown at maximum travel on a 0 to 100 range.

In order to load an external module the script needs to be either a function 
or class, class suits our needs better because we can use inheritance and 
the script can use more than one method. Base the class on the 
10ttk_range_calibrate.py calibration script. This changes the Scale length
by first estimating the range size, rather than change the window size and
adjusting the Scale length that way.

Inheritance from ttk Scale
--------------------------

All the existing options available on the ttk Scale become available, without
extra programming. Any options with their default values need to be
in the normal list that follows the __init__ statement, then repeated  
as a self variable. The super statement repeats all the ttk variables, after 
the super statement equate the remaining variables to self variables::

    class  TtkScale(Scale):
        def __init__(self, parent, length, from_=0, to=255, orient='horizontal',
                    variable=0, digits=None, tickinterval=None, sliderlength=32,
                    command=None, style=None, showvalue=True, resolution=1):

        self.from_ = from_
        self.to = to
        self.variable = variable
        self.length = length
        self.command = command
        self.parent = parent

        super().__init__(parent, length=length, from_=from_, to=to, orient=orient,
                        variable=variable, command=command, style=style)

        self.digits = digits
        self.tickinterval = tickinterval
        self.showvalue = showvalue
        self.resolution = resolution
        self.sliderlength = sliderlength

When determining the cursor position for ``resolution`` it is easier to work 
in actual ``x`` position rather than a relative position, so add a 
conversion method. Base it on convert_to_relx, just multiply rel_max and 
rel_min by the Scale length len_val.

There were no other major changes compared to the calibration script other 
than changing over to a class.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 11ttk_horiz_scale_class.py

    .. literalinclude:: ../examples/scale/11ttk_horiz_scale_class.py