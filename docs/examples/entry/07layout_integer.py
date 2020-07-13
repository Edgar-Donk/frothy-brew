"""String layout that determines the finish of input from a Return event.
    the integer is checked against limits before confirming that all is OK

"""
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Style, Label, Labelframe

root = Tk()
style = Style()
style.theme_use('default')

style.configure('brown.TLabelframe', background='#C9B99B')
style.configure('brown.TLabelframe.Label', background='#EDEF77')
style.configure('brown.TLabel', background='#EDEF77')
style.configure('lowr.TLabel', background='lightblue')
style.configure('upr.TLabel', background='red')

LFTEXT = 'Number of Coils'
lf0 = Labelframe(root, text=LFTEXT, style='brown.TLabelframe')
lf0.pack(padx=10, pady=10)
L_LIMIT = 0
U_LIMIT = 100

ulab = Label(lf0, text=str(U_LIMIT)+"  upper limit", style='brown.TLabel')
ulab.grid(row=0, column=1, padx=10)
llab = Label(lf0, text=str(L_LIMIT)+"  lower limit", style='brown.TLabel')
llab.grid(row=2, column=1, padx=10)


def end_input(evt):
    """limit on integer

    Parameters
    ----------
    evt : str
        bind handle

    Returns
    -------
    None
    """
    print('evt', entsv.get())
    ulab['style'] = 'brown.TLabel'
    llab['style'] = 'brown.TLabel'
    if L_LIMIT < int(entsv.get()) < U_LIMIT:
        mess_lbl['text'] = "That's OK"
    elif L_LIMIT >= int(entsv.get()):
        mess_lbl['text'] = "Input below lower limit"
        llab['style'] = 'lowr.TLabel'
    else:
        mess_lbl['text'] = "Input above upper limit"
        ulab['style'] = 'upr.TLabel'

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

entsv = StringVar()
ent0 = Entry(lf0, validate='key', validatecommand=(vcmd, '%P'), textvariable=entsv)
ent0.bind("<Return>", end_input)
ent0.grid(row=1, column=0, padx=10)
ent0.focus()

mess_lbl = Label(lf0, text='Insert +ve or -ve integer, <Return> to confirm',
                style='brown.TLabel')
mess_lbl.grid(row=2, column=0, pady=10, padx=10)

root.mainloop()
