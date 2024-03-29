from tkinter import Tk
from tkinter.ttk import Style, Scale
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)

root.geometry("+500+300")
st = Style()
# print(st.theme_names())
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
# 9, 30, 9, 30, 30, ?, ? about half the width of vista
theme = 'default'
st.theme_use('default')

def start_s(evt):
    # find slider width

    X = evt.x
    Y = evt.y

    comp = sc.identify(X,Y)
    print(X,Y, 'X,Y')
    print(sc.identify(X,Y)) # -->slider or trough

    if comp == 'slider':
        while str(comp) == 'slider':
            X -= 1
            comp = sc.identify(X,Y)
            print(X, comp)

        print('X', X, 'comp', sc.identify(X,Y))
        comp = 'slider'

        while str(comp) == 'slider':
            X += 1
            comp = sc.identify(X,Y)
            print(X, comp)

        print('X', X, 'comp', sc.identify(X,Y), 'theme', theme)


sc = Scale(root, from_=0, to =100, length = 200)
sc.grid(padx=10, pady=10)

sc.bind('<ButtonRelease-1>', start_s)

root.mainloop()