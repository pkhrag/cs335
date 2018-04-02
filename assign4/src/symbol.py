
class symbolTable:

    def __init__(self):
        self.table = {}
        self.globalSymbolList = []
        self.parent = None

    # Checks whether "name" lies in the symbol table
    def lookUp(self, name):
        return (name in self.table)

    # Inserts if already not present
    def insert(self, name, typeOf):
        if (not self.lookUp(name)):
            (self.table)[name] = {}
            self.globalSymbolList.append(name)
            (self.table)[name]["type"] = typeOf

    # Returns the argument list of the variable else returns None
    # Note that type is always a key in argument list
    def getInfo(self, name):
        if(self.lookUp(name)):
            return (self.table)[name]

        return None

    # Updates the variable of NAME name with arg list of KEY key with VALUE value
    def updateArgList(self, name, key, value):
        if (self.lookUp(name)):
            (self.table)[name][key] = value
        else:
            print ("Key Error Symbol name doesn't exists - Cant Update")


    def setParent(self, parent):
        self.parent = parent

