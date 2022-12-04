from PIL import ImageGrab
from tkinter import Canvas,Tk

def getter(canvas):
    x=root.winfo_rootx()+canvas.winfo_x()
    y=root.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()*2
    y1=y+canvas.winfo_height()*2
    #print(canvas.winfo_width(),canvas.winfo_height())

    #print(x,y,x1,y1)
    ImageGrab.grab((x,y,x1,y1)).save("../../images/canvas/test_circle_tk.png")



# create circle with centre and radius
def create_circle(canvas,c,r,outline='#888888',fill='#888888'):
    return canvas.create_oval([c[0]-r,c[1]-r,c[0]+r,c[1]+r], # c[0]+r-1,c[1]+r-1],
                          outline=outline,fill=fill)

w=21*9
h=21*9
c=w//2,h//2
r=w//2

this_color = "#00A2E8"
background='white'

root=Tk()
root.geometry('300x300+0+0')
#root.update_idletasks()
root.overrideredirect(1)
canvas=Canvas(root,height=h,width=w,bd=0,highlightthickness=0,bg='red')

canvas.pack(side='right', expand='yes', fill='both')

create_circle(canvas,c,r,outline='',fill=this_color)
#print(w,h)
root.update()
#print(canvas.winfo_width(),canvas.winfo_height())
getter(canvas)

root.overrideredirect(0)
root.mainloop()