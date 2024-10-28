==========
Resolution
==========

The resolution affects how the cursor moves if the Scale is clicked in the
trough either before or after the slider. The default value is 1 pixel, even
when the range is running from -1 to 1 with 0.1 tickintervals where a smaller
resolution would be appropriate. However with
higher ranges the resolution can be changed. Whilst setting the resolution 
it is found that when an amount is added to the Scale that the actual value 
is overstepped by 1 pixel. Likewise when an amount is subtracted from the 
Scale's actual value it understeps by 1 pixel.

To work resolution bind the ttk Scale to the left mouse button. Ignore the 
calculations if the resolution or tickinterval is less than 1. Only work 
with mouse clicks in the trough, ignore those on the slider itself::

    scth.bind("<Button-1>", resolve)
    
    def resolve(evt):
        if res_val < 1 or tick_val < 1:
            pass
        else:
            value = scth.get()
            curr_x = convert_to_actx(value)
            if evt.x < curr_x - slider_val / 2:
                scth.set(value - res_val + 1)
            elif evt.x > curr_x + slider_val / 2:
                scth.set(value + res_val - 1)