from tkinter import Button, Tk, Label

root = Tk()

but = Button(root, height=2, width=10, bg='yellow')
but.pack(padx=40, pady=40)

lab0 = Label(root, text='N')
lab0.place(in_=but,  bordermode='outside', relx=0.5, rely=0, anchor='s')

lab1 = Label(root, text='W')
lab1.place(in_=but,  bordermode='outside', relx=0, rely=0.5, anchor='e')

lab2 = Label(root, text='E')
lab2.place(in_=but,  bordermode='outside', relx=1, rely=0.5, anchor='w')

lab3 = Label(root, text='S')
lab3.place(in_=but,  bordermode='outside', relx=0.5, rely=1, anchor='n')

root.mainloop()