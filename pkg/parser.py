import re
import openpyxl as xl

db = './input/db.xlsx'
wb = xl.load_workbook(db)
ws = wb.active

dbObject = {}

def parseId(name:str):
    id = re.sub("\.","",
            re.sub("-","",
                re.sub(" ","",
                       re.sub("_","",name))))
    return id
def dbToDict():
    counter = 0
    for index,row in enumerate(ws):
        #print (index)
        name = row[0].value
        id = parseId(name)
        exists = row[1].value
        link = row[2].value
        status = row[3].value
        if index > 0:
            if id not in dbObject.keys():
                counter = counter + 1
                dbObject[id] = {"index":int(counter),
                                "id" : id,
                               "name" : name ,
                               "exists" : exists ,
                               "link" : link ,
                               "status" : status}
            else:print("Already exists", index,id)


    print(dbObject)
    return dbObject
class DB():
    def getDB(self):
        database = dbToDict()
        return database