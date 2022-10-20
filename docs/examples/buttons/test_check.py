'''
test checkbuttons - use the properties of the theme to check for
active, selected
disabled, alternate
disabled, selected
'''
from tkinter import Tk
from tkinter.ttk import Style, Checkbutton, Button, Label

switch = 0

def change():
    global switch
    if switch == 0:
        c1.state(['disabled']) # active
        #print(c1.state())
    else:
        c1.state(['!disabled']) # !active
    switch = 1 if switch == 0 else 0

def look():
    print(c1.state())
    lb1['text'] = c1.state()

root = Tk()

s = Style()
s.theme_use('alt')

c = Checkbutton(root, text='disabled', command=change)
c.grid(column=0, row=0, pady=5, sticky='w')
l = Label(root, text= 'Checkbutton to disable/enable\n the button below')
l.grid(column=1, row=0, pady=5, padx=5, sticky='w')
c1 = Checkbutton(root, text='good')
c1.grid(column=0, row=1, pady=5, sticky='w')
l1 = Label(root, text= 'Checkbutton being tested')
l1.grid(column=1, row=1, pady=5, padx=5, sticky='w')
c2 = Checkbutton(root, text='OK')
c2.grid(column=0, row=2, pady=5, sticky='w')
c3 = Checkbutton(root, text='poor')
c3.grid(column=0, row=3, pady=5, sticky='w')

b = Button(root, text='lookup', command=look)
b.grid(column=0, row=3, pady=5, sticky='w')
lb = Label(root, text= 'Show current state')
lb.grid(column=1, row=3, pady=5, padx=5, sticky='w')
lb1 = Label(root, text= 'Current state')
lb1.grid(column=1, row=4, pady=5, padx=5, sticky='w')

root.mainloop()