==============
Special Ranges
==============

When using a range such as -1 to 1 then expect the ``range`` in the 
``for`` loop to give an error. This can be solved by using numpy ``arange``.
The relative positions of the minimum and maximum tick values can be made 
into variables::

    rel_min = ((slider_val - from_size) / 2 + bw_val) / len_val
    rel_max = 1 - ((slider_val - to_size) / 2 - bw_val) / len_val

Create a numpy array of the data in our range::

    data = np.arange(from_val, to_val+tick_val, tick_val)

the construction is similar to the range. To ensure the maximum
value is included add the tick value to the ``to_val``. As the data is 
an array of floats round the values, then convert to a tuple::

    data = np.round(data,1)
    range_vals = tuple(data)
    len_rvs = len(range_vals)

numpy ``round`` does not round to the floor but rounds to the nearest digit. 

The tick placement was changed slightly to accomodate the negative values
and small tick intervals::

    for i, rv in enumerate(range_vals):
        item = ttk.Label(root, text=rv)
        item.place(in_=scth, bordermode='outside',
                relx=(rel_min + i / (len_rvs - 1) * (rel_max - rel_min)) ,
                rely=1, anchor='n')

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 06ttk_tkinter_range.py

    .. literalinclude:: ../examples/scale/06ttk_tkinter_range.py
        :emphasize-lines: 2, 4, 13-14, 21, 25-27, 41-42, 44-52, 54