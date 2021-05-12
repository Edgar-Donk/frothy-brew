'''
integer entry allowing additional characters
'''

from tkinter import Tk
from tkinter.ttk import Entry, Style
    
root = Tk()
s = Style()
s.theme_use('default')

def isOkay(act, inp, text): # 
    print(inp)
    #if act == '1':
    '''
        if text in '0123456789.-+':
            try:
                float(inp)
                #if 1<float(inp)<63:
                    #return True
                #else:
                    #return False
            except ValueError:
                return False
        else:
            return False
    '''
    if inp == "" or inp == "-"  or inp == "." or inp == "-.": # and len(inp) == 1
        return True
    if isinstance(inp, float):
        float(inp)
        print('ok')
        #if -10<float(inp)<63:
            #return True
        #else:
            #return False
        return True
    else:
        return False
    #if 10<float(inp)<63:
        #return True
    #else:
        #return False
    
    #else:
        #True
    
#    elif len(inp) == 0:
#        return True
    

vcmd = root.register(isOkay) # 
en = Entry(root,validate = "key",validatecommand=(vcmd, '%d', '%P', '%S'))
en.pack(padx=10)

root.mainloop()