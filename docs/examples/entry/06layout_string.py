"""entry for string with layout"""
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Style, Label, Labelframe

root = Tk()
style = Style()
style.theme_use('default')

LF_TEXT = 'Beer Type'
lf0 = Labelframe(root, text=LF_TEXT)
lf0.grid(column=0, row=0)

def end_input(evt):
    """limit on string

    Parameters
    ----------
    evt : str
        bind handle

    Returns
    -------
    None
    """
    print('evt', entsv.get())
    if len(entsv.get()) > 5:
        mess_lbl['text'] = "That's OK"
    else:
        mess_lbl['text'] = "Should be at least 6 characters long"

def is_okay(text, input, index):
    """ validation function

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
    print(text)
    index = int(index)
    if text.isupper() and index == 0:
        return True
    if input in (",", ".", "'", " ") and index > 0:
        return True
    if input.isalnum() and index > 0:
        return True
    if text == "":
        return True
    else:
        return False

vcmd = root.register(is_okay)

entsv = StringVar()
ent0 = Entry(lf0, validate='key', validatecommand=(vcmd, '%P', '%S', '%i'),
             textvariable=entsv)
ent0.bind("<Return>", end_input)
ent0.grid(row=1, column=0, padx=10)
ent0.focus()

mess_lbl = Label(lf0, text='Start with capital letter, <Return> to confirm')
mess_lbl.grid(row=2, column=0, pady=10, padx=10)

root.mainloop()
