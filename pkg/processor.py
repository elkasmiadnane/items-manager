class Item():
    def __init__(self,repr,name):
        self.repr = repr
        self.name = name

class Processor(Item):

    def find(self) -> bool:

        with open('./input/repo.txt', 'r+') as repo:
            content = repo.read()
        repo.close()
        if content.__contains__(self.name):
            self.exists = True
        else:
            self.exists = False

        return self.exists
    def insert(self):
        if not(self.find(self.name)):
            with open('./input/repo.txt','a') as repo:
                repo.write(f"\n{self.name}")
        else:print(self.name,"already exists!")

