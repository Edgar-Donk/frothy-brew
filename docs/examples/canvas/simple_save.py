from tkinter import Tk, Canvas
root = Tk()
canvas = Canvas(root)
canvas.pack()
rect = canvas.create_rectangle(10,10,100,100, fill="blue")
retval = canvas.postscript(file="../../images/canvas/saved.ps", height=100, width=100, colormode="color")
root.mainloop()