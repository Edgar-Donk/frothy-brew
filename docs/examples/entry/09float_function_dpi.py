"""
Float function for entry, tried using a named tuple to stop pylint
    complaining about too many variables - still complaining
"""
from tkinter import Tk, DoubleVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Frame, Button
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def entry_float(parent,lf_text,l_limit,u_limit, mess_text, out_var):
    """Float layout for entry

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    l_limit : float
        lower limit
    u_limit : float
        upper limit
    mess_text : str
        message
    out_var : float
        tkvar handle

    Returns
    -------
    float
    """
    st1 = Style()
    st1.theme_use('default')

    st1.configure('brown.TLabelframe', background='#C9B99B')
    st1.configure('brown.TLabelframe.Label', background='#EDEF77')
    st1.configure('brown.TLabel', background='#EDEF77')
    st1.configure('lowr.TLabel', background='lightblue')
    st1.configure('upr.TLabel', background='red')

    lf0 = Labelframe(parent, text=lf_text, style='brown.TLabelframe')
    lf0.grid(row=0, column=0, padx=10, pady=10)

    ulab = Label(lf0, text=str(u_limit)+"  upper limit", style='brown.TLabel')
    ulab.grid(row=0, column=1, padx=10)
    llab = Label(lf0, text=str(l_limit)+"  lower limit", style='brown.TLabel')
    llab.grid(row=2, column=1, padx=10)

    def end_input(_evt):
        """limit on float

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        None
        """
        ulab['style'] = 'brown.TLabel'
        llab['style'] = 'brown.TLabel'
        if l_limit < entsv.get() < u_limit:
            messlbl['text'] = "That's OK"
            out_var.set(entsv.get())
        elif l_limit >= entsv.get():
            messlbl['text'] = "Input below lower limit"
            llab['style'] = 'lowr.TLabel'
        else:
            messlbl['text'] = "Input above upper limit"
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
        if text in ("", "-", ".", "-."):
            return True
        try:
            float(text)
        except ValueError:
            return False
        return True

    vcmd = lf0.register(is_okay)

    entsv = DoubleVar()
    ent0 = Entry(lf0, validate='key', validatecommand=(vcmd, '%P'),
                textvariable=entsv)
    ent0.bind("<Return>", end_input)
    ent0.grid(row=1, column=0, padx=10)
    ent0.focus()

    messlbl = Label(lf0, text=mess_text, style='brown.TLabel')
    messlbl.grid(row=2, column=0, pady=10, padx=10)

if __name__ == "__main__":
    root = Tk()
    ORIGINAL_DPI = 96
    current_dpi = root.winfo_fpixels('1i')
    SCALE = current_dpi / ORIGINAL_DPI
    # when current_dpi is 192 SCALE becomes 2.0
    root.tk.call('tk', 'scaling', SCALE)

    fra0 = Frame(root)
    fra0.grid()
    LFTEXT = 'Beer Strength % v/v'
    LLIMIT = 0.0
    ULIMIT = 10.0
    out_var1 = DoubleVar()
    MESSTEXT = 'Insert +ve or -ve float, <Return> to confirm'

    entry_float(fra0,LFTEXT,LLIMIT,ULIMIT, MESSTEXT, out_var1)

    b2 = Button(root, text='Click after selection',
                command=lambda: print(out_var1.get()))
    b2.grid(row=1, column=0)
    root.mainloop()
