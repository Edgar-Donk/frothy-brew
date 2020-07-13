"""basic entry for integer, validation, allows negative numbers,
    no range checking
"""
from tkinter import Tk
from tkinter.ttk import Entry, Style

root = Tk()
style = Style()
style.theme_use('default')

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
    if text in("", "-"):
        return True
    try:
        int(text)
    except ValueError:
        return False
    return True

vcmd = root.register(is_okay)

ent0 = Entry(root, validate="key", validatecommand=(vcmd, "%P"))
ent0.pack(padx=10)

root.mainloop()
