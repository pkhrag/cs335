from config import *

f = open('output.asm', 'w')

# TODO
# Currently in intel format, need to change to at&t
def initializeGlobals():
    symbolList = ST.globalSymbolList
    f.write('section     .data\n\n')
    for x in symbolList:
        if ST.table[x]["type"] == "int":
            f.write(x+"     dw"+"     0\n")


# at&t format
def genInstr(instr):
    f.write('\t' + instr + '\n')
