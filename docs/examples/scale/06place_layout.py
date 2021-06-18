from tkinter import Button, Tk, Label

root = Tk()

but = Button(root, height=2, width=10, bg='yellow')
but.pack(padx=40, pady=40)

l0 = Label(root, text='N')
l0.place(in_=but,  bordermode='outside', relx=0.5, rely=0, anchor='s')

l1 = Label(root, text='W')
l1.place(in_=but,  bordermode='outside', relx=0, rely=0.5, anchor='e')

l2 = Label(root, text='E')
l2.place(in_=but,  bordermode='outside', relx=1, rely=0.5, anchor='w')

l3 = Label(root, text='S')
l3.place(in_=but,  bordermode='outside', relx=0.5, rely=1, anchor='n')

root.mainloop()