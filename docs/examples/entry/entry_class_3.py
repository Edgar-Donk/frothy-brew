"""String, Integer and Float Entry classes"""
from tkinter import Tk, StringVar, IntVar, DoubleVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Button, Frame,\
    Checkbutton


class StringEntry:
    """String class for entry
        added colour, change state
        integer and float classes added

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    def_inp : str
        default text
    colour : str
        frame colour
    mod : str
        enable or disable state switch

    Returns
    -------
    string
    """

    def __init__(self, parent, lf_text, mess_text, def_inp="", colour='brown',
                 mod=False):
        self.parent = parent
        self.lf_text = lf_text
        self.mess_text = mess_text
        self.mod = mod

        self.ent0 = None    #   for entry
        self.cb_opt = None  #   for check option

        self.out_var = StringVar()
        self.out_var.set(def_inp)

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

        self.construct()

    def construct(self):
        """construct of LabelFrame and message

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.lf1 = Labelframe(self.parent, text=self.lf_text,
                              style=self.colour + '.TLabelframe')
        self.lf1.grid(column=0, row=0, padx=10, pady=10)
        self.messlbl = Label(
            self.lf1,
            text=self.mess_text,
            style='brown.TLabel')
        self.messlbl.grid(row=2, column=0, pady=10, padx=10)

        self.make_entry()

    def make_entry(self):
        """construct of Entry

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        vcmd = root.register(self.is_okay)

        self.ent0 = ent0 = Entry(self.lf1, validate='key',
                                 validatecommand=(vcmd, '%P', '%S', '%i'),
                                 textvariable=self.out_var)
        ent0.bind("<Return>", self.end_input)
        ent0.grid(row=1, column=0, padx=10)
        ent0.focus()

        if self.mod in (True, False):
            self.modify()

    def modify(self):
        """construct of state switch

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        lf_text = self.lf_text
        # entry disabled until checkbox is ticked
        self.cb_opt = Checkbutton(self.lf1, command=self.toggle_opt,
                                  style=self.colour + '.TCheckbutton')
        self.lf1['labelwidget'] = self.cb_opt
        if self.mod:
            self.ent0.state(['!disabled'])
            self.cb_opt.state(['!selected'])
            self.cb_opt['text'] = lf_text + '\n Check to prevent editing '
            self.ent0.focus()
        else:
            self.ent0.state(['disabled'])
            self.cb_opt.state(['selected'])
            self.cb_opt['text'] = lf_text + '\n Check to modify '

    def toggle_opt(self):
        """state switch logic

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        lf_text = self.lf_text
# state of entry controlled
# by the state of the check button in Option frame label widget
        if self.cb_opt.instate(['selected']):
            self.ent0.state(['disabled'])
            self.cb_opt['text'] = lf_text + '\n Check to modify '
        else:
            self.ent0.state(['!disabled'])  # enable option
            self.cb_opt['text'] = lf_text + '\n Check to prevent editing '
            self.ent0.focus()

    def end_input(self, _evt):
        """limit on string

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        None
        """
        # print('evt',self.ensv.get())
        if len(self.out_var.get()) > 5:
            self.messlbl['text'] = "That's OK"
        else:
            self.messlbl['text'] = "Should be at least 6 characters long"

    def is_okay(self, text, inp, ind):
        """ validation function

        Parameters
        ----------
        text : str
            text if allowed
        inp : str
            current input

        Returns
        -------
        boolean
        """
        ind = int(ind)
        print(ind)
        if (inp.isalnum() or inp in (",", ".", "'", " ")) and ind > 0:
            return True
        else:
            return bool((text.isupper() or text == "") and ind == 0)


class IntegerEntry(StringEntry):
    """Integer class for entry

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    l_limit : int
        lower limit
    u_limit : int
        upper limit
    def_inp : str
        default text
    colour : str
        frame colour
    mod : str
        enable or disable state switch

    Returns
    -------
    integer
    """

    def __init__(self, parent, lf_text, mess_text, l_limit, u_limit, def_inp="",
                 colour='brown', mod=False):
        self.parent = parent
        self.lf_text = lf_text
        self.mess_text = mess_text
        self.mod = mod
        self.colour = colour
        StringEntry.__init__(
            self,
            parent,
            lf_text,
            mess_text,
            def_inp,
            colour,
            mod)
        self.l_limit = l_limit
        self.u_limit = u_limit

        self.out_var = IntVar()
        self.out_var.set(def_inp)

        self.farbe = farbe = {'blue': 'light blue', 'brown': '#EDEF77',
                              'green': 'light green', 'pink': '#EAAFBF'}

        colour = colour if colour in farbe else 'brown'

        self.colour = colour

        st1 = Style()
        st1.theme_use('default')

        st1.configure(colour + '.TLabelframe', background='#C9B99B')
        st1.configure(colour + '.TLabelframe.Label', background=farbe[colour])
        st1.configure(colour + '.TCheckbutton', background=farbe[colour])
        st1.configure('brownn.TLabel', background='#EDEF77')
        st1.configure('lowr.TLabel', background='lightblue')
        st1.configure('upr.TLabel', background='red')

        self.construct()
        self.limits()

    def limits(self):
        """limit logic

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.ulab = Label(self.lf1, text=str(self.u_limit) + "  upper limit",
                          style='brown.TLabel')
        self.ulab.grid(row=0, column=1, padx=10)
        self.llab = Label(self.lf1, text=str(self.l_limit) + "  lower limit",
                          style='brown.TLabel')
        self.llab.grid(row=2, column=1, padx=10)

        self.make_entry()

    def end_input(self, _evt):
        """limit on integer

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        None
        """
        self.ulab['style'] = 'brown.TLabel'
        self.llab['style'] = 'brown.TLabel'
        if self.l_limit < int(self.out_var.get()) < self.u_limit:
            self.messlbl['text'] = "That's OK"
        elif self.l_limit >= int(self.out_var.get()):
            self.messlbl['text'] = "Input below or at lower limit"
            self.llab['style'] = 'lowr.TLabel'
        else:
            self.messlbl['text'] = "Input above or at upper limit"
            self.ulab['style'] = 'upr.TLabel'

    def is_okay(self, text, inp, ind):
        """ validation function

        Parameters
        ----------
        text : str
            text if allowed
        inp : str
            current input

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
    """Float class for entry

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    l_limit : float
        lower limit
    u_limit : float
        upper limit
    deftext : str
        default text
    colour : str
        frame colour
    mod : str
        enable or disable state switch

    Returns
    -------
    float
    """

    def __init__(self, parent, lf_text, mess_text, l_limit, u_limit, def_inp="",
                 colour='brown', mod=False):
        self.parent = parent
        self.lf_text = lf_text
        self.mess_text = mess_text
        self.mod = mod
        self.colour = colour
        self.l_limit = l_limit
        self.u_limit = u_limit
        IntegerEntry.__init__(self, parent, lf_text, mess_text, l_limit, u_limit,
                              def_inp=None, colour='brown', mod=False)
        self.out_var = DoubleVar()
        self.out_var.set(def_inp)

        self.farbe = farbe = {'blue': 'light blue', 'brown': '#EDEF77',
                              'green': 'light green', 'pink': '#EAAFBF'}

        colour = colour if colour in farbe else 'brown'

        self.colour = colour

        st1 = Style()
        st1.theme_use('default')

        st1.configure(colour + '.TLabelframe', background='#C9B99B')
        st1.configure(colour + '.TLabelframe.Label', background=farbe[colour])
        st1.configure(colour + '.TCheckbutton', background=farbe[colour])
        st1.configure('brownn.TLabel', background='#EDEF77')
        st1.configure('lowr.TLabel', background='lightblue')
        st1.configure('upr.TLabel', background='red')

        self.construct()
        self.limits()

    def end_input(self, _evt):
        """limit on float

        Parameters
        ----------
        evt : str
            bind handle

        Returns
        -------
        None
        """
        self.ulab['style'] = 'brown.TLabel'
        self.llab['style'] = 'brown.TLabel'
        if self.l_limit < float(self.out_var.get()) < self.u_limit:
            self.messlbl['text'] = "That's OK"
        elif self.l_limit >= float(self.out_var.get()):
            self.messlbl['text'] = "Input below lower limit"
            self.llab['style'] = 'lowr.TLabel'
        else:
            self.messlbl['text'] = "Input above upper limit"
            self.ulab['style'] = 'upr.TLabel'

    def is_okay(self, text, inp, ind):
        """ validation function

        Parameters
        ----------
        text : str
            text if allowed
        inp : str
            current input

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
    fr = Frame(root)
    fr.grid(row=0, column=0)
#    LF_TEXT = 'Beer Type'
#    DEF_TEXT = 'Pilsner'
    COLOUR = ''
    MOD = True
    '''
    MESS_TEXT = 'Start with capital letter,\n use at least 6 characters\n <Return> to confirm'
    v = StringEntry(fr,LF_TEXT,MESS_TEXT,DEF_TEXT,COLOUR,MOD)

    LF_TEXT = 'Number of Coils'
    MESS_TEXT = 'Insert +ve or -ve integer,\n <Return> to confirm'
    DEF_TEXT = 10
    L_LIMIT = 1
    U_LIMIT= 100
    v = IntegerEntry(fr,LF_TEXT,MESS_TEXT,L_LIMIT,U_LIMIT,DEF_TEXT,COLOUR,MOD)
    '''
    LF_TEXT = 'Beer Strength v/v % alcohol'
    DEF_TEXT = 5.0
    L_LIMIT = 0.5
    U_LIMIT = 10.5
    MESS_TEXT = 'Insert +ve or -ve float,\n <Return> to confirm'
    v = FloatEntry(
        fr,
        LF_TEXT,
        MESS_TEXT,
        L_LIMIT,
        U_LIMIT,
        DEF_TEXT,
        COLOUR,
        MOD)

    b2 = Button(root, text='Click after selection',
                command=lambda: print(v.out_var.get()))
    b2.grid(row=2, column=0)
    root.mainloop()
