from tkinter import Tk, Canvas

def callback(event):
    #can.update()
    #can_width = can.winfo_reqwidth()
    #can_height = can.winfo_reqheight()

    for search in can.find_closest(event.x, event.y):
        foundling = can.gettags(search)
        if foundling[0] == 'ring':
            event.x = (c0[0] + c1[0])/2
            event.y = min(max(event.y,20), can_height-20 )
            can.coords(search, event.x-20, event.y-20, event.x+20, event.y+20)
        elif foundling[0] == 'square':
            event.y = (s0[1] + s1[1])/2
            event.x = min(max(event.x,10), can_width-10 )
            can.coords(search, event.x-10, event.y-10, event.x+10, event.y+10)

root = Tk()
can_width = 380
can_height = 270
can = Canvas(root, width=can_width, height=can_height)
can.bind('<B1-Motion>', callback)
#can.bind('<Button>', find)
can.pack()

c0 = 0, 0
c1 = 40, 40
s0 = 100, 100
s1 = 120, 120
circle = can.create_oval(c0, c1, fill='orange', tags='ring')
square = can.create_rectangle(s0, s1, fill='pink', tags='square')

root.mainloop()
