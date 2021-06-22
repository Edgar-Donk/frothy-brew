====================
Calculate the Length
====================

.. figure:: ../figures/09est_length.png
    :align: center
    :width: 1144
    :height: 267
    :alt: length estimated by script
    
    Script estimates size

There is an alternative to adjusting the Scale length until after it is drawn 
then changing the window size. Estimate the required length,  
use the range values, measure each 
range value then allow for the empty space between ticks (width
of a zero)::

    data = np.arange(from_val, to_val+tick_val, tick_val)
    data = np.round(data,1)
    range_vals = tuple(data)
    
    vals_size = def_font.measure(str(i)) for i in range_vals]
    data_size = sum(vals_size)
    
    len_rvs = len(range_vals)
    space_size = len_rvs * def_font.measure('0')
    
    min_len = int(ceil((data_size+space_size) / 50.0)) * 50

This code needs to be positioned before the Scale length (len_val) is used 
for calculation.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 09ttk_tkinter_estimate_size.py

    .. literalinclude:: ../examples/scale/09ttk_tkinter_estimate_size.py
        :emphasize-lines: 13, 31-35, 37-42, 49, 57, 60, 79, 84-85, 94, 96, 101
