"""tkinter ttk treeview
    Shows data in parallel columns, selection, zebra stripes
    includes workaround for python 3.7 tag colour display
  """

from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Treeview, Style, Label

def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in st1.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

root = Tk()
st1 = Style()
st1.theme_use('default')

st1.map('Treeview', foreground=fixed_map('foreground'),
            background=fixed_map('background'))

# function to enable selection
def select_item(evt):
    curItem = tree.focus()
    lvar.set(tree.item(curItem)['values'])

# headings and data
tree_columns = ['Colours', 'Hash', 'RGB']

tree_data = (('red', '#FF0000', (255,0,0)),
            ('yellow', '#FFFF00', (255,255,0)),
            ('blue', '#0000FF', (0,0,255)),
            ('green', '#00FF00', (0,255,0)),
            ('magenta', '#FF00FF', (255,0,255)),
            ('cyan', '#00FFFF', (0,255,255)))

backg = ["white",'#f0f0ff']

fr0 = Frame(root)
fr0.grid(column=0, row=0, sticky='nsew')

# create Treeview widget
tree = Treeview(fr0, column=tree_columns, show='headings')
tree.grid(column=0, row=0, sticky='nsew')
tree.bind("<<TreeviewSelect>>", select_item)

# insert header, data and tag configuration
for col in tree_columns:
    tree.heading(col, text=col.title())

for ix, item in enumerate(tree_data):
    item_ID = tree.insert('', 'end', values=item)
    tree.item(item_ID, tags=item_ID)
    tree.tag_configure(item_ID, background=backg[ix%2])

# display selection
lvar = StringVar()
lbl = Label(fr0, textvariable=lvar, text="Ready")
lbl.grid(column=0, row=1, sticky='nsew')

root.mainloop()
