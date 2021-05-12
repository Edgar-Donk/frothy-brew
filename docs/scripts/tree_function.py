"""ttk tkinter treeview
    displays table of data in columns, loading from csv file,
    sorts data by column, selection of row

  Parameters
  ----------
  fr : str
    The parent tk widget, normally a Frame.
  csvFile : str
    csv file name to be imported
  outVar : str
    Name of tkvariable that contains output
  csvDelimiter : str
    Type of csv delimiter, defaults to ','

  Returns
  -------
  string
    Information in outVar
  """
from tkinter import Tk, StringVar, font
from tkinter.ttk import Frame, Treeview, Style, Label, Scrollbar, Button
import csv

def fixed_map(s,option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in s.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

def Tree(fr,outVar):
    s = Style()
    s.theme_use('default')

    s.map('Treeview', foreground=fixed_map(s,'foreground'),
            background=fixed_map(s,'background'))

    test_length = font.Font(family="Times", size=12, weight="bold").measure('Test')
    fact = int(test_length / 30 * 20.45) # 30 is the length of Test in Idle

    s.configure('Treeview', rowheight= fact)

    s.configure('font.Treeview', font='TkDefaultFont')
    # determine Heading font based on TkDefaultFont
    s.configure('font.Treeview', font='TkDefaultFont')
    def_font = font.nametofont('TkDefaultFont')
    font_family = def_font.actual()['family']
    font_size = def_font.actual()['size'] + 1
    s.configure('font.Treeview.Heading', font=(font_family,font_size,'bold'))

    # function to enable selection
    def selectItem(evt):
        curItem = tree.focus()
        lvar.set(tree.item(curItem)['values'])
        outVar.set(tree.item(curItem)['values'])

    def sortBy(tree, col, descending):
        # When a column is clicked on sort tree contents .
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: sortBy(tree, col, int(not descending)))

        # reconfigure tags after ordering
        list_of_items = tree.get_children('')
        for i in range(len(list_of_items)):
            tree.tag_configure(list_of_items[i], background=backg[i%2])

    # headings and data
    treeColumns = ['Colours', 'Hash', 'RGB', 'Extra long header']

    treeData = (('red', '#FF0000', (255,0,0)),
            ('yellow', '#FFFF00', (255,255,0)),
            ('blue', '#0000FF', (0,0,255)),
            ('green', '#00FF00', (0,255,0)),
            ('magenta', '#FF00FF', (255,0,255)),
            ('cyan', '#00FFFF', (0,255,255)),
            ('foo', 'bar', 'bong', 'ding a ling ping'))

    backg = ["white",'#f0f0ff']

    # create Treeview widget
    tree = Treeview(fr, column=treeColumns, show='headings',style='font.Treeview')
    tree.grid(column=0, row=0, sticky='nsew')
    tree.bind("<<TreeviewSelect>>", selectItem)

    vsb = Scrollbar(fr,orient="vertical", command=tree.yview)
    vsb.grid(column=1, row=0, sticky='ns')
    hsb = Scrollbar(fr,orient="horizontal", command=tree.xview)
    hsb.grid(column=0, row=1,  sticky='ew')

    tree.configure(xscrollcommand=hsb.set,yscrollcommand=vsb.set)
    fr.grid_columnconfigure(0, weight=1)
    fr.grid_rowconfigure(0, weight=1)

    # insert header, data and tag configuration
    for ix,col in enumerate(treeColumns):
        tree.heading(col, text=col.title(),
            command=lambda c=col: sortBy(tree, c, 0))
        #tree.column(col,stretch=True)
        #tree.column(col,width=font.nametofont('TkHeadingFont').measure(col.title()),
                #stretch=False)
        tree.column(col,width=font.Font(family=font_family,size=font_size, weight="bold").measure(col.title()) + 10,
                stretch=False)
        #print(tree.column(col))

    # insert data row by row, then measure each items' width
    for ix, item in enumerate(treeData):
        itemID = tree.insert('', 'end', values=item)
        tree.item(itemID, tags=itemID)
        tree.tag_configure(itemID, background=backg[ix%2])

        for indx, val in enumerate(item):
            #ilen = font.Font(family="Segoe UI", size=10, weight="normal").measure(val)
            ilen = font.nametofont('TkDefaultFont').measure(val)
            if tree.column(treeColumns[indx], width=None) < ilen +10:
                tree.column(treeColumns[indx], width=ilen + 10)
            # you should see the widths adjust
            #print('col',tree.column(treeColumns[indx]),ilen)

    # display selection
    lvar = StringVar()
    lbl = Label(fr, textvariable=lvar, text="Ready")
    lbl.grid(column=0, row=2, sticky='nsew')

if __name__ == "__main__":
    root = Tk()
    #csvFile = '../csv/test.csv'
    #csvDelimiter = ';'
    page1 = Frame(root)
    page1.pack(fill='both', expand=False)
    outVar = StringVar()
    t = Tree(page1,outVar)
    b2=Button(page1,text='Click after selection', command=lambda:print(outVar.get()))
    b2.grid(column=0, row=3)

    root.mainloop()
    #parser = optparse.OptionParser()
