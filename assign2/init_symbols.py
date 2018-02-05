from config import *


def initializeGlobals():

	symbolList = ST.globalSymbolList
	with open('output.asm','w') as f:
		f.write('section     .data\n\n')
		for x in symbolList:
			if ST.table[x]["type"] == "int":
				f.write(x+"     dw"+"     0\n")

