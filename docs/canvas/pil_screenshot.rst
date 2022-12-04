==============
PIL Screenshot
==============

Run the tkinter canvas script, then when all is as should be take a screenshot
using PIL ``ImageGrab.grab``. The default is the entire screen, so one 
normally needs to define the area of the tkinter canvas in **bbox**. 
For windows machines it is better
to set the option **include_layered_windows=False** otherwise spurious layers 
may intrude.

bbox is a tuple of the pixel coordinates of the left upper and right lower
corners. To be certain that the containing box only includes the canvas and 
not the tkinter window manager decorations switch them off during the 
drawing build and capture using **root.overrideredirect(1)**, then restore them. 

.. figure:: ../images/canvas/test_circle_tk.png
    :width: 600px
    :height: 600px

    The image grabbed with PIL

.. container:: toggle

    .. container:: header

        *Show/Hide Code* test_circle_tk.py

    .. literalinclude:: ../examples/canvas/grab_circle_tk.py

The procedure is not absolutely straightforward, and many examples on the
internet capture the wrong area.