from tkinter import Tk, Label

Root=Tk()
Root.title("Window")

lab = Label(Root, text = "Test")
lab.pack()
Root.geometry("300x300")

Root.update_idletasks()

def check(event):
    RWidth = Root.winfo_width()
    RHeight = Root.winfo_height()
    print(RWidth, 'RWidth')
    print(RHeight, 'RHeight')

Root.bind("<Configure>",check)
Root.mainloop()