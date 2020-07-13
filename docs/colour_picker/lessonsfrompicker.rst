====================
Colour Picker Wrapup
====================

When running an application with many changes in real time it is important
that the changes are carried out in the fastest way. 

The following were new to me:-

#. Working with arrays to produce gradients and chequered output
#. Save arrays as PPM files then directly import into tkinter
#. Emulating alpha changes on RGB files (no alpha channel)
#. Writing range values for Scale adjusted to scale width and cursor width
#. Controlling cursor movement in a canvas
#. Gradient changes for the colour components
#. Expanding a widget containing an image

Say we wish to have different colour schemes other than hsv, then hsl is 
a good candidate. Whatever colour scheme is chosen it would be a good idea to 
include rgb since that is the base for displaying colour on the monitor.