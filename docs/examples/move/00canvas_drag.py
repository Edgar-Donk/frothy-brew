from tkinter import Tk, Canvas, Label

def callback(event):
    draw(event.x, event.y)

def draw(x, y):
    can.coords(circle, x-20, y-20, x+20, y+20)

root = Tk()
lab = Label(root, text='Drag the cursor into the empty frame')
lab.pack()
can = Canvas(root)
can.bind('<Motion>', callback)
can.pack()

circle = can.create_oval(0, 0, 0, 0, fill='orange')
#poly = can.create_polygon((0, 0, 0, 0, 0, 0), fill="#4eccde")
root.mainloop()
