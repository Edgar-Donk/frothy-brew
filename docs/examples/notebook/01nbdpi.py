
"""Basic notebook with 3 tabs """

from tkinter import Tk, Frame, font
from tkinter.ttk import Notebook, Style
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
ORIGINAL_DPI = 96
current_dpi = root.winfo_fpixels('1i')
SCALE = current_dpi / ORIGINAL_DPI
print(SCALE)
# when current_dpi is 192 SCALE becomes 2.0
root.tk.call('tk', 'scaling', SCALE)
st1 = Style()
st1.theme_use('default')

test_size = font.Font(family="Times", size=12, weight="bold").measure('Test')
mult = int(test_size / 30)

nb1 = Notebook(root)
page1 = Frame(root, background='red', height=20*mult)
page2 = Frame(root, background='yellow', height=20*mult)
page3 = Frame(root, background='alice blue', height=20*mult)
nb1.grid(row=0, column=0)
nb1.add(page1, text='one')
nb1.add(page2, text='two')
nb1.add(page3, text='three')

root.mainloop()
