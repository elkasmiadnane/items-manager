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

    def _insert_to_db(self):
        dictItem = {'id':self.id,
                    'name' :self.name,
                    'link' :self.link,
                    'exists' :'yes',
                    'status' :self.status}
        db = DB.insert_row(dictItem)

    def _delete_from_db(self,row:int):
        db = DB.delete_row(row)


