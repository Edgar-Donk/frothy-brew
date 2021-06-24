from tkinter import Tk, Canvas
from dataclasses import dataclass

@dataclass
class pos:
    __slots__ = ['name', 'xval', 'yval']
    name: str
    xval: int
    yval: int

@dataclass
class dc:
    found: str
    can_width: int = 380
    can_height: int = 270

s0 = pos(name='upper left corner', xval=50, yval=50)
s1 = pos(name='lower right corner', xval=350, yval=250)
#rectx = s0[0]
#recty = s1[1]

def click(event):
    search = can.find_closest(event.x, event.y)
    dc.found = can.gettags(search)[0]

def callback(event):

    if dc.found == 'harrow':
        X = event.x
        #Y = event.y
        Y = s0.yval #s0[1]
        #rectx = X
        X = max(X,10)
        can.move(dc.found, X-s0.xval, 0)
        can.delete('square', 'varrow')
        can.create_rectangle((X,s0.yval), (s1.xval, s1.yval), width=2, tags='square')

        Y = s1.yval
        can.create_polygon([X,Y-10,X-5,Y-5,X-2,Y-5,X-2,Y+5,
            X-5,Y+5,X,Y+10,X+5,Y+5,X+2,Y+5,X+2,Y-5,X+5,Y-5],
            fill='lawn green',outline='lawn green', width=2,
            tags=('varrow'), activefill='red')
        s0.xval = X

    elif dc.found == 'varrow':
            Y = event.y
            X = s0.xval
            #recty = Y
            Y = min(Y,dc.can_height-10)
            can.move(dc.found, 0, Y-s1.yval)
            can.delete('square')
            can.create_rectangle((X, s0.yval), (s1.xval, Y), width=2, tags='square')
            s1.yval = Y

root = Tk()

can = Canvas(root, width=dc.can_width, height=dc.can_height)
can.bind('<B1-Motion>', callback)
can.bind('<ButtonPress-1>', click)
can.pack()


square = can.create_rectangle([s0.xval,s0.yval], [s1.xval,s1.yval], width=2,
    tags='square')

x = s0.xval
y = s0.yval
can.create_polygon([x-10,y,x-5,y-5,x-6,y-2,x+6,y-2,
            x+5,y-5,x+10,y,x+5,y+5,x+6,y+2,x-6,y+2,x-5,y+5],
            fill='',outline='lawn green',width=2, tags=('harrow'),
            activefill='red')

x = s0.xval
y = s1.yval
can.create_polygon([x,y-10,x-5,y-5,x-2,y-5,x-2,y+5,
            x-5,y+5,x,y+10,x+5,y+5,x+2,y+5,x+2,y-5,x+5,y-5],
            fill='lawn green',outline='lawn green', width=2,
            tags=('varrow'), activefill='red')

root.mainloop()
