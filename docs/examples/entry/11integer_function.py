"""Enhanced Integer Entry as a function, after pylint"""

from tkinter import Tk, IntVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Button, Frame

def entry_integer(parent, lftext, llimit, ulimit, messtext, out_var):
    """Integer layout for entry

    Parameters
    ----------
    parent : str
        parent handle
    lftext : str
        text on LabelFrame
    llimit : int
        lower limit
    ulimit : int
        upper limit
    messtext : str
        message
    out_var : int
        tkvar handle

    Returns
    -------
    integer
    """
    st1 = Style()
    st1.theme_use('default')

    st1.configure('brown.TLabelframe', background='#C9B99B')
    st1.configure('brown.TLabelframe.Label', background='#EDEF77')
    st1.configure('brown.TLabel', background='#EDEF77')
    st1.configure('lowr.TLabel', background='lightblue')
    st1.configure('upr.TLabel', background='red')

    lf0 = Labelframe(parent, text=lftext, style='brown.TLabelframe')
    lf0.grid(row=0, column=0, padx=10, pady=10)

    ulab = Label(lf0, text=str(ulimit)+"  upper limit", style='brown.TLabel')
    ulab.grid(row=0, column=1, padx=10)
    llab = Label(lf0, text=str(llimit)+"  lower limit", style='brown.TLabel')
    llab.grid(row=2, column=1, padx=10)

    def end_input(_evt):
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
        if llimit < int(entsv.get()) < ulimit:
            mee_lbl['text'] = "That's OK"
            out_var.set(int(entsv.get()))
        elif llimit >= int(entsv.get()):
            mee_lbl['text'] = "Input below lower limit"
            llab['style'] = 'lowr.TLabel'
        else:
            mee_lbl['text'] = "Input above upper limit"
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

    vcmd = lf0.register(is_okay)

    entsv = IntVar()
    ent0 = Entry(lf0, validate='key', validatecommand=(vcmd, '%P'),
                 textvariable=entsv)
    ent0.bind("<Return>", end_input)
    ent0.grid(row=1, column=0, padx=10)
    ent0.focus()

    mee_lbl = Label(lf0, text=messtext, style='brown.TLabel')
    mee_lbl.grid(row=2, column=0, pady=10, padx=10)

if __name__ == "__main__":
    root = Tk()
    fra0 = Frame(root)
    fra0.grid(row=0, column=0)
    LF_TEXT = 'Number of Coils'
    L_LIMIT = 0
    U_LIMIT = 100
    out_var1 = IntVar()
    MESS_TEXT = 'Insert +ve or -ve integer, <Return> to confirm'
    entry_integer(fra0, LF_TEXT, L_LIMIT, U_LIMIT, MESS_TEXT, out_var1)
    b2 = Button(root, text='Click after selection',
                command=lambda: print(out_var1.get()))
    b2.grid(row=1, column=0)
    root.mainloop()
