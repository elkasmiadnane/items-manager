import warnings

from pkg.processor import Processor
from pkg.processor import Item
from tkinter import *
from tkinter import messagebox

class Gui():
    def __init__(self, size, title):
        self.size = size
        self.title = title

    def executeGui(self):
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Initialization
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        window = Tk()
        window.geometry(str(self.size))
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Functions of Objects
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        def checkItem():
            if(entry.get() == '' or entry.get() is None):messagebox.showwarning(title="warning", message="field empty")
            else:
                itm = Processor(None,str(entry.get()))
                if (itm.find()):
                    lbl.config(text='Status : existing')
                    lbl.config(fg='green')
                else:
                    lbl.config(text='Status : non existing')
                    lbl.config(fg='red')

        def refreshAndShow():
            list.delete(0, END)
            with open('./input/repo.txt', 'r+') as repo:
                content = repo.readlines()
                for index, line in enumerate(content):
                    list.insert(index, line)
        def selectionCallback(event):
            selection = event.widget.curselection()
            if selection:
                print(selection)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Objects in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list = Listbox(window, width=30, height=30)
        entry = Entry(window, bd=5)
        refreshButton = Button(window, text='Refresh', command=refreshAndShow)
        check = Button(window, text='check', command=checkItem)
        lbl = Label(window,text='Status : ')
        list.bind("<<ListBoxSelect>>",selectionCallback)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Placement in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list.place(x=10, y=10)
        entry.place(x=290, y=10)
        check.place(x=290, y=50)
        lbl.place(x=290, y=80)
        refreshButton.place(x=200, y=10)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # first run call
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        refreshAndShow()

        window.mainloop()