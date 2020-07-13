from tkinter import Tk, StringVar, font
from tkinter.ttk import Frame, Treeview, Style, Label, Scrollbar, Button
import csv

class Tree:
    def __init__(self,fr0,csv_file,csv_delimiter=','):
        """tkinter ttk treeview
        Shows data in parallel columns, selection, zebra stripes,
        column sorting, adjusting heading, column widths and row heights,
        scrollbars, convert to class
        includes workaround for python 3.7 tag colour display

        Parameters
        ----------
        fr0 : str
            The parent tk widget, normally a Frame.
        csv_file : str
            csv file name to be imported
        out_var : str
            Name of tkvariable that contains output
        csv_delimiter : str
            Type of csv delimiter, defaults to ','

        Returns
        -------
        string
            Information in out_var
        """

        self.fr0=fr0
        self.csv_file=csv_file
        self.csv_delimiter=csv_delimiter
        self.tree_data = []
        self.treeSel = []
        self.backg = ["white",'#f0f0ff']

        self.st1 = st1 = Style()
        st1.theme_use('default')

        st1.map('Treeview', foreground=self.fixed_map('foreground'),
            background=self.fixed_map('background'))

        if font.Font(family="Times", size=12, weight="bold").measure('Test') == 66:
            st1.configure('Treeview', rowheight=45) #

        st1.configure('font.Treeview', font='TkDefaultFont')
        # determine Heading font based on TkDefaultFont
        st1.configure('font.Treeview', font='TkDefaultFont')
        def_font = font.nametofont('TkDefaultFont')
        self.font_family = def_font.actual()['family']
        self.font_size = def_font.actual()['size'] + 1
        st1.configure('font.Treeview.Heading', font=(self.font_family,self.font_size,'bold'))

        with open(self.csv_file, newline='', encoding='utf-8-sig') as csvfile:
            treeCsv = csv.reader(csvfile, delimiter=self.csv_delimiter)

            for ix, row in enumerate(treeCsv):
                if ix == 0:
                    self.tree_columns = row
                else:
                    self.tree_data.append(row)

        self.setup(self.tree_columns, self.tree_data)

    def select_item(self,evt):
        """ function to enable selection

        Parameters
        ----------
        evt : trigger hook

        Returns
        -------
        string
            Selection
        """
        # del self.treeSel[:] # delete previous entry
        curItem = self.tree.focus()
        self.treeSel = self.lvar.set(self.tree.item(curItem)['values'])
        return(self.treeSel)

    def sort_by(self,tree, col, descending):
        """Column sorting function

        Parameters
        ----------
        tree : str
            link to treeview
        col : str
            column selection for sorting
        descending : str
            method of sorting

        Returns
        -------
            None
        """

        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # reorder data
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

        # switch the heading so that it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: self.sort_by(tree, col, int(not descending)))

        # reconfigure tags after ordering
        list_of_items = tree.get_children('')
        for i in range(len(list_of_items)):
            tree.tag_configure(list_of_items[i], background=self.backg[i%2])

    def setup(self, tree_columns, tree_data):
        """Create Treeview widget

        Parameters
        ----------
        tree_columns : str
            list of column names
        tree_data : str, int, float
            list of tree data

        Returns
        -------
            None
        """
        # create Treeview widget
        tree =self.tree = Treeview(self.fr0, column=tree_columns, show='headings',style='font.Treeview')
        tree.grid(column=0, row=0, sticky='nsew')
        tree.bind("<<TreeviewSelect>>", self.select_item)

        vsb = Scrollbar(self.fr0,orient="vertical", command=tree.yview)
        vsb.grid(column=1, row=0, sticky='ns')
        hsb = Scrollbar(self.fr0,orient="horizontal", command=tree.xview)
        hsb.grid(column=0, row=1,  sticky='ew')

        tree.configure(xscrollcommand=hsb.set,yscrollcommand=vsb.set)
        self.fr0.grid_columnconfigure(0, weight=1)
        self.fr0.grid_rowconfigure(0, weight=1)

        # insert header, data and tag configuration
        for ix,col in enumerate(tree_columns):
            tree.heading(col, text=col.title(),
                command=lambda c=col: self.sort_by(tree, c, 0))
            #tree.column(col,stretch=True)
            #tree.column(col,width=font.nametofont('TkHeadingFont').measure(col.title()),
                #stretch=False)
            tree.column(col,width=font.Font(family=self.font_family,size=self.font_size, weight="bold").measure(col.title()) + 10,
                stretch=False)
            #print(tree.column(col))

        # insert data row by row, then measure each items' width
        for ix, item in enumerate(tree_data):
            item_ID = tree.insert('', 'end', values=item)
            tree.item(item_ID, tags=item_ID)
            tree.tag_configure(item_ID, background=self.backg[ix%2])

            for indx, val in enumerate(item):
                #ilen = font.Font(family="Segoe UI", size=10, weight="normal").measure(val)
                ilen = font.nametofont('TkDefaultFont').measure(val)
                if tree.column(tree_columns[indx], width=None) < ilen +10:
                    tree.column(tree_columns[indx], width=ilen + 10)
                # you should see the widths adjust
                #print('col',tree.column(tree_columns[indx]),ilen)

        # display selection
        self.lvar = StringVar()
        lbl = Label(self.fr0, textvariable=self.lvar, text="Ready")
        lbl.grid(column=0, row=2, sticky='nsew')

    def fixed_map(self, option):
        """Fix for setting text colour for Tkinter 8.6.9
        From: https://core.tcl.tk/tk/info/509cafafae

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
        return [elm for elm in self.st1.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]


if __name__ == "__main__":
    root = Tk()
    csv_file = '../../csv/test.csv'
    csv_delimiter = ';'
    page1 = Frame(root)
    page1.pack(fill='both', expand=False)
    t = Tree(page1,csv_file,csv_delimiter)
    b2=Button(page1,text='Click after selection', command=lambda:print(t.lvar.get()))
    b2.grid(column=0, row=3)

    root.mainloop()
