from tkinter import Tk, Canvas

can_width = 380
can_height = 270
s0 = 50, 50
s1 = 350, 250
rectx = s0[0]
recty = s1[1]

def callback(event):
    can.update()
    can_height = can.winfo_reqheight()

    for search in can.find_closest(event.x, event.y):
        global recty, rectx
        foundling = can.gettags(search)
        if foundling[0] == 'harrow':
            X = event.x
            #Y = event.y
            Y = s0[1]
            #rectx = X
            X = max(X,10)
            can.move(search, X-rectx, 0)
            can.delete('square', 'varrow')
            can.create_rectangle((X,s0[1]), (s1[0], recty), width=2, tags='square')

            Y = recty
            can.create_polygon([X,Y-10,X-5,Y-5,X-2,Y-5,X-2,Y+5,
                X-5,Y+5,X,Y+10,X+5,Y+5,X+2,Y+5,X+2,Y-5,X+5,Y-5],
                fill='lawn green',outline='lawn green', width=2,
                tags=('varrow'), activefill='red')
            rectx = X

        elif foundling[0] == 'varrow':
            Y = event.y
            X = rectx
            #recty = Y
            Y = min(Y,can_height-10)
            can.move(search, 0, Y-recty)
            can.delete('square')
            can.create_rectangle((X, s0[1]), (s1[0], Y), width=2, tags='square')
            recty = Y

root = Tk()

can = Canvas(root, width=can_width, height=can_height)
can.bind('<B1-Motion>', callback)
can.pack()


square = can.create_rectangle(s0, s1, width=2, tags='square')

x = rectx
y = s0[1]
can.create_polygon([x-10,y,x-5,y-5,x-6,y-2,x+6,y-2,
            x+5,y-5,x+10,y,x+5,y+5,x+6,y+2,x-6,y+2,x-5,y+5],
            fill='',outline='lawn green',width=2, tags=('harrow'),
            activefill='red')

x = rectx
y = recty
can.create_polygon([x,y-10,x-5,y-5,x-2,y-5,x-2,y+5,
            x-5,y+5,x,y+10,x+5,y+5,x+2,y+5,x+2,y-5,x+5,y-5],
            fill='lawn green',outline='lawn green', width=2,
            tags=('varrow'), activefill='red')

root.mainloop()
