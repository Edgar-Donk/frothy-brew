==============
Enhanced Entry
==============

Scientific and engineering data entry often requires a knowledge not only the
name of the data but of its units together with upper and lower limits. Related
data might be colour coded rather than just grouped. Some form of checking 
is required to ensure that numerical and character inputs conform. 

If we surround an Entry widget with a LabelFrame we can then place the name 
and units of our data in the label part of the LabelFrame, which can
be coloured and have a switch to activate/deactivate the entry. Within
the LabelFrame place two labels with upper and lower limits next to the entry. 
Finally another label can be placed below the entry with user hints. 

All this can be bundled together and used as a single widget.

.. toctree::
   :caption: Entries...
   :maxdepth: 1
   
   entry_validation
   basic_entries
   entry_layouts
   entry_class
   adding_entries
   working_with_class