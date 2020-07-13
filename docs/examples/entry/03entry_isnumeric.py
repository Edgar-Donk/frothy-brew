"""basic entry for positive integers, with validation,
    optional range checking
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
    if text.isnumeric(): # int(inp):
        ## do not use range, change 1 to 11 and test ##
        if int(text) in range(1, 63):
            return True
        else:
            return False
        return True
    elif text == "":
        return True
    else:
        return False

vcmd = root.register(is_okay)

ent0 = Entry(root, validate="key", validatecommand=(vcmd, "%P"))
ent0.pack(padx=10)

root.mainloop()
