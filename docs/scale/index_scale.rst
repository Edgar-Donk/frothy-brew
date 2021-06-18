=========
ttk Scale
=========

It is noticeable that the ttk Scale has fewer attributes than its tkinter
mate, and some of these missing attributes are useful for everyday use, on
top of this there is no straightforward substitute in ttk Style. To obtain 
an equivalent ttk to tkinter scale one must use fairly complicated scripts,
or find a workable script after searching the web.

If you do not require a scale with an annotated start and finish then the
existing ttk scale suffices, but if you wish to have an annotated scale then
use the tkinter scale but then the scale will probably look out of place
compared to the other widgets unless tkinter is used throughout. If you 
require a theme with an annotated scale, then the following chapters will be
of interest.  

.. toctree::
   :caption: Annotated ttk Scale...
   :maxdepth: 1
   
   comparison_scales
   horizontal_scale
   vertical_scale