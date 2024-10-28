===============
Related Colours
===============

.. figure :: ../figures/yiq_related.webp
    :width: 501
    :height: 333 
    :alt: combined rgb and yiq with related colours 
    :align: center
    
    Combined RGB and YIQ with Related Colours 

No matter where we are on the spectrum it is easy to calculate related 
colours using YIQ. Just keep the hue constant that is the I and Q 
components, then adjust the luma Y and read off the related colour. The 
complementary colour is not much more complicated, multiply the I and Q 
values by -1 and take away the luma from 100.

Something similar can be done in HSV. Related colours have the same 
hue, so adjusting saturation and value gave the related colours. Often
it is obvious, especially when dealing with fully saturated and 100% value,
in these cases saturation starts at white and finishes with our colour mix 
while value starts at black and finishes with our colour mix. 

However try with brown and it is a different story. With a hash value of
#7f3f3f, hue sits at 0 and both saturation and value are both 50. Are 
related colours found by changing saturation or value, or both?
With YIQ there is no such ambiguity. Keeping I and Q constant (equivalent to
hue constant in HSV) change the luma and the related colours do not change.

Resizing
--------

Resize along similar lines to RGB and HSV, but now use
a single resize function, where the name of the Canvas is included in
our bind call. Special provision is made using the ``partial`` method fron
the package ``functools``. Depending on the Canvas name so the appropriate
gradient is redrawn with a new width. The actual values of the colour 
components need to be found before the gradients are drawn. Just as before
update the default Canvas width, otherwise once the resizing is 
complete any cursor movement could result in wrongly sized gradients.

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 05relatedyiqlist.py

    .. literalinclude:: ../examples/yiq/05relatedyiqlist.py
