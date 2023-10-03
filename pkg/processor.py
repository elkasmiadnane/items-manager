from pkg.parser import DB
class Item():
    def __init__(self,id_,name,exists,link,status):
        self.id = id_
        self.name = name
        self.exists = exists
        self.link = link
        self.status = status

class Processor(Item):

    def _check_item_exists(self,item:Item,database:dict):
        values = database.keys()
        if(item.id in values):
            return True
        return False
    def _insert_to_db(self,item:Item):
        print("Inserting")



