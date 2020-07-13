======================
Combining RGB with YIQ
======================

.. figure:: ../figures/rgb_yiq_mod.webp
    :width: 407
    :height: 268
    :alt: rgb and yiq colour schemes combined modified labels
    :align: center
    
    RGB and YIQ Combined

Going along the same pathline as for hsv, we can now add the rgb colour
system, then tie the two parts together. So in essence add 07entryscalemod
to 03yiqspaceadded to make 04rgbandyiq, removing duplicate files and 
renaming sb_okay and its references in the yiq part.

Check that the layout is correct, adjust the LabelFrame references and grid
layout for opacity. Now add the function overlord, copied from 12rgbandhsv
changing the references to hsv as we go. Add the function rgb_to_yiq. All
the handles require a reference to overlord. Test that all these work, now
add references in the handles for I and Q and overlord to the colour space, 
so the cursor moves when the scales are adjusted::

    X=i*3/2+150
    Y=q*3/2+150
    ringR=self.ringR
    for s in self.canYiq.find_withtag("ring"):
        self.canYiq.coords(s,X-ringR,Y-ringR,X+ringR,Y+ringR)

Whoops - forgot to change the labels to themed ones, delete the references 
to background and height.

.. figure:: ../figures/rgb_yiq.webp
    :width: 413
    :height: 270
    :alt: rgb and yiq colour schemes combined
    :align: center
    
    RGB and YIQ Combined 

There are one or two advantages that yiq/yuv has over rgb and hsv, we can
optically get an accurate grey just by selecting the Y component(I and Q 
both 0), further the complementary colour is -1.0 times the I and Q 
components, and Y is 100-Y. For general purposes YIQ is easier to understand 
what is going on than with most other colour systems. 

In principle we can use the same method for YUV, but we probably would run
into trouble with any of the LAB colour systems. As we saw the main problem
is how long it takes to draw a gradient. By sticking to the RGB gradient we
have all the speed advantages and can use straight python.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 04rgbandyiqlist.py

    .. literalinclude:: ../examples/yiq/04rgbandyiqlist.py

Modifying Tick Intervals
------------------------

Using our original algorithm most of the scale tick values sit reasonably 
well together with the gradients but the Y (luma) scale starts too late
and finishes too early. Change the tickinterval placing by changing the first
component to a quarter of the slider length and the final component to half
the slider length. Overall the tick values look better with this change. 

