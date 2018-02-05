from config import *


# Initializes addrDes
def createAddrDesc():
    table = ST.globalSymbolList

    for symbol in table:
        if ST.table[symbol]['type'] != 'void':
            addrDes[symbol] = {"register": None, "memory": None}

# finds and returns an empty register. returns None if not exist.
def emptyReg():
    for key, value in regDes.iteritems():
        if key != 'esp' and key != 'ebp':
            if value == None:
                return key
    return None

def getreg(instr, nextUseTable):
    pass
