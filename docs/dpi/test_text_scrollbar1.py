from tkinter import *
ws1 = Tk()
ws1.title('Third Example of Tkinter Scrollbar')
ws1.config(bg='#7FFFD4')
frame = Frame(
    ws1,
    bg='#FF0000'
    )
text1_box = Text(
    ws1,
    height=12,
    width=39,
    font=(14)
)
text1_box.grid(row=0, column=0)
text1_box.config(bg='#F0F8FF')
sb = Scrollbar(
    ws1,
    orient=VERTICAL
    )
sb.grid(row=0, column=1, sticky=NS)
text1_box.config(yscrollcommand=sb.set)
sb.config(command=text1_box.yview)
ws1.mainloop()