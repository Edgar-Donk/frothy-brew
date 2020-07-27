"""
String function for entry
"""
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Button, Frame

def entry_string(parent, lf_text, mess_text, out_var):
    """String layout for entry
        06layout_string converted to a function

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    out_var : float
        tkvar handle

    Returns
    -------
    string
    """
    st1 = Style()
    st1.theme_use('default')

    st1.configure('brown.TLabelframe', background='#C9B99B')
    st1.configure('brown.TLabelframe.Label', background='#EDEF77')
    st1.configure('brown.TLabel', background='#EDEF77')

    lf0 = Labelframe(parent, text=lf_text, style='brown.TLabelframe')
    lf0.grid(column=0, row=0, padx=10, pady=10)

    def end_input(_evt):
        """limit on string

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        None
        """
        if len(entsv.get()) > 5:
            mee_lbl['text'] = "That's OK"
            out_var.set(entsv.get())
        else:
            mee_lbl['text'] = "Should be at least 6 characters long"

    def is_okay(text, input, index):
        """ validation function

        Parameters
        ----------
        text : str
            text if allowed
        input : str
            current inputut
        index : str
            indexex

        Returns
        -------
        boolean
        """
        index = int(index)
        print(index)
        if (input.isalnum() or input in (",", ".", "'", " ")) and index > 0:
            return True
        else:
            return bool((text.isupper() or text == "") and index == 0)

    vcmd = lf0.register(is_okay)

    entsv = StringVar()
    ent0 = Entry(lf0, validate='key', textvariable=entsv,
                 validatecommand=(vcmd, '%P', '%S', '%i'))
    ent0.bind("<Return>", end_input)
    ent0.grid(row=1, column=0, padx=10)
    ent0.focus()

    mee_lbl = Label(lf0, text=mess_text, style='brown.TLabel')
    mee_lbl.grid(row=2, column=0, pady=10, padx=10)

if __name__ == "__main__":
    root = Tk()
    fra0 = Frame(root)
    fra0.grid()
    LFTEXT = 'Beer Type'
    out_var1 = StringVar()
    MESSTEXT = 'Start with capital letter, use at least 6 characters '\
            '<Return> to confirm'
    entry_string(fra0, LFTEXT, MESSTEXT, out_var1)
    b2 = Button(root, text='Click after selection',
                command=lambda: print(out_var1.get()))
    b2.grid(row=2, column=0)
    root.mainloop()
