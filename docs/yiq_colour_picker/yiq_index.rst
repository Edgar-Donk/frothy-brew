=====================
RGB YIQ Colour Picker
=====================

Following on from the HSV colour picker we can make a YIQ colour picker.
In principle YIQ and YUV have similar methods, but we probably would run
into trouble with any of the LAB colour systems. As we saw the main problem
is how long it takes to draw a gradient and LAB calculations are more involved,
whereas YIQ and YUV have simple conversions to and from RGB. 

Just as in the previous section these scripts are DPI aware, but if your
monitor is not 96 or 192dpi then run the script to generate the colour space
:ref:`02yiq_colour_space.py<colour-space>`.

.. toctree::
    :caption: YIQ Colour Picker...
    :maxdepth: 1
   
    make_yiq_picker
    adding_colour_space
    combining_rgb_yiq
    related_colours