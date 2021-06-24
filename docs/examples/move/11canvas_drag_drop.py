from tkinter import Tk, Canvas

X = 40
Y = 40

def callback(event):
    global X, Y
    drag(event.x-X, event.y-Y)
    X = event.x
    Y = event.y

def drag(dx, dy):
    can.move(circle, dx, dy)

root = Tk()
can = Canvas(root)
can.bind('<B1-Motion>', callback)
# can.bind('<B1-Button>', callback)
#can.bind('<Button>', find)
can.pack()

r=30
circle = can.create_oval(X-r, Y-r, X+r, Y+r, outline='orange', width=3,
    activeoutline='red')

root.mainloop()
