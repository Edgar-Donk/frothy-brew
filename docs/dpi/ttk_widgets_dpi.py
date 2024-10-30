from tkinter import Tk, IntVar, StringVar, TclError, font
from tkinter.ttk import Frame, Checkbutton, Button, Separator, \
Radiobutton, LabelFrame, Label, Entry, Style, Combobox
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def _show_vars():
    # set text for labels in var_panel to include the control
    # variable name and current variable value
    vb0['text'] = '{:<11} {:<8}'.format('enabled:', enabled.get())
    vb1['text'] = '{:<11} {:<8}'.format('cheese:', cheese.get())
    vb2['text'] = '{:<11} {:<8}'.format('tomato:', tomato.get())
    vb3['text'] = '{:<11} {:<8}'.format('basil:', basil.get())
    vb4['text'] = '{:<11} {:<8}'.format('oregano:', oregano.get())
    vb5['text'] = '{:<11} {:<8}'.format('happiness:', happiness.get())

def change_style(event=None):
    """set the Style to the content of the Combobox"""
    content = cb.get()
    st0.theme_use(content)
    st0.configure('TCheckbutton', font=20, indicatorsize=20, indicatordiameter=20)
    st0.configure('TRadiobutton', font=20, indicatorsize=20, indicatordiameter=20)
    root.title(content)

root = Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
#root.tk.call('tk', 'scaling', SCALE)
root.tk.call('tk', 'scaling', 2.7)

st0 = Style()
st0.configure('TCheckbutton', font=11)

# frame to hold contents
frame = Frame(root, name='descrip')

# widgets to be displayed on 'Description' tab
# position and set resize behaviour

frame.rowconfigure(1, weight=1)
frame.columnconfigure((0,1), weight=1, uniform=1)
frame.pack()
lf = LabelFrame(frame, text='Animals')
lf.pack(pady=5,padx=5,side='left',fill='y')
beasts = ['horse','elephant',
                  'crocodile','bat','grouse']
ttkbut = []
for t in beasts:
    b = Button(lf, text=t)
    b.pack(pady=2)
    ttkbut.append(b)

lF2 = LabelFrame(frame,text="Theme Listbox")
lF2.pack(pady=5,padx=5)
themes = list(sorted(st0.theme_names())) # get_themes
#print(themes)
themes.insert(0, "Pick a theme")
cb = Combobox(lF2, values=themes, state="readonly", height=10)

cb.set(themes[0])
cb.bind('<<ComboboxSelected>>', change_style)
cb.grid(row=0,column=0,sticky='nw', pady=5)

lF3 = LabelFrame(frame,text="Entry")
lF3.pack(anchor='n')
en = Entry(lF3)
en.grid(row=0,column=0,sticky='ew', pady=5, padx=5)

lf1 = LabelFrame(frame, text='Checkbuttons')
lf1.pack(pady=5,padx=5,side='left',fill='y')

# control variables
enabled = IntVar()
cheese = IntVar()
tomato = IntVar()
basil = IntVar()
oregano = IntVar()
# checkbuttons
cbOpt = Checkbutton(lf1, text='Enabled', variable=enabled, style='TCheckbutton')
cbCheese = Checkbutton(text='Cheese', variable=cheese, command=_show_vars,
            style='TCheckbutton')
cbTomato = Checkbutton(text='Tomato', variable=tomato, command=_show_vars,
            style='TCheckbutton')
sep1 = Separator(orient='h')
cbBasil = Checkbutton(text='Basil', variable=basil, command=_show_vars,
            style='TCheckbutton')
cbOregano = Checkbutton(text='Oregano', variable=oregano, command=_show_vars,
            style='TCheckbutton')
sep2 = Separator(orient='h')

cbs = [cbOpt, cbCheese, cbTomato, cbBasil, cbOregano] # sep1, sep2
for opt in cbs:
    #if opt.winfo_class() == 'TCheckbutton':
    opt.configure(onvalue=1, offvalue=0)
    opt.setvar(opt.cget('variable'), 0)

    opt.pack(in_=lf1, side='top', fill='x', pady=2, padx=5, anchor='nw')

lf2 = LabelFrame(frame, text='Radiobuttons', labelanchor='n')
lf2.pack(pady=5,padx=5,side='left',fill='y')

rb=[]
happiness = StringVar()
for s in ['Great', 'Good', 'OK', 'Poor', 'Awful']:
    b = Radiobutton(lf2, text=s, value=s,
        variable=happiness,  style='TRadiobutton',
        command=lambda s=s: _show_vars())
    b.pack(anchor='nw', side='top', fill='x', pady=5,padx=5)

right = LabelFrame(frame, text='Control Variables')
right.pack(pady=5,padx=5,side='left',fill='y')

vb0 = Label(right, font=('Courier', 10))
vb1 = Label(right, font=('Courier', 10))
vb2 = Label(right, font=('Courier', 10))
vb3 = Label(right, font=('Courier', 10))
vb4 = Label(right, font=('Courier', 10))
vb5 = Label(right, font=('Courier', 10))

vb0.pack(anchor='nw', pady=5,padx=5)
vb1.pack(anchor='nw', pady=5,padx=5)
vb2.pack(anchor='nw', pady=5,padx=5)
vb3.pack(anchor='nw', pady=5,padx=5)
vb4.pack(anchor='nw', pady=5,padx=5)
vb5.pack(anchor='nw', pady=5,padx=5)

_show_vars()

root.mainloop()