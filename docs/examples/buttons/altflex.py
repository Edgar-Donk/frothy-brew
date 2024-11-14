from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk
from tkinter.ttk import Style, Frame, Checkbutton

checkimg = {}
radioimg = {}
checkimage = {}
radioimage = {}

states = ['background', 'active', ('disabled', 'selected'), ('active', 'selected'),
             'selected','disabled', ('disabled', 'alternate'), 'alternate',
             'pressed']

def _load_images():
    for iz, state in enumerate(states):
        checkimg[state] = ImageTk.PhotoImage(checkimage[state])
        radioimg[state] = ImageTk.PhotoImage(radioimage[state])

def install():

    root = Tk()

    winsys = root.tk.call("tk", "windowingsystem")
    BASELINE = 1.33398982438864281 if winsys != 'aqua' else 1.000492368291482
    scaling = root.tk.call("tk", "scaling")
    dpi_scaling = int(scaling / BASELINE + 0.5)
    root.destroy()

    chline_colours = {'selected': {'topleft': "#888888",
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

    imagebg = {'selected': 'white', 'alternate': "#aaaaaa",
        'active': 'white', 'disabled': "#d9d9d9", 'pressed': "#d9d9d9",
        'background': 'white', ('disabled', 'alternate'): "#d9d9d9",
        ('disabled', 'selected'): "#d9d9d9", ('active', 'selected'): 'white'}

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


    width, height = int(15*dpi_scaling), int(15*dpi_scaling)
    b = int(1*dpi_scaling)

    for ix, state in enumerate(states):
        image = Image.new('RGB', (width,height), imagebg[state])
        idraw = ImageDraw.Draw(image)

        idraw.line([(0,(b-1)//2), (width-b-1,(b-1)//2)], width=b,
            fill=chline_colours[state]['topleft'])
        idraw.line([((b-1)//2,0), ((b-1)//2,height-b-1)], width=b,
            fill=chline_colours[state]['topleft'])

        if chline_colours[state]['botright']:
            idraw.line([(0,height-1-b//2), (width-1,height-1-b//2)], width=b,
                fill=chline_colours[state]['botright'])
            idraw.line([(width-1-b//2,0), (width-1-b//2,height-1)], width=b,
                fill=chline_colours[state]['botright'])

        idraw.line([(b,b+(b-1)//2), (width-2*b-1,b+(b-1)//2)], width=b,
            fill=chline_colours[state]['intopleft'])
        idraw.line([(b+(b-1)//2,b), (b+(b-1)//2,height-2*b-1)], width=b,
            fill=chline_colours[state]['intopleft'])

        if chline_colours[state]['inbotright']:
            idraw.line([(b,height-1-b//2-b), (width-b-1,height-1-b//2-b)], width=b,
                fill=chline_colours[state]['inbotright'])
            idraw.line([(width-1-b//2-b,b), (width-1-b//2-b,height-b-1)], width=b,
                fill=chline_colours[state]['inbotright'])

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

        checkimage[state] = image

    width, height = int(12 * dpi_scaling), int(12 * dpi_scaling)
    b = int(1 * dpi_scaling)

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

        if state in ('selected',('disabled','selected'), ('active', 'selected')):
            circle(idraw, (width//2, height//2), 2*b, fill='#a3a3a3' \
                if state == ('disabled','selected') else 'black')

        radioimage[state] = image

    _load_images()
    st0 = Style()
    st0.theme_create( "altflex", parent="alt", settings={

        'Checkbutton.indicator': {"element create":
                ('image', checkimg['background'],
                ('disabled', 'selected', checkimg[('disabled', 'selected')]),
                ('disabled', checkimg['disabled']),
                ('pressed', checkimg['pressed']),
                ('disabled', 'alternate', checkimg[('disabled', 'alternate')]),
                ('alternate', checkimg['alternate']),
                ('selected', checkimg['selected']),
                { 'sticky': "w", 'padding':3*dpi_scaling}),
            },

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
                { 'sticky': "w", 'padding':3*dpi_scaling})
            },
        'TCheckbutton': {'map': {'background':[('active',"#ececec")]}},
        'TRadiobutton': {'map': {'background':[('active',"#ececec")]}}

                })


if __name__ == "__main__":
    root = Tk()
    fr0 = Frame(root)
    fr0.grid(column=0,row=0,sticky='nsew')
    st = Style()
    install()
    st.theme_use('altflex')
    widg = Checkbutton(fr0, text='Cheese' ,width=-8)
    widg1 = Checkbutton(fr0, text='Tomato' ,width=-8)
    widg.grid(column=0,row=15,sticky='nsew', padx=5, pady=5)
    widg1.grid(column=0,row=16,sticky='nsew', padx=5, pady=5)

    root.mainloop()

