from tkinter import Tk, Canvas

def callback(event):
    for search in can.find_closest(event.x, event.y):
        foundling = can.gettags(search)
        if foundling[0] == 'ring':
            can.coords(search, event.x-20, event.y-20, event.x+20, event.y+20)
        elif foundling[0] == 'square':
                can.coords(search, event.x-10, event.y-10, event.x+10, event.y+10)

root = Tk()
can = Canvas(root)
can.bind('<B1-Motion>', callback)
#can.bind('<B1-Button>', callback)
can.pack()

circle = can.create_oval(0, 0, 40, 40, fill='orange', tags='ring')
square = can.create_rectangle(100, 100, 120, 120, fill='pink', tags='square')

root.mainloop()
