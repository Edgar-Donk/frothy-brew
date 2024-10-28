====================
Adjusting the Window
====================

.. figure:: ../figures/08too_small.png
    :align: center
    :width: 594
    :height: 298
    :alt: length input too small
    
    Before the length is adjusted
    
    Using adjustable window size.


If we properly select the layout manager options then the Scale will change
its length as the window size is altered. Check what happens when the window
is expanded sideways. The displayed value seems to react reasonably, but the
range values do not adjust so well, in particular look at the highest and
lowest values, as the window expands so the placement becomes less accurate.
We need to sense that the window size is changing and redraw the range with
new length sizes. If the length is adjusted from the script then our current
calculations are good enough.

If we bind to the event ``Configure`` this seems to fit the bill.

* Configure

    The user changed the size of a widget, for example by dragging a corner 
    or side of the window.

As the slider moves only the displayed value changes, whereas when the window
is adjusted both the displayed value and the range values change in position. 
If the changes are made without a dwell time anywhere the previous values are 
overwritten and do not stay on the screen, however if there is a dwell time
between the movement and new writing then the old value remains.

.. figure:: ../figures/08adjusted.png
    :align: center
    :width: 971
    :height: 298
    :alt: length adjusted by window sizing
    
    After the length is adjusted
    
    Using adjustable window size and binding to configure.

The Scale length is altered by the window sizing, all other values remain 
constant, so when recalculating the new Scale length must be found::

    len_val = scth['length']

or::

    len_val = scth.cget(length)

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 08ttk_tkinter_update_size.py

    .. literalinclude:: ../examples/scale/08ttk_tkinter_update_size.py
        :emphasize-lines: 20-27, 29-31, 38-39, 51, 61, 66-68, 70, 73, 82, 87,
                            92, 94
