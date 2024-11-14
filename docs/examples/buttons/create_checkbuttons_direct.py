from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk
from tkinter.ttk import Style, Frame, Checkbutton, Label

checkimg = {}
switch = 0

states = ['background', 'active', ('disabled', 'selected'), ('active', 'selected'),
             'selected','disabled', ('disabled', 'alternate'), 'alternate',
             'pressed']

line_colours = {'selected': {'topleft': "#888888",
                            'botright': None,
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
                            'inbotright': None},
   ('disabled', 'selected'): {'topleft': "#888888",
                            'botright': None,
                            'intopleft': "#aaaaaa",
                            'inbotright': None}
                            }

imagebg = {'selected': 'white', 'alternate': "#aaaaaa",
    'active': 'white', 'disabled': "#d9d9d9", 'pressed': "#d9d9d9",
    'background': 'white', ('disabled', 'alternate'): "#d9d9d9",
    ('disabled', 'selected'): "#d9d9d9", ('active', 'selected'): 'white'}

def draw_widgets(scaling):
    width, height = int(15*scaling), int(15*scaling)
    b = int(1*scaling)

    for ix, state in enumerate(states):
        image = Image.new('RGB', (width,height), imagebg[state])
        idraw = ImageDraw.Draw(image)

        idraw.line([(0,(b-1)//2), (width-b-1,(b-1)//2)], width=b,
            fill=line_colours[state]['topleft'])
        idraw.line([((b-1)//2,0), ((b-1)//2,height-b-1)], width=b,
            fill=line_colours[state]['topleft'])

        if line_colours[state]['botright']:
            idraw.line([(0,height-1-b//2), (width-1,height-1-b//2)], width=b,
                fill=line_colours[state]['botright'])
            idraw.line([(width-1-b//2,0), (width-1-b//2,height-1)], width=b,
                fill=line_colours[state]['botright'])

        idraw.line([(b,b+(b-1)//2), (width-2*b-1,b+(b-1)//2)], width=b,
            fill=line_colours[state]['intopleft'])
        idraw.line([(b+(b-1)//2,b), (b+(b-1)//2,height-2*b-1)], width=b,
            fill=line_colours[state]['intopleft'])

        if line_colours[state]['inbotright']:
            idraw.line([(b,height-1-b//2-b), (width-b-1,height-1-b//2-b)], width=b,
                fill=line_colours[state]['inbotright'])
            idraw.line([(width-1-b//2-b,b), (width-1-b//2-b,height-b-1)], width=b,
                fill=line_colours[state]['inbotright'])

        if state in ('selected',('disabled','selected')):
            # tick
            idraw.line([4*b, 6*b, 4*b, 9*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([5*b, 7*b, 5*b, 10*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([6*b, 8*b, 6*b, 11*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([7*b, 7*b, 7*b, 10*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([8*b, 6*b, 8*b, 9*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([9*b, 5*b, 9*b, 8*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)
            idraw.line([10*b, 4*b, 10*b, 7*b],
                fill='black' if state == 'selected' else '#a3a3a3', width=b)

        checkimg[state] = ImageTk.PhotoImage(image)

def show_widgets(fr, scaling):
    st0 = Style()

    st0.theme_create( "altflex", parent="alt", settings={

        'Checkbutton.indicator': {"element create":
                ('image', checkimg['background'],
                ('disabled', 'selected', checkimg[('disabled', 'selected')]),
                ('disabled', checkimg['disabled']),
                ('pressed', checkimg['pressed']),
                ('disabled', 'alternate', checkimg[('disabled', 'alternate')]),
                ('alternate', checkimg['alternate']),
                #('active', 'selected', checkimg[('active', 'selected')]),
                #('active', checkimg['active']),
                ('selected', checkimg['selected']),
                { 'sticky': "w", 'padding':3*scaling})
                }})

    st0.theme_use('altflex')
    st0.map('TCheckbutton', background=[('active',"#ececec")])
    st0.map('TRadiobutton', background=[('active',"#ececec")])

    def change():
        global switch
        if switch == 0:
            widg.state(['disabled']) # active
            #print(widg.state())
        else:
            widg.state(['!disabled']) # !active
        switch = 1 if switch == 0 else 0

    widg = Checkbutton(fr, text='Cheese' ,width=-8)
    widg1 = Checkbutton(fr, text='Tomato' ,width=-8)
    widg.grid(column=0,row=15,sticky='nsew', padx=5, pady=5)
    widg1.grid(column=0,row=16,sticky='nsew', padx=5, pady=5)

    #run_state(fr,widg,widg1)
    c = Checkbutton(root, text='disable/enable top checkbutton', command=change)
    c.grid(column=0, row=17, pady=5, sticky='w')
    label = Label(root, text='selected image on label', \
            image=checkimg[('selected')], compound='left')
    #label.image = checkimg['selected']
    label.grid(column=0,row=18,sticky='nsew', padx=5, pady=5)

if __name__ == "__main__":
    root = Tk()
    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    dpi_scaling = int(scaling / BASELINE + 0.5)
    fr0 = Frame(root)
    fr0.grid(column=0,row=0,sticky='nsew')
    draw_widgets(dpi_scaling)
    show_widgets(fr0, dpi_scaling)

    root.mainloop()
