from tkinter import Tk, Canvas
can_width = 380
can_height = 270
X0 = 20
Y0 = 20
X1 = 110
Y1 = 110

def callback(event):
    global X0, Y0, X1, Y1
    for search in can.find_closest(event.x, event.y):
        foundling = can.gettags(search)
        if foundling[0] == 'ring':
            event.y = min(max(event.y,10), can_height-10 )
            can.move(search, 0, event.y-Y0)
            #X0 = event.x
            Y0 = event.y
        elif foundling[0] == 'square':
            event.x = min(max(event.x,20), can_width-20 )
            can.move(search, event.x-X1, 0)
            X1 = event.x
            #Y1 = event.y

root = Tk()
can = Canvas(root)
can.bind('<B1-Motion>', callback)
can.pack()

r = 10
circle = can.create_oval(X0-r, Y0-r, X0+r, Y0+r, fill='orange', tags='ring')
r = 20
square = can.create_rectangle(X1-r, Y1-r, X1+r, Y1+r, fill='pink', tags='square')

root.mainloop()
