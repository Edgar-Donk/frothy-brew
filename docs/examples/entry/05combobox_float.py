"""basic entry for float, correction, allows negative input,
    optional range checking

Parameters
----------
None

Returns
-------
None
"""
from tkinter import Tk, font
from tkinter.ttk import Spinbox, Style

root = Tk()
style = Style()
style.theme_use('default')

def_font = font.nametofont('TkDefaultFont')
font_family = def_font.actual()['family']
font_size = def_font.actual()['size'] + 2

def is_okay(text):
    """ validation function

    Parameters
    ----------
    text : str
        text if allowed

    Returns
    -------
    boolean
    """
    print(text)
    if text in ("", "-", ".", "-."):
        return True
    try:
        float(text)
    except ValueError:
        return False
    return True

vcmd = root.register(is_okay)

ent0 = Spinbox(root, validate="key", validatecommand=(vcmd, '%P'),
           font=(font_family, font_size, 'bold'))
ent0.pack(padx=10)

root.mainloop()
