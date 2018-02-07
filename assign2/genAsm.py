from config import *

f = open('output.S', 'w')

# TODO
# Currently in intel format, need to change to at&t
def initializeGlobals():
    symbolList = ST.globalSymbolList
    f.write('.data\n\n')
    for x in symbolList:
        if ST.table[x]["type"] == "int":
            f.write( x +":\n\t.int\t0\n")
    f.write('\n.text\n\n.global main\n\nmain:\n\n')


# at&t format
def genInstr(instr):
    f.write('\t' + instr + '\n')

def closeFile():
	# f.write('\\n')
	genInstr("movl $0, %ebx")
	genInstr("movl $1, %eax")
	genInstr("int $0x80")
	f.close()
