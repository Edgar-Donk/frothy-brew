"""basic entry for string allowing additional characters, made better
    but not the best
"""

from tkinter import Tk
from tkinter.ttk import Entry, Style

root = Tk()
style = Style()
style.theme_use('default')

def is_okay(index, action, input):
    """ validation function

    Parameters
    ----------
    index : str
        index
    action : str
        action
    input : str
        current input

    Returns
    -------
    boolean
    """
    index = int(index)
    if action == '1':
        if input.isupper() and index == 0:
            return True
        if input in (",", ".", "'", " ") and index > 0:
            return True
        if input.isalnum() and index > 0:
            return True
        else:
            return False
    else:
        return True

vcmd = root.register(is_okay)

ent0 = Entry(root, validate='key', validatecommand=(vcmd, '%i', '%d', '%S'))
ent0.pack(padx=10)

root.mainloop()
