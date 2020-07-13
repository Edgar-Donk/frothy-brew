"""basic entry for string allowing additional characters,
    the logic in the validation function will be improved
"""
from tkinter import Tk
from tkinter.ttk import Entry, Style

root = Tk()
style = Style()
style.theme_use('default')

def is_okay(text, input):
    """ validation function - demo purposes only

    Parameters
    ----------
    text : str
        text if allowed
    input : str
        current input

    Returns
    -------
    boolean
    """
    if input.isupper() and len(text) == 1:
        return True
    elif input in (",", ".", "'", " ") and len(text) > 1:
        return True
    elif input.isalnum() and len(text) > 1:
        return True
    elif text == "":
        return True
    else:
        return False

vcmd = root.register(is_okay)

ent0 = Entry(root, validate='key', validatecommand=(vcmd, '%P', '%S'))
ent0.pack(padx=10)

root.mainloop()
