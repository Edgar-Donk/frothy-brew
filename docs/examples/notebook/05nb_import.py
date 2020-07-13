"""Basic notebook with 3 tabs, binding, disabled state, height and
    width adjustments, import treewiew with selection
  """

from tkinter import Tk, Frame, StringVar, Label
from tkinter.ttk import Notebook, Button, Style
import sys
sys.path.insert(1, '../treeview/')
from tree_function import Tree

root = Tk()
st1 = Style()
st1.theme_use('default')
st1.configure(
    'green.TNotebook.Tab',
    background='light green',
    foreground='blue')
st1.map('green.TNotebook.Tab', background=[
        ('disabled', '#d9d9d9'), ('selected', '#bceebc')])


def tab_changed(event):
    """notebook handler changes width and height after a tab is selected

    Parameters
    ----------
    event : str
        bind event
    """
    event.widget.update_idletasks()
    tc1 = event.widget.nametowidget(event.widget.select())
    event.widget.configure(
        height=tc1.winfo_reqheight(),
        width=tc1.winfo_reqwidth())


nb1 = Notebook(root, style='green.TNotebook')
nb1.bind("<<NotebookTabChanged>>", tab_changed)
nb1.grid(row=0, column=0)
nb1.enable_traversal()

# first page
page1 = Frame(root, background='red', height=70)

enabler = Button(page1, text='Enable Tab two\n Test it out',
                 command=lambda: nb1.tab(1, state='normal'))
enabler.pack(ipadx=5, ipady=5)

nb1.add(page1, text='one', underline=0, padding=2)

# second page
page2 = Frame(root, background='yellow', height=20)

CSV_FILE = '../../csv/test.csv'
CSV_DELIMITER = ';'
OUT_VAR = StringVar()
OUT_VAR.set("First make your selection in page two")
tree = Tree(page2, CSV_FILE, OUT_VAR, CSV_DELIMITER)

nb1.add(page2, text='two', underline=1, padding=2, state='disabled')

# third page
page3 = Frame(root, background='alice blue', height=120)

lbl = Label(
    page3,
    text='waiting',
    textvariable=OUT_VAR,
    bg='#AFDBFF',
    height=10)
lbl.grid(column=0, row=1, sticky='e', ipadx=5)

nb1.add(page3, text='three', underline=2, padding=2)

root.mainloop()
