===============
Automatic Range
===============

Two aids in the script help in automating any range changes. In the first 
an inline if clause is used where the numpy arange function, either adds 
``1`` to the ``to_val`` (to) or if the ``tick_val`` (tickinterval) is less 
than 1 then adds tick_val to the to_val::

    data = np.arange(from_val, (to_val+1 if tick_val >=1 else to_val+tick_val), tick_val)

The second is more complicated, in most ranges 
both the ``from`` and ``to`` range values are shown, but in the case of 0 to 
255, as used in RGB displays, the highest value ``to`` is not usually 
displayed, as the Scale becomes too long if tick intervals are smaller than
10 or 20. The slider's maximum position will be at the ``to`` value, with its
actual display value. On the other hand the highest range value shown will 
be the second to last in our range 
of values and its ``x`` position will be correspondingly less than the 
slider's maximum position.

In all cases the ``from`` value (x_min) is shown, so no change is required here,
only the x_max or the position of the last displayed tick has to change::

    if range_vals[-1] == to_val:
        pass 
    else:
        max_rv = range_vals[-1]
        mult_x = ((max_rv-from_val)*x_max/(to_val-from_val))

The actual value position uses the relative x computation uses an actual x
placement, which helps in calibration::

    x=(x_min + i / (len_rvs - 1) *
        ((x_max if range_vals[-1] == to_val else mult_x) - x_min)),

Both these changes are already in the calibration script.