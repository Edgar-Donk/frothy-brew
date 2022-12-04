from tkinter import Tk, Canvas, Button
from PIL import Image
from io import BytesIO

'''
def circular_arc(canvas,x,y,r,t0,t1,width,colour='black',tags=''):
       # 0° is vertically upwards, t0 start, t1 end
        # extent measured anticlockwise from start along x-axis
        # x,y centre, r radius
        return canvas.create_arc(x-r, y-r, x+r+1, y+r+1, start=t0, extent=t1,
                        style='arc', width=width, outline=colour,tags=tags)
'''

def save():
    ps = canvas.postscript(colormode='color',pagewidth=w-1,pageheight=h-1)
    img = Image.open(BytesIO(ps.encode('utf-8')))
    img.save('../../images/canvas/circle_test.png')

w = 200
h = 200

root = Tk()
canvas = Canvas(root, width=w, height=h, bg='white')
canvas.grid()

canvas.create_oval(0, 0, w+4, h+4, outline='black')

but = Button(root, text="save", command=save)
but.grid()

root.mainloop()
