from tkinter import Tk, Checkbutton, StringVar
import pprint

root = Tk()

# making checkbutton
option_var = StringVar()

checkbutton = Checkbutton(root, text='abc', variable = option_var, onvalue='hi',
                offvalue='bye', height=30)

checkbutton.pack()

pprint.pprint(checkbutton.config()) # displays the configuration options of the widget


root.mainloop()