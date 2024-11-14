from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Radiobutton, Checkbutton, Separator, Style
        
class run_state():
    def __init__(self, fr, widg, widg1=None):
        ''' Used to enable state change

        Creates radio buttons showing states
        Creates check button with "Enabled", useful for testing
            check and radio buttons

        Args:
            fr: frame reference in calling program
            widg: widget reference
            widg1: optional widget
        '''
        self.fr = fr
        self.widg = widg
        self.widg1 = widg1

        # Create radio buttons which will display widget states
        states = ['active', ('active', 'selected'),'alternate', 'background',
                  'disabled', ('disabled', 'alternate'), 'focus', 'invalid',
                  'pressed', 'readonly', ('disabled', 'selected'), 'selected']

        self.rb = []
        self.state_val = StringVar()
        for iy, state in enumerate(states):
            st_rb = Radiobutton(fr, value=state, text=state,
                variable=self.state_val, command=self.change_state)
            st_rb.grid(column=0,row=iy+2,padx=5,pady=5, sticky='nw')
            self.rb.append(st_rb)
        sep = Separator(fr, orient='h')
        sep.grid(column=0,row=14,sticky='ew')

    def change_state(self):
        ''' used to enable state change'''
        newstate = self.state_val.get()
        oldstate = self.widg.state()
        # Check and Radio buttons start with alternate state
        # prefix oldstate with !
        oldst = [f"!{s}" for s in oldstate]
        # convert tuple to string
        oldst = " ".join(oldst)
        self.widg.state([oldst])
        # if newstate is compound run each part separately
        if ' ' in newstate:
            newstate, nstate = newstate.split()
            self.widg.state([newstate])
            self.widg.state([nstate])
        else:
            self.widg.state([newstate])

if __name__ == '__main__':
    root = Tk()
    st0 = Style()
    st0.theme_use('alt')
    fr1 = Frame()
    fr1.grid(column=0,row=0,sticky='nsew')

    Widg = Checkbutton(fr1,text='Checkbutton')
    Widg.grid(column=0,row=15)
    Widg1 = Checkbutton(fr1,text='Another one')
    Widg1.grid(column=0,row=16)
    run_state(fr1,Widg,Widg1)
    root.mainloop()
