"""String class for entry, with colour and enabling/disabling choice """
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Button, Frame, \
                        Checkbutton

class StringEntry:
    """String class for entry
        added colour, change state

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    def_text : str
        default text
    colour : str
        frame colour
    mod : str
        enable or disable state switch

    Returns
    -------
    string
    """
    def __init__(self, parent, lf_text, mess_text, def_text="", colour='brown',
                 mod=False):
        self.parent = parent
        self.lf_text = lf_text
        self.mess_text = mess_text
        self.mod = mod

        self.out_var = StringVar()
        self.out_var.set(def_text)

        self.farbe = farbe = {'blue': 'light blue', 'brown': '#EDEF77',
                              'green': 'light green', 'pink': '#EAAFBF'}

        colour = colour if colour in farbe else 'brown'

        self.colour = colour

        st1 = Style()
        st1.theme_use('default')

        st1.configure(colour+'.TLabelframe', background='#C9B99B')
        st1.configure(colour+'.TLabelframe.Label', background=farbe[colour])
        st1.configure(colour+'.TCheckbutton', background=farbe[colour])
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
                              style=self.colour+'.TLabelframe')
        self.lf1.grid(column=0, row=0, padx=10, pady=10)
        self.messlbl = Label(self.lf1, text=self.mess_text, style='brown.TLabel')
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

        self.ent1 = ent1 = Entry(self.lf1, validate='key',
                                 validatecommand=(vcmd, '%P', '%S', '%i'),
                                 textvariable=self.out_var)
        ent1.bind("<Return>", self.end_input)
        ent1.grid(row=1, column=0, padx=10)
        ent1.focus()

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
                                  style=self.colour+'.TCheckbutton')
        self.lf1['labelwidget'] = self.cb_opt
        if self.mod:
            self.ent1.state(['!disabled'])
            self.cb_opt.state(['!selected'])
            self.cb_opt['text'] = lf_text+' Check to prevent editing '
            self.ent1.focus()
        else:
            self.ent1.state(['disabled'])
            self.cb_opt.state(['selected'])
            self.cb_opt['text'] = lf_text+' Check to modify '

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
#       state of entry controlled
#       by the state of the check button in Option frame label widget
        if self.cb_opt.instate(['selected']):
            print('selected state')
            self.ent1.state(['disabled'])
            self.cb_opt['text'] = lf_text+' Check to modify '
        else:
            print('unselected state')
            self.ent1.state(['!disabled'])  # enable option
            self.cb_opt['text'] = lf_text+' Check to prevent editing '
            self.ent1.focus()

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

if __name__ == "__main__":
    root = Tk()
    fra0 = Frame(root)
    fra0.grid(row=0, column=0)
    LF_TEXT = 'Beer Type'
    DEF_TEXT = 'Pilsner'
    COLOUR = 'blue'
    MOD = False
    MESS_TEXT = 'Start with capital letter, use at least 6 characters '\
        '<Return> to confirm'
    v = StringEntry(fra0, LF_TEXT, MESS_TEXT, DEF_TEXT, COLOUR, MOD)

    b2 = Button(root, text='Click after selection',
                command=lambda: print(v.out_var.get()))
    b2.grid(row=2, column=0)
    root.mainloop()
