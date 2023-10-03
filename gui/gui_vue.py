import warnings

import time
import pyperclip
from pkg.processor import Processor
from pkg.parser import DB,parseId
from pkg.processor import Item
from tkinter import *
from tkinter import messagebox

from threading import Thread

database = DB.getDB(None)
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
        def check_item(itm:Item):
            print('Fired')
            itm.id = parseId(itm.name)
            if (itm._check_item_exists(itm,database)):
                lbl.config(text=f'Status :{itm.name} existing')
                lbl.config(fg='green')
                update_infos(itm)
            else:
                lbl.config(text=f'Status :{itm.name} non existing')
                lbl.config(fg='red')
        def check_item_from_entry():
            if(entry.get() == '' or entry.get() is None):messagebox.showwarning(title="warning", message="field empty")
            itm = Processor(None, entry.get(), None, None, None)
            check_item(itm)

        def check_copied_item(i:str):
            itm = Processor(None,i,None,None,None)
            check_item(itm)

        def update_infos(itm:Item):
            indx = int(database[itm.id]['index']) - 1
            itm.id = parseId(itm.name)
            list_of_elements.see(indx)
            list_of_elements.select_set(indx, indx)
            namelbl.config(text=f'{itm.name}')
            linklbl.config(text=f'{itm.link}')
            statuslbl.config(text=f'{itm.status}')

        def refresh_and_show():
            list_of_elements.delete(1,END)
            database = DB.getDB(None)
            for index, line in enumerate(database.values()):
                list_of_elements.insert(int(line['index']), f'{int(line["index"])} - {line["name"]}')
        def selection_callback(event):
            selection = list_of_elements.curselection()
            print(' ------ ',selection)
            if selection:
                print('selection fired')
                update_infos(check_copied_item(str(selection)))
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Objects in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list_of_elements = Listbox(window,name="list", width=30, height=30)
        list_of_elements.bind("<<ListBoxSelect>>",selection_callback)
        entry = Entry(window, bd=5)
        refreshButton = Button(window, text='Refresh', command=refresh_and_show)
        check = Button(window, text='check', command=check_item_from_entry)
        lbl = Label(window,text='Status : ')

        namelbl = Label(window,text='Name : ')
        linklbl = Label(window,text='Link : ')
        statuslbl = Label(window,text='Status : ')

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Placement in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list_of_elements.place(x=10, y=10)
        entry.place(x=290, y=10)
        check.place(x=270, y=50)
        lbl.place(x=290, y=80)
        refreshButton.place(x=200, y=10)

        namelbl.place(x=290,y=150)
        linklbl.place(x=290,y=170)
        statuslbl.place(x=290,y=190)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # loop to detect copy string event
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        def detect():
            recent_value = ""
            while True:
                tmp_value = pyperclip.paste()
                if tmp_value != recent_value:
                    recent_value = tmp_value
                    print(recent_value)
                    check_copied_item(recent_value)
                time.sleep(0.1)

        t1 = Thread(target=detect)
        t1.start()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # first run call
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        refresh_and_show()

        window.mainloop()
