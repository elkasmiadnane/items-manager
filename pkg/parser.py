import re
import openpyxl as xl

db = './input/db.xlsx'
wb = xl.load_workbook(db)
ws = wb.active

def parseId(name:str):
    id = re.sub("\.","",
            re.sub("-","",
                re.sub(" ","",
                       re.sub("_","",name))))
    return id
def dbToDict():
    dbObject = {}
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

    def insert_row(data:dict):
        rowIndex = int(ws.max_row+1)
        ws.insert_rows(rowIndex)
        for col, value in enumerate(data.values()):
            ws.cell(row=rowIndex, column=col+1, value= '' if value is None else str(value))
            print(str(value))

        wb.save(db)

    def delete_row(row:int):
        ws.delete_rows(row,1)