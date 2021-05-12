"""Module containing class Tree, based upon tkinter.ttk treeview.

* The following properties are set:-
* Inserting Data
* Data Selection
* Using Tags
* Sorting Rows by Columns - followed by a reverse sort
* Adding Scrollbars
* Importing Data Headers and Data as a CSV File
* Includes workaround for python 3.7 tag colour display

"""

from tkinter import Tk, StringVar, font
from tkinter.ttk import Frame, Treeview, Style, Label, Scrollbar, Button
import csv

class Tree:
    """Parallel columns within treeview.

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

    def __init__(self, fr, csvFile, csvDelimiter=','):

        self.fr=fr
        self.csvFile=csvFile
        self.csvDelimiter=csvDelimiter
        self.treeData = []
        self.treeSel = []
        self.backg = ["white",'#f0f0ff']

        self.s = s = Style()
        s.theme_use('default')

        s.map('Treeview', foreground=self.fixed_map('foreground'),
            background=self.fixed_map('background'))

        fact = font.Font(font="TkDefaultFont").metrics('linespace')
        s.configure('font.Treeview', rowheight=fact,
                      font=font.nametofont("TkDefaultFont"))

        # determine Heading font based on TkDefaultFont
        def_font = font.nametofont('TkDefaultFont')
        self.font_family = def_font.actual()['family']
        self.font_size = def_font.actual()['size'] + 1
        s.configure('font.Treeview.Heading', font=(self.font_family,self.font_size,'bold'))

        with open(self.csvFile, newline='', encoding='utf-8-sig') as csvfile:
            treeCsv = csv.reader(csvfile, delimiter=self.csvDelimiter)

            for ix, row in enumerate(treeCsv):
                if ix == 0:
                    self.treeColumns = row
                else:
                    self.treeData.append(row)

        self.setup(self.treeColumns, self.treeData)

    def selectItem(self,evt):
        """Function to enable selection.

        Parameters
        ----------
        evt : trigger hook

        Returns
        -------
        string
            Selected row
        """
        # del self.treeSel[:] # delete previous entry
        curItem = self.tree.focus()
        self.treeSel = self.lvar.set(self.tree.item(curItem)['values'])
        return(self.treeSel)

    def sortBy(self,tree, col, descending):
        """Column sorting function.

        Parameters
        ----------
        tree : str
            link to treeview
        col : str
            column selection for sorting
        descending : str
            method of sorting
        """

        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sortBy(tree, col, int(not descending)))

        # reconfigure tags after ordering
        list_of_items = tree.get_children('')
        for i in range(len(list_of_items)):
            tree.tag_configure(list_of_items[i], background=self.backg[i%2])

    def setup(self, treeColumns, treeData):
        """Create Treeview widget.

        Parameters
        ----------
        treeColumns : str
            list of column names
        treeData : str, int, float
            list of tree data

        """
        # create Treeview widget
        tree =self.tree = Treeview(self.fr, column=treeColumns, show='headings',style='font.Treeview')
        tree.grid(column=0, row=0, sticky='nsew')
        tree.bind("<<TreeviewSelect>>", self.selectItem)

        vsb = Scrollbar(self.fr,orient="vertical", command=tree.yview)
        vsb.grid(column=1, row=0, sticky='ns')
        hsb = Scrollbar(self.fr,orient="horizontal", command=tree.xview)
        hsb.grid(column=0, row=1,  sticky='ew')

        tree.configure(xscrollcommand=hsb.set,yscrollcommand=vsb.set)
        self.fr.grid_columnconfigure(0, weight=1)
        self.fr.grid_rowconfigure(0, weight=1)

        # insert header, data and tag configuration
        for ix,col in enumerate(treeColumns):
            tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortBy(tree, c, 0))
            #tree.column(col,stretch=True)
            #tree.column(col,width=font.nametofont('TkHeadingFont').measure(col.title()),
                #stretch=False)
            tree.column(col,width=font.Font(family=self.font_family,size=self.font_size, weight="bold").measure(col.title()) + 10,
                stretch=False)
            #print(tree.column(col))

        # insert data row by row, then measure each items' width
        for ix, item in enumerate(treeData):
            itemID = tree.insert('', 'end', values=item)
            tree.item(itemID, tags=itemID)
            tree.tag_configure(itemID, background=self.backg[ix%2])

            for indx, val in enumerate(item):
                #ilen = font.Font(family="Segoe UI", size=10, weight="normal").measure(val)
                ilen = font.nametofont('TkDefaultFont').measure(val)
                if tree.column(treeColumns[indx], width=None) < ilen +10:
                    tree.column(treeColumns[indx], width=ilen + 10)
                # you should see the widths adjust
                #print('col',tree.column(treeColumns[indx]),ilen)

        # display selection
        self.lvar = StringVar()
        lbl = Label(self.fr, textvariable=self.lvar, text="Ready")
        lbl.grid(column=0, row=2, sticky='nsew')

    def fixed_map(self, option):
        """Fix for setting text colour for Tkinter 8.6.9.

        From: `Tk Source Code View Ticket <https://core.tcl.tk/tk/info/509cafafae>`_

        Parameters
        ----------
        option : str
            foreground, background

        Returns
        -------
        string
            foreground, background
        """
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.s.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]


if __name__ == "__main__":
    root = Tk()
    csvFile = '../csv_data/test.csv'
    csvDelimiter = ';'
    page1 = Frame(root)
    page1.pack(fill='both', expand=False)
    t = Tree(page1,csvFile,csvDelimiter)
    b2=Button(page1,text='Click after selection', command=lambda:print(t.lvar.get()))
    b2.grid(column=0, row=3)

    root.mainloop()
