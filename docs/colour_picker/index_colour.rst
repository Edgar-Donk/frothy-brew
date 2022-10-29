=================
Colour Picker App
=================

While there are a load of rgbahsv colour pickers out there it is still  
useful to make one.

Let's use the colour picker in paint.net as an example, and keep it simple
at the start, use the canvas to display our gradient, then use a scale 
underneath the canvas and a spinbox to show the value of the scale. If both 
the scale and its associated spinbox point to the same tk variable they 
should affect each other. At the same time the gradient should change with the 
value on with each colour component.

In case you are wondering the following scripts are DPI aware, so they have
an enlargement factor included, and will operate at 96dpi and 192dpi equally 
well, for larger dpi remember to run the colour wheel script 
:ref:`09colour_wheel_pil.py<colour-wheel>`.

.. toctree::
    :caption: Colour Picker...
    :maxdepth: 1
   
    deducing_the_gradients
    using_tkinter_widgets
    adding_alpha_result
    modifying_scales_and_entry
    starting_hsv
    adding_colour_wheel
    creating_cursor_colour_wheel
    cursor_interaction
    joining_rgb_hsv
    lessonsfrompicker