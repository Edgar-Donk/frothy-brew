"""String, Integer and Float Entry classes, using super, inherit from
tkinter.ttk LabelFrame. Contains the following functionality:-

* Entry Validation
* Layout in a LabelFrame
* includes limits and warnings
* ability for the user to disable with a checkbox
* default value
* colour of LabelFrame

"""

from tkinter import Tk, StringVar, IntVar, DoubleVar
from tkinter.ttk import Entry, Style, Label, LabelFrame, Button, Frame, Checkbutton


class StringEntry(LabelFrame):
    """String class for entry.

        rationalised with integer and float classes,
        using super

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    def_inp : str
        default text
    colour : str
        frame colour
    mod : boolean
        enable or disable state switch

    Returns
    -------
    string
    """

    def __init__(self, parent, lf_text, def_inp="", colour='brown', mod=False):
        self.lf_text = lf_text
        super().__init__(parent, text=lf_text)
        self.mod = mod

        self.ent0 = None  # for entry
        self.cb_opt = None  # for check option

        self.out_var = StringVar()
        self.out_var.set(def_inp)

        self.construct(colour)

    def construct(self, colour):
        """Building the colour style.

        Parameters
        ----------
        colour : str
            frame colour
        """
        self.farbe = farbe = {'blue': 'light blue', 'brown': 'brown1',
                              'green': 'light green', 'pink': '#EAAFBF'}

        colour = colour if colour in farbe else 'brown'

        self.colour = colour

        st1 = Style()
        st1.theme_use('default')

        st1.configure(colour + '.TLabelframe', background='#C9B99B')
        st1.configure(colour + '.TLabelframe.Label', background=farbe[colour])
        st1.configure(colour + '.TCheckbutton', background=farbe[colour])
        st1.configure('brown.TLabel', background='#EDEF77')
        st1.configure('lowr.TLabel', background='lightblue')
        st1.configure('upr.TLabel', background='red')

        self['style'] = self.colour + '.TLabelframe'
        self.mess_lbl = Label(self, style='brown.TLabel')
        self.mess_lbl.grid(row=2, column=0, pady=10, padx=10)

        self.vcmd = root.register(self.is_okay)
        self.make_entry()

    def make_entry(self):
        """Building of Entry."""

        vcmd = root.register(self.is_okay)

        self.ent0 = ent0 = Entry(self, validate='key',
                                 validatecommand=(vcmd, '%P', '%S', '%i'),
                                 textvariable=self.out_var)
        ent0.bind("<Return>", self.end_input)
        ent0.grid(row=1, column=0, padx=10)
        ent0.focus()

        if self.mod in (True, False):
            self.modify()

    def modify(self):
        """Building of state switch.
            consists of checkbox in Label part of LabelFrame"""

        # entry disabled until checkbox is ticked
        self.cb_opt = Checkbutton(self, command=self.toggle_opt,
                                  style=self.colour + '.TCheckbutton')
        self['labelwidget'] = self.cb_opt
        if self.mod:
            self.ent0.state(['!disabled'])
            self.cb_opt.state(['!selected'])
            self.cb_opt['text'] = self.lf_text
            self.ent0.focus()
        else:
            self.ent0.state(['disabled'])
            self.cb_opt.state(['selected'])
            self.cb_opt['text'] = self.lf_text

    def toggle_opt(self):
        """state switch toggle logic"""

        # state of entry controlled
        # by the state of the check button in Option frame label widget
        if self.cb_opt.instate(['selected']):
            self.ent0.state(['disabled'])
            self.cb_opt['text'] = self.lf_text
        else:
            self.ent0.state(['!disabled'])
            self.cb_opt['text'] = self.lf_text
            self.ent0.focus()

    def end_input(self, _evt):
        """String size limit logic.

        Parameters
        ----------
        evt : str
            bind handle
        """
        if len(self.out_var.get()) > 5:
            self.mess_lbl['text'] = "That's OK"
        else:
            self.mess_lbl['text'] = "Need at least 6 characters"

    def is_okay(self, text, input_, index):
        """String validation function.

        Parameters
        ----------
        text : str
            text if allowed
        input_ : str
            current input
        index : str
        """
        if (input_.isalnum() or input_ in (",", ".", "'", " ")) and index > 0:
            return True
        else:
            return bool((text.isupper() or text == "") and index == 0)


class IntegerEntry(StringEntry):
    """Integer class with enhanced string entry functionality.

        applying limits with warnings, using super

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    l_limit : int
        lower limit
    u_limit : int
        upper limit
    def_inp : str
        default text
    colour : str
        frame colour
    mod : bool
        enable or disable state switch

    Returns
    -------
    integer
    """

    def __init__(self, parent, lf_text, l_limit, u_limit, def_inp="",
                 colour='brown', mod=False):
        super().__init__(parent, lf_text, def_inp, colour, mod)
        self.l_limit = l_limit
        self.u_limit = u_limit

        self.out_var = IntVar()
        self.out_var.set(def_inp)

        self.construct(colour)
        self.limits()
        self.make_entry()

    def limits(self):
        """Buiding limit Labels."""

        self.ulab = Label(self, text=str(self.u_limit) + "  upper limit",
                          style='brown.TLabel')
        self.ulab.grid(row=0, column=1, padx=10)
        self.llab = Label(self, text=str(self.l_limit) + "  lower limit",
                          style='brown.TLabel')
        self.llab.grid(row=1, column=1, padx=10)

    def end_input(self, _evt):
        """Limit logic for integer or float.

        Parameters
        ----------
        evt : str
            bind handle
        """

        self.ulab['style'] = 'brown.TLabel'
        self.llab['style'] = 'brown.TLabel'
        if self.l_limit < self.out_var.get() < self.u_limit:
            self.mess_lbl['text'] = "That's OK"
        elif self.l_limit >= self.out_var.get():
            self.mess_lbl['text'] = "Input below or at lower limit"
            self.llab['style'] = 'lowr.TLabel'
        else:
            self.mess_lbl['text'] = "Input above or at  upper limit"
            self.ulab['style'] = 'upr.TLabel'

    def is_okay(self, text, input_, index):
        """Validation function, using the same attributes as String entry.

        Parameters
        ----------
        text : str
            text if allowed
        input_ : str
            current input
        index : str

        Returns
        -------
        boolean
        """

        if text in ("", "-"):
            return True
        try:
            int(text)
        except ValueError:
            return False
        return True


class FloatEntry(IntegerEntry):
    """Float class for entry.

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
    def_inp : str
        default text
    colour : str
        frame colour
    mod : bool
        enable or disable state switch

    Returns
    -------
    float
    """

    def __init__(self, parent, lf_text, l_limit, u_limit, def_inp="",
                 colour='brown', mod=False):
        super().__init__(parent, lf_text, l_limit, u_limit, def_inp, colour,
                         mod)

        self.out_var = DoubleVar()
        self.out_var.set(def_inp)

        self.construct(colour)
        self.make_entry()
        self.limits()

    def is_okay(self, text, input_, index):
        """Validation function, using the same attributes as String entry.

        Parameters
        ----------
        text : str
            text if allowed
        input_ : str
            current input
        index : str

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


if __name__ == "__main__":
    root = Tk()
    fra0 = Frame(root)
    fra0.grid(row=0, column=0, columnspan=3)
    COLOUR = 'green'
    MOD = True

    LF_TEXT = 'Beer Type'
    DEF_INP = 'Pilsner'
    v0 = StringEntry(fra0, LF_TEXT, DEF_INP, COLOUR, MOD)
    v0.update_idletasks()

    LF_TEXT = 'Number of Coils'
    DEF_INP = 10
    L_LIMIT = 1
    U_LIMIT = 100
    v1 = IntegerEntry(fra0, LF_TEXT, L_LIMIT, U_LIMIT, DEF_INP, COLOUR, MOD)
    v1.update_idletasks()

    LF_TEXT = 'Beer Strength v/v % alcohol'
    DEF_INP = 5.5
    L_LIMIT = 0.5
    U_LIMIT = 10.5
    v2 = FloatEntry(fra0, LF_TEXT, L_LIMIT, U_LIMIT, DEF_INP, COLOUR, MOD)
    v2.update_idletasks()

    v2w = v2.winfo_reqwidth()
    v2h = v2.winfo_reqheight()
    v1w = v1.winfo_reqwidth()
    v1h = v1.winfo_reqheight()
    v0w = v0.winfo_reqwidth()
    v0h = v0.winfo_reqheight()
    maxw = max(v0w, v1w, v2w)
    maxh = max(v0h, v1h, v2h)

    v0.grid(column=0, row=0, ipadx=(maxw - v0w) // 2, ipady=(maxh - v0h) // 2)
    v1.grid(column=1, row=0, ipadx=(maxw - v1w) // 2, ipady=(maxh - v1h) // 2)
    v2.grid(column=2, row=0, ipadx=(maxw - v2w) // 2, ipady=(maxh - v1h) // 2)

    b0 = Button(root, text='Click after string selection',
                command=lambda: print(v0.out_var.get(), v0.mess_lbl['text']))
    b0.grid(row=2, column=0)
    b1 = Button(root, text='Click after integer selection',
                command=lambda: print(v1.out_var.get(), v1.mess_lbl['text']))
    b1.grid(row=2, column=1)
    b2 = Button(root, text='Click after float selection',
                command=lambda: print(v2.out_var.get(), v2.mess_lbl['text']))
    b2.grid(row=2, column=2)

    print('maxw',maxw,'maxh',maxh)

    root.mainloop()
