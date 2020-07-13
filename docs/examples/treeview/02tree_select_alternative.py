"""tkinter ttk treeview
    Shows data in parallel columns, selection, alternative binding
  """

from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Treeview, Style, Label

root = Tk()
st1 = Style()
st1.theme_use('default')

# function to enable selection
def select_item(evt):
    cur_item = tree.focus()
    lvar.set(tree.item(cur_item)['values'])

# headings and data
tree_columns = ['Colours', 'Hash', 'RGB']

tree_data = (('red', '#FF0000', (255,0,0)),
            ('yellow', '#FFFF00', (255,255,0)),
            ('blue', '#0000FF', (0,0,255)),
            ('green', '#00FF00', (0,255,0)),
            ('magenta', '#FF00FF', (255,0,255)),
            ('cyan', '#00FFFF', (0,255,255)))

fr0 = Frame(root)
fr0.grid(column=0, row=0, sticky='nsew')

# create Treeview widget
tree = Treeview(fr0, column=tree_columns, show='headings')
tree.grid(column=0, row=0, sticky='nsew')
tree.bind("<ButtonRelease-1>", select_item)

# insert header and data
for col in tree_columns:
    tree.heading(col, text=col.title())

for  item in tree_data:
    itemID = tree.insert('', 'end', values=item)

# display selection
lvar = StringVar()
lbl = Label(fr0, textvariable=lvar, text="Ready")
lbl.grid(column=0, row=1, sticky='nsew')

root.mainloop()
