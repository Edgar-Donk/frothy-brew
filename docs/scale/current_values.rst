========================
Current Value ttk.Scales
========================

Command Option
--------------

.. figure:: ../figures/02ttk_tkinter_scale_value.png
    :align: center
    :width: 297
    :height: 425
    :alt: Adding current value to  horizontal and vertical Scales in ttk
    
    Adding Current Value
    
    Using ``command`` to show current values.

Some parts of these scripts are common to both vertical and horizontal scales.

The example 01ttk_tkinter.py can be used as a basis with which to start. The 
most obvious shortcoming is that there is no value shown for the cursor 
position. Use the method ``get()`` to obtain this value and place it in a
Label. The problem with this method is that as it stands it only gives the 
first position of the cursor. If a button is used to query the scale then
the current cursor position will be shown. Compared to the tkinter option
this method is not dynamic enough. Our problem lies with the command sequence,
so get() is doing its job, but the Scale needs to be first redrawn then the 
Label text updated before ``get()`` returns the correct answer. We can use 
the ``command`` option, then update the Label from the relevant function.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 02ttk_tkinter_value.py

    .. literalinclude:: ../examples/scale/02ttk_tkinter_value.py
        :emphasize-lines: 4-5, 7-8, 27, 33

The simplest method of displaying the current value is to place the result in
a Label. Later on in Colour Picker a Spinbox is used, which allows the slider
to position itself according to the Spinbox entry and not just positioned by
the cursor, in this case a FloatVar or IntVar is used. It is also possible 
to position the current value just above the slider.

Bind to Mouse Button
--------------------

There may be occasions when the ``command`` option is required for other 
actions than showing the current value. In this case bind to the mouse cursor
the result is much the same as with command. The bind can be when the mouse
is pressed or preferably when the mouse is released while using the method 
``get()``. This is because when clicking on the slider it normally is not in
the position we are interested in, when the mouse is released the slider is
in position and the value obtained by ``get()`` is more pertinent. This is 
still not as dynamic as the tkinter option and will be addressed later.

When binding we can pick up the current x-position of the cursor, note the
x-position values at the two extremes. The vertical scale shows the current
y-position. Remember the bind gives the actual position for the cursor 
rather than the centre of the slider.


.. container:: toggle

    .. container:: header

        *Show/Hide Code* 03ttk_tkinter_bind.py

    .. literalinclude:: ../examples/scale/03ttk_tkinter_bind.py
        :emphasize-lines: 6, 10, 29-30, 36-37