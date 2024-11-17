========================
Monitor Resolution - DPI
========================

.. figure:: ../figures/01two_buttons_combined.jpg
    :width: 753
    :height: 315
    :align: center
    :alt: Tkinter buttons
    
    tkinter buttons, same sizes differing highlight and shadow

Not many scripts make allowance for the different monitor resolutions (dots
per inch or DPI), as a consequence, in particular older scripts, look good 
when run at 96dpi but look too small when run at higher resolutions. Often
the default resolution is set by the IDE (Integrated Development Environment),
which is 96dpi for Python directly from the OS, Idle, PyScripter or Thonny but 
for other IDEs (Spyder etc) uses the higher resolution. A lot of the problem
stems from the fact that sizes are usually in pixels which  
are simple integers.

No single silver bullet exists to solve this situation, so it's best to deal
with this on a case by case basis.

.. toctree::
   :caption: DPI Awareness...
   :maxdepth: 1
   
   intro_dpi
   tk_widgets
   ttk_widgets