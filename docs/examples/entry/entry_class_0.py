"""String class for entry"""
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Style, Label, Labelframe, Button, Frame

class StringEntry:
    """String class for entry
        06layout_string converted to a class

    Parameters
    ----------
    parent : str
        parent handle
    lf_text : str
        text on LabelFrame
    mess_text : str
        message
    outVar : float
        tkvar handle

    Returns
    -------
    string
    """
    def __init__(self, parent, lf_text, mess_text):
        self.parent = parent
        self.lf_text = lf_text
        self.mess_text = mess_text

        self.out_var = StringVar()

        st1 = Style()
        st1.theme_use('default')

        st1.configure('brown.TLabelframe', background='#C9B99B')
        st1.configure('brown.TLabelframe.Label', background='#EDEF77')
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
        self.lf0 = Labelframe(self.parent, text=self.lf_text,
                              style='brown.TLabelframe')
        self.lf0.grid(column=0, row=0, padx=10, pady=10)
        self.mee_lbl = Label(self.lf0, text=self.mess_text,
                             style='brown.TLabel')
        self.mee_lbl.grid(row=2, column=0, pady=10, padx=10)

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
        vcmd = self.lf0.register(self.is_okay)

        ent0 = Entry(self.lf0, validatecommand=(vcmd, '%P', '%S', '%i'),
                     validate='key', textvariable=self.out_var)
        ent0.bind("<Return>", self.end_input)
        ent0.grid(row=1, column=0, padx=10)
        ent0.focus()

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
            self.mee_lbl['text'] = "That's OK"
        else:
            self.mee_lbl['text'] = "Should be at least 6 characters long"

    def is_okay(self, text, input, index):
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
        #print(text)
        index = int(index)
        print(index)
        if (input.isalnum() or input in (",", ".", "'", " ")) and index > 0:
            return True
        else:
            return bool((text.isupper() or text == "") and index == 0)

if __name__ == "__main__":
    root = Tk()

    fra0 = Frame(root)
    fra0.grid(row=0, column=0)
    LF_TEXT = 'Beer Type'

    MESS_TEXT = 'Start with capital letter, use at least 6 characters '\
        '<Return> to confirm'
    v = StringEntry(fra0, LF_TEXT, MESS_TEXT)

    b2 = Button(root, text='Click after selection',
                command=lambda: print(v.out_var.get()))
    b2.grid(row=2, column=0)
    root.mainloop()
