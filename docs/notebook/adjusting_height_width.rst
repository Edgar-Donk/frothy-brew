Adjusting Width and Height
==========================

.. figure:: ../figures/nb_adjust.webp
    :width: 120
    :height: 70
    :alt: tkinter notebook adjusting size
    :align: center

From the last script it can be seen that all the tabs are the same size, 
which would be usuitable in many instances. In order to change the size 
of the panel contents we have a problem as none of the frames within the tabs
can be changed by the layout manager. We need to use the notebook's built in 
virtual event ``<<NotebookTabChanged>>`` bound to a function:: 

    def tab_changed(event):
        tc1 = event.widget.nametowidget(event.widget.select())
        event.widget.configure(
            height=t.winfo_reqheight(),
            width=t.winfo_reqwidth())
        
        ...........
    nb1.bind("<<NotebookTabChanged>>", tab_changed)

If we run the above we see that the size of the panel content changes, but 
only after a tab has been clicked. On opening our application the button in
Page1 is not to be seen, it only appears after the first tab has been 
selected. This is not what we want, so update the widget's idletasks at the 
beginning of the function **tab_changed**::

    def tab_changed(event):
        event.widget.update_idletasks()

.. container:: toggle

    .. container:: header

        *Show/Hide Code* 04nb_adjust.py

    .. literalinclude:: ../examples/notebook/04nb_adjust.py
        :emphasize-lines: 19, 27-31, 35

The full effect of the size adjustment becomes really apparent once we have
loaded data, which we should see in the next section.        