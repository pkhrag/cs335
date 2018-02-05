

def initializeGlobals(ST):

	symbolList = ST.globalSymbolList
	with open('output.asm','w') as f:
		f.write('section     .data\n\n')
		f.write('heyaa')
