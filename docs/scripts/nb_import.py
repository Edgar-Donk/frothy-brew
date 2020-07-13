"""Basic notebook with 3 tabs, binding, disabled state, height and
    width adjustments, import treewiew with selection
"""

from tkinter import Tk, Frame, StringVar, Label
from tkinter.ttk import Notebook, Button, Style
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '.')
from tree_function import Tree


def tab_changed(event):
    """procedure to change size configuration
        bound to clicking on tab

    Parameters
    ----------
    event : str
        bind handle

    """
    event.widget.update_idletasks()
    tc1 = event.widget.nametowidget(event.widget.select())
    event.widget.configure(
        height=tc1.winfo_reqheight(),
        width=tc1.winfo_reqwidth())


def nb_import(parent):
    """Notebook using three tabs,
        import notebook, autosized

    Parameters
    ----------
    parent : str
      parent
    st : str
      handle to Style

    """
    st1 = Style()
    st1.theme_use('default')
    st1.configure(
        'green.TNotebook.Tab',
        background='light green',
        foreground='blue')
    st1.map('green.TNotebook.Tab', background=[
        ('disabled', '#d9d9d9'), ('selected', '#bceebc')])

    nbi = Notebook(parent, style='green.TNotebook')
    nbi.bind("<<NotebookTabChanged>>", tab_changed)
    nbi.grid(row=0, column=0)
    nbi.enable_traversal()

    # first page
    page1 = Frame(root, background='red', height=70)

    enabler = Button(page1, text='Enable Tab two\n Test it out',
                     command=lambda: nbi.tab(1, state='normal'))
    enabler.pack(ipadx=5, ipady=5)

    nbi.add(page1, text='one', underline=0, padding=2)

    # second page
    page2 = Frame(root, background='yellow', height=20)

    out_var = StringVar()
    out_var.set("First make your selection in page two")
    Tree(page2, out_var)

    nbi.add(page2, text='two', underline=1, padding=2, state='disabled')

    # third page
    page3 = Frame(root, background='alice blue', height=120)

    lbl = Label(page3, text='waiting', textvariable=out_var, bg='#AFDBFF',
                height=10)
    lbl.grid(column=0, row=1, sticky='e', ipadx=5)

    nbi.add(page3, text='three', underline=2, padding=2)


if __name__ == "__main__":
    root = Tk()

    fr1 = Frame(root)
    fr1.pack()
    nb_import(fr1)
    root.mainloop()
