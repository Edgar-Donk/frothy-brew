'''
class has image loss due to garbage collection
alt is problem, drawing based on widget images, allow for scaling
'''

from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk
from tkinter.ttk import Style, Frame, Radiobutton, Label, Checkbutton

from RunStatettk import run_state

# createButtons:
switch = 0

radioimg = {}
# colours from alt

states = ['background', 'active',('active', 'selected'), ('disabled', 'selected'),
             'selected','disabled', ('disabled', 'alternate'), 'alternate',
             'pressed']

rline_colours =  {'selected': {'topleft': "#888888",
                            'botright': 'white',
                            'intopleft': "#414141",
                            'inbotright': "#d9d9d9"},
                'alternate': {'topleft': "#888888",
                            'botright': "#888888",
                            'intopleft': "#414141",
                            'inbotright': "#d9d9d9"},
                'active': {'topleft': "#888888",
                            'botright': 'white',
                            'intopleft': "#414141",
                            'inbotright': "#ececec"},
    ('active', 'selected'): {'topleft': "#888888",
                            'botright': 'white',
                            'intopleft': "#414141",
                            'inbotright': "#ececec"},
                'disabled': {'topleft': "#888888",
                            'botright': None,
                            'intopleft': "#aaaaaa",
                            'inbotright': None},
                'pressed': {'topleft': "#888888",
                            'botright': None,
                            'intopleft': "#414141",
                            'inbotright': None},
                'background': {'topleft': "#888888",
                            'botright': 'white',
                            'intopleft': "#414141",
                            'inbotright': "#d9d9d9"},
   ('disabled', 'alternate'): {'topleft': "#888888",
                            'botright': "#aaaaaa",
                            'intopleft': "#414141",
                            'inbotright': "#d9d9d9"},
   ('disabled', 'selected'): {'topleft': "#888888",
                            'botright': "#aaaaaa",
                            'intopleft': "#414141",
                            'inbotright': None}
                            }

imagebg = {'selected': 'white',
            'alternate': "#aaaaaa", 'active': 'white',
            ('active', 'selected'): 'white',
            'disabled': "#d9d9d9", 'pressed': "#d9d9d9",
            'background': 'white', ('disabled', 'alternate'): "#d9d9d9",
            ('disabled', 'selected'): "#d9d9d9"}

outerbg = {'selected': "#d9d9d9",
            'alternate': "#d9d9d9", 'active': "#ececec",
            ('active', 'selected'): "#ececec",
            'disabled': "#d9d9d9", 'pressed': "#d9d9d9",
            'background': "#d9d9d9", ('disabled', 'alternate'): "#d9d9d9",
            ('disabled', 'selected'): "#d9d9d9"}

def circle(dr, center, radius, fill):
    dr.ellipse((center[0] - radius, center[1] - radius,
                center[0] + radius - 1, center[1] + radius - 1),
               fill=fill, outline=None)

# create pieslice with centre and radius, assume only fill used
def pie(idraw,c,r,fill='#888888',start=180,end=270):
    return idraw.pieslice([c[0]-r,c[1]-r,c[0]+r-1,c[1]+r-1],
                          fill=fill,start=start,end=end)


def rdraw_widgets(scaling):
    width, height = int(12 * scaling), int(12 * scaling)
    b = int(1 * scaling)

    for ix, state in enumerate(states):
        image = Image.new('RGB', (width,height), outerbg[state])
        idraw = ImageDraw.Draw(image)

        pie(idraw, [width//2, height//2], width//2,
            fill=rline_colours[state]['topleft'], start=135, end=315)

        if rline_colours[state]['botright']:
            pie(idraw, [width//2, height//2], width//2,
            fill=rline_colours[state]['botright'], start=315, end=135)

        pie(idraw, [width//2, height//2], width//2-b,
            fill=rline_colours[state]['intopleft'], start=135, end=315)

        if rline_colours[state]['inbotright']:
            pie(idraw, [width//2, height//2], width//2-b,
            fill=rline_colours[state]['inbotright'], start=315, end=135)

        circle(idraw, (width//2, height//2), width//2-2*b,
            fill=imagebg[state])

        if state in ('selected',('disabled','selected'),
                    ('active', 'selected')):
            circle(idraw, (width//2, height//2), 2*b, fill='#a3a3a3' \
                if state == ('disabled','selected') else 'black')

        radioimg[state] = ImageTk.PhotoImage(image)

def show_widgets(fr, scaling):
    st0 = Style()

    st0.theme_create( "altflex", parent="alt", settings={

        'Radiobutton.indicator': {"element create":
                ('image', radioimg['background'],
                ('disabled', 'selected', radioimg[('disabled', 'selected')]),
                ('disabled', radioimg['disabled']),
                ('disabled', 'alternate', radioimg[('disabled', 'alternate')]),
                ('alternate', radioimg['alternate']),
                ('pressed', radioimg['pressed']),
                ('active', 'selected', radioimg[('active', 'selected')]),
                ('selected', radioimg['selected']),
                ('active', radioimg['active']),
                { 'sticky': "w", 'padding':3*scaling})
                }})

    st0.theme_use('altflex')
    st0.map('TRadiobutton', background=[('active',"#ececec")])

    def change():
        global switch
        if switch == 0:
            widg.state(['disabled']) # active
            print(widg.state())
        else:
            widg.state(['!disabled']) # !active
        switch = 1 if switch == 0 else 0

    widg = Radiobutton(fr, text='Cheese' ,width=-8, value=1)
    widg1 = Radiobutton(fr, text='Tomato' ,width=-8, value=2)
    widg.grid(column=0,row=15,sticky='nsew', padx=5, pady=5)
    widg1.grid(column=0,row=16,sticky='nsew', padx=5, pady=5)

    label = Label(root, text='selected', \
            image=radioimg[('selected')], compound='left')
    label.image = radioimg['selected']
    label.grid(column=0,row=17,sticky='nsew', padx=5, pady=5)

    c = Checkbutton(root, text='disabled', command=change)
    c.grid(column=0, row=18, pady=5)
    run_state(fr,widg,widg1)

if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    dpi_scaling = int(scaling / BASELINE + 0.5)
    fr0 = Frame(root)
    fr0.grid(column=0,row=0,sticky='nsew')
    rdraw_widgets(dpi_scaling)
    show_widgets(fr0, dpi_scaling)

    root.mainloop()
