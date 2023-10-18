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

configMode = False
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
            global database
            itm.id = parseId(itm.name)
            if (itm._check_item_exists(itm,database) is not None):
                itm = itm._check_item_exists(itm,database)
                lbl.config(text=f'Status :{itm.name} existing')
                lbl.config(fg='green')
                itm.exists = 'yes'
                secondaryWindow = Tk()
                secondaryWindow.geometry('100x70')
                secondaryWindow.overrideredirect(True)
                secondaryWindow.configure(bg='green')
                screen_width = secondaryWindow.winfo_screenwidth()
                screen_height = secondaryWindow.winfo_screenheight()

                # calculate position x and y coordinates
                x = screen_width -100
                y = screen_height - 70

                for rng in range (y):

                    secondaryWindow.after(2,secondaryWindow.geometry(f"+{x}+{rng}"))

                secondaryWindow.geometry('%dx%d+%d+%d' % (100, 70, x, y))

                def close_after_2s():
                    secondaryWindow.destroy()

                secondaryWindow.after(1500, close_after_2s)
                secondaryWindow.mainloop()
                update_infos(itm)
                return itm

            else:
                lbl.config(text=f'Status :{itm.name} non existing')
                lbl.config(fg='red')
                itm.exists = 'no'
                nameEntry.delete(0, END)
                nameEntry.insert(0, itm.name)


        def check_item_from_entry():
            if(entry.get() == '' or entry.get() is None):messagebox.showwarning(title="warning", message="field empty")
            itm = Processor(None, entry.get(), None, None, None)
            check_item(itm)

        def check_copied_item(i:str):
            itm = Processor(None,i,None,None,None)
            check_item(itm)

        def update_infos(itm:Item):
            global database
            if itm is not None:
                indx = int(database[itm.id]['index']) - 1
                itm.id = parseId(itm.name)
                list_of_elements.see(indx)
                list_of_elements.select_set(indx, indx)
                nameEntry.delete(0, END)
                nameEntry.insert(0,itm.name)
                existslbl.config(text=f'Exists ? : {itm.exists}')
                statuslbl.config(text=f'Status   : {itm.status}')
                linkEntry.delete(0, END)
                linkEntry.insert(0, str(itm.link))
                statusEntry.delete(0, END)
                statusEntry.insert(0, str(itm.status))

        def update_database():
            global configMode
            if configMode:
                itm = Processor(0,nameEntry.get(),True,linkEntry.get(),statusEntry.get())
                print(itm)

        def refresh_and_show():
            global database
            list_of_elements.delete(0,END)
            list_of_elements.focus()
            database = DB.getDB(None)
            for index, line in enumerate(database.values()):
                list_of_elements.insert(int(line['index']), f'{line["name"]}')
        def selection_callback(event):
            id_ = list_of_elements.curselection()[0]
            selection = str(list_of_elements.get(id_,id_)[0])
            if selection:
                check_copied_item(selection)

        def enter_config_mode():
            global configMode
            if config['relief'] == 'raised':
                config.config(relief=SUNKEN)
                configMode = True
            else:
                config.config(relief=RAISED)
                configMode = False
        def update_config_mode():
            if configMode:
                global database
                itm = Processor(parseId(nameEntry.get()),nameEntry.get(),None,None,None)
                itm._insert_to_db()
                database[itm.id] = {"index":int(len(database) + 1),
                                "id" : itm.id,
                               "name" : itm.name ,
                               "exists" : "yes" ,
                               "link" : itm.link ,
                               "status" : itm.status}
                updatelbl.config(text="Inserted",fg='red')
                time.sleep(0.8)
                updatelbl.place_configure(height=0)
                refresh_and_show()
                update_infos(itm)

            else:
                lbl.config(text='Please activate config mode')
        def delete_config_mode():
            if configMode:
                itm = Processor(parseId(nameEntry.get()),nameEntry.get(),None,None,None)
                itm._delete_from_db()
            else:
                lbl.config(text='Please activate config mode',highlightcolor='red')

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Objects in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list_of_elements = Listbox(window,name="list", width=50, height=30)
        list_of_elements.bind('<<ListboxSelect>>',selection_callback)
        entry = Entry(window, bd=5)
        refreshButton = Button(window, text='Refresh', command=refresh_and_show)
        check = Button(window, text='check', command=check_item_from_entry)
        lbl = Label(window,text='Status : ')

        namelbl = Label(window,text='Name   : ')
        nameEntry = Entry(window,width=60)
        existslbl = Label(window,text='Exists ? :')
        linklbl = Label(window,text='Link : ')
        linkEntry = Entry(window,width=60)
        statuslbl = Label(window,text='Status   : ')
        statusEntry = Entry(window,width=60)

        config = Button(window,text='Config Mode',command=enter_config_mode)
        update = Button(window,text='Update',command=update_config_mode)
        delete = Button(window,text='Delete',command=delete_config_mode)

        updatelbl = Label(window)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Placement in the Gui
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        list_of_elements.place(x=10, y=10)
        entry.place(x=320, y=10)
        check.place(x=320, y=50)
        lbl.place(x=320, y=80)
        refreshButton.place(x=160, y=510)

        namelbl.place(x=320,y=150)
        nameEntry.place(x=370,y=150)
        existslbl.place(x=320,y=170)
        linklbl.place(x=320,y=190)
        linkEntry.place(x=370,y=190)
        statuslbl.place(x=320,y=210)
        statusEntry.place(x=370,y=210)
        config.place(x=800,y=5)
        update.place(x=750,y=145)
        delete.place(x=110, y=510)

        updatelbl.place(x=750,y=175)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # loop to detect copy string event
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        def detect():
            recent_value = ""
            flag = False
            while True:
                tmp_value = pyperclip.paste()
                if tmp_value != recent_value:
                    recent_value = tmp_value
                    if flag:
                        check_copied_item(recent_value)
                    flag = True
                time.sleep(0.1)

        t1 = Thread(target=detect)
        t1.start()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # first run call
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        refresh_and_show()

        window.mainloop()