"""tkinter ttk treeview
    Shows data in parallel columns
"""
  
from tkinter import Tk
from tkinter.ttk import Frame, Treeview, Style
   
root = Tk()
st1 = Style()
st1.theme_use('default')

# headings and data
tree_columns = ['Colours', 'Hash', 'RGB']

tree_data = (('red', '#FF0000', (255,0,0)),
            ('yellow', '#FFFF00', (255,255,0)),
            ('blue', '#0000FF', (0,0,255)),
            ('green', '#00FF00', (0,255,0)),
            ('magenta', '#FF00FF', (255,0,255)),
            ('cyan', '#00FFFF', (0,255,255)))

fr0 = Frame(root)
# make sure that the frame adjusts, so use sticky='nsew'
fr0.grid(column=0, row=0, sticky='nsew') 

# create Treeview widget    
tree = Treeview(fr0, column=tree_columns, show='headings')
tree.grid(column=0, row=0, sticky='nsew')

# insert header
for col in tree_columns:
    tree.heading(col, text=col.title())

#insert data   
for  item in tree_data:
    itemID = tree.insert('', 'end', values=item)

root.mainloop()
