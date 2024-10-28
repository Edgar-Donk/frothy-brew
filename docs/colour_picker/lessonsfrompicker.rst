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
a good candidate, it should follow a similar method to hsv. Whatever colour 
scheme is chosen it would be a good idea to 
include rgb since that is the base for displaying colour on the monitor.

Printing in CMYK
================

Printing operates in CMYK is a subtractive system so whereas (255, 255, 255) 
in RGB gives white,
a combination of CMY produces a dark grey approaching black, hence the
need for the black - quite apart from reduced cost it gives a better rendition
of darker colours. Printers designed for photographic output will have
additional inks, probably a photographic black and grey cartridge - so six
inks in all. Unless you have access to a good printer the results could be 
disappointing because printers render a different colour range. 

Generally rather than converting pixels we require image conversion to 
preview the results before printing. The problem is that the result will be
displayed in RGB at our computer and the CMYK rendition will at best be a
good approximation, which may or may not show all the problems. A good image
from the camera will carry its own embedded colour profile, so this is
required for commercial printing. 

At home always test the result on the printer - try out photographic paper -
but also be prepared to use good quality matt paper. Calibrate all the 
hardware especially the monitor, do not expect that results can be easily
duplicated on different printers, or even the same printer at different
times. If all else fails use the chain chemist's photographic printers,
rather than investing in a rarely used expensive printer.
