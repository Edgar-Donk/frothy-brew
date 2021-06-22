====================
Moving Current Value
====================

The tkinter Scale has the ability to display a moving Label with the current
scale value. One might think of a Canvas with a moving value, but we shall 
use an ordinary Label positioned according to the ``place`` layout manager.
Assume that we can obtain the current Scale value. The main unknown is the 
position of the display Label for any given Scale output, this should 
correspond to the centre
of the slider offset to be above the Scale. Since we already know ``rel_min``
and ``rel_max`` it should be easy to calculate.

Just as with the
range values use a relative ``x`` value. As the cursor moves so the current 
value in the display value should change - you can always see what is 
required by moving the tkinter Scale. We could link the display label through
a tkinter variable, but without special programming the display would show
a float number with umpteen decimal places. To keep the display label 
updated use the ``command`` option on the
Scale, this calls up a function that calculates the relative ``x`` and 
simultaneously sets the display labels position and actual display value. 
Every slider movement triggers the function, so a continuously moving and 
changing display results. Link the SpinBox and
Scale through a tkinter variable, then adjust the Spinbox's size to limit the
its display. 

A simple function is used to calculate the relative x position::

    def convert_to_relx(curr_val):
        return ((curr_val - from_val) * (rel_max - rel_min) / (to_val - from_val) \
            + rel_min)

Another function changes the display label::

    def display_value(value):
        rel_x = convert_to_relx(float(value))
        disp_lab.place_configure(relx=rel_x)
        disp_lab.configure(text=f'{float(value):.{dig_val}f}')

.. note:: There are several methods to format text, the latest configuration 
    for Python 3.6 and above is the preferred method. Value (Scale actual 
    value) needs to be converted to a float. The ``digits`` option, dig_val 
    is related to the number of decimal places shown. As we are replacing
    a number in the float format the variable ``dig_val`` is placed in curly
    brackets.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 07ttk_tkinter_shift_value.py

    .. literalinclude:: ../examples/scale/07ttk_tkinter_shift_value.py
        :emphasize-lines: 17, 36-38, 40-45, 47-48, 50-51, 53, 67, 70-73, 75-77