"""basic entry for string, with validation"""

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
    if text.isalpha():
        print(text)
        return True
    else:
        return False

vcmd = root.register(is_okay)

ent0 = Entry(root, validate='key', validatecommand=(vcmd, '%P'))
ent0.pack(padx=10)

root.mainloop()
