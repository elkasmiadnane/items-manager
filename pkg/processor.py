import re

from pkg.parser import DB,parseId
class Item():
    def __init__(self,id_,name,exists,link,status):
        self.id = id_
        self.name = name
        self.exists = exists
        self.link = link
        self.status = status

class Processor(Item):

    def _check_item_exists(self,item:Item,database:dict) -> Item:
        values = database.keys()
        if(item.id in values):
            itm = database[item.id]
            itm = Processor(item.id,itm['name'],itm['exists'],itm['link'],itm['status'])
            return itm
    def _check_item_partially_exists(self,word:str,database:dict) -> dict:
        itms = {}
        values = database.keys()
        for idx,v in enumerate(values):
            if re.match(f"^{word}",v):
                itm = database[v]
                itm = Processor(v, itm['name'], itm['exists'], itm['link'], itm['status'])
                itms[idx]=itm
            print(itms)
        return itms



    def _insert_to_db(self):
        dictItem = {'id':self.id,
                    'name' :self.name,
                    'exists': self.exists,
                    'link' :self.link,
                    'status' :self.status}
        db = DB.insert_row(dictItem)

    def _update_db(self,idx:int):
        dictItem = {'id':self.id,
                    'name' :self.name,
                    'exists': self.exists,
                    'link' :self.link,
                    'status' :self.status}
        db = DB.modify_row(idx,dictItem)

    def _delete_from_db(self,row:int):
        db = DB.delete_row(row)