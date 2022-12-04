=================
Starting with HSV
=================

Using paint.net as our guide the hsv part consists of 3 colour gradients,
similar to their rgb part, but there will be a colour wheel which will be
directly linked to the hsv part. Apart from the colour wheel it should be
similar to the widgets already used for rgb.

Determining HSV Gradients
=========================

Using a similar process to that for rgb create our 
gradients. Before starting note that we have dissimilar ranges. Hue starts 
at 0 and finishes at 360, whilst saturation and value both start and finish 
at 0 and 100 respectively. When saturation or value change the hue gradient 
remains unaltered. As hue changes from 0 to 360, if both saturation and value 
are at 100, their final colour follows the hue colour. Saturation 
starts from white whereas value starts from black. Altering saturation or 
value has no effect on their own gradient, but they do affect the other 
component. When saturation and value are at 0 any change in hue has no 
effect, as we are at black. In fact Saturation stays black whenever its value is 
0, no matter what value hue or saturation have. Value changes from white to 
black when saturation is 0.

.. figure :: ../figures/red_hsv.webp
    :width: 173
    :height: 125
    :alt: red hsv in paint.net
    :align: center

    Full red at 100% saturation and 100% value

Hue is straightforward, it always is the same so no gradient change, we only 
have to generate it at
initialisation. When saturation and value are both 100 we see that hue at 0 
corresponds to red #ff0000 as does hue at 360. When hue is moved and 
saturation and value are both 100 one or more rgb components are always at 255.

.. figure :: ../figures/white_hsv.webp
    :width: 170
    :height: 125
    :alt: white hsv in paint.net
    :align: center

    White at 0% saturation and 100% value

.. figure :: ../figures/black_hsv.webp
    :width: 173
    :height: 125
    :alt: black hsv in paint.net 0% saturation 0% value
    :align: center
    
    Black at 0% saturation and 0% value

.. figure :: ../figures/black_100s.webp
    :width: 173
    :height: 124
    :alt: black hsv in paint.net 100% saturation 0% value
    :align: center
    
    Black at 100% saturation and 0% value

.. figure :: ../figures/hsv_50_50.webp
    :width: 171
    :height: 122
    :alt: brown hsv in paint.net 50% saturation 50% value
    :align: center

    Brown at 50% saturation and 50% value
    
Using similar analogies developed from rgb, we can deduce that the saturation
gradient is influenced by both hue and value in the manner that the start
colour is (h,0,v) and finishes at (h,100,v). Likewise the value gradient
can be drawn from (h,v,0) finishing at (h,v,100).

Converting HSV to RGB and Back Again
------------------------------------

If we were being pedantic our upper limits would be 359 and 99, rather than
360 and 100.

Using the conversions, as found in colorsys, only the converted start 
and finish values are required to make the gradient in rgb.
That means intermediate values need not be converted from hsv to hash. 
The conversions are made with normalised values (0 to 1) therefore it is 
useful to include normalisation and denormalisation at the input and 
output in our function.

Working with the Validation
---------------------------

When working with spinbox entry areas there is a similar situation to just
plain entry, but when these are linked to tk variables additional constraints
are created. Firstly even though we can have an empty entry that continues to
validate, the tk variable will raise an error if we are using an IntVar or
DoubleVar. Also the output of a themed Scale is not restrained to produce
integers. Some seat of the pants changes are required to prevent errors, so
do not allow an empty entry part, changes have to be made with a part entry 
input which can be prefixed as necessary.

When validating use the current input, rather than the text if we can. This
prevents a completely empty editing area.

It would be better if the upper size limit is imported and reuse the 
validation code, since all the code is otherwise exactly the same. This has
been done by inserting the upper limit in the spinbox call to the register
function. The validate command accepts just the number, but cannot have 
an attribute such as ``upper=360``.

After all that we should have a script that looks like 02all3colours.py.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 08basichsv.py

    .. literalinclude:: ../examples/colours/08basichsv.py

.. figure :: ../figures/basic_hsv.webp
    :width: 459
    :height: 280
    :alt: hsv in tkinter three gradients
    :align: center

    The basic hsv colour picker
