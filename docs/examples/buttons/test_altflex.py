from tkinter import Tk
from tkinter.ttk import Style, Frame, Checkbutton, Radiobutton, Label

import altflex

switch = 0

def change():
    global switch
    if switch == 0:
        widg.state(['disabled']) # active
        widg2.state(['disabled'])
        #print(widg.state())
    else:
        widg.state(['!disabled']) # !active
        widg2.state(['!disabled'])
    switch = 1 if switch == 0 else 0

root = Tk()

st = Style()
altflex.install()
st.theme_use('altflex')

fr0 = Frame(root)
fr0.grid(column=0,row=0,sticky='nsew')

widg = Checkbutton(fr0, text='Cheese' ,width=-8)
widg1 = Checkbutton(fr0, text='Tomato' ,width=-8)
widg.grid(column=0,row=15,sticky='nsew', padx=5, pady=5)
widg1.grid(column=0,row=16,sticky='nsew', padx=5, pady=5)

c = Checkbutton(fr0, text='disable/enable\n top checkbutton\n top radiobutton',
    command=change, width=-8)
c.grid(column=0, row=17, pady=5, sticky='nsew')

widg2 = Radiobutton(fr0, text='Ketchup' ,width=-8, value=1)
widg3 = Radiobutton(fr0, text='OK Sauce' ,width=-8, value=2)
widg2.grid(column=0,row=18,sticky='nsew', padx=5, pady=5)
widg3.grid(column=0,row=19,sticky='nsew', padx=5, pady=5)

root.mainloop()