"""Basic notebook with 3 tabs, binding, disabled state """

from tkinter import Tk, Frame
from tkinter.ttk import Notebook, Button, Style

root = Tk()
st1 = Style()
st1.theme_use('default')
st1.configure(
    'green.TNotebook.Tab',
    background='light green',
    foreground='blue')
st1.map('green.TNotebook.Tab', background=[
        ('disabled', '#d9d9d9'), ('selected', '#bceebc')])

nb1 = Notebook(root, style='green.TNotebook')
page1 = Frame(root, background='red', height=20)
page2 = Frame(root, background='yellow', height=20)
page3 = Frame(root, background='alice blue', height=20)
nb1.grid(row=0, column=0)
nb1.add(page1, text='one', underline=0, padding=2)
nb1.add(page2, text='two', underline=1, padding=2, state='disabled')
nb1.add(page3, text='three', underline=2, padding=2)
nb1.enable_traversal()

enabler = Button(page1, text='Enable Tab two\n Test it out',
                 command=lambda: nb1.tab(1, state='normal'))
enabler.pack()

root.mainloop()
