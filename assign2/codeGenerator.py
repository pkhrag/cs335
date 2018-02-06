from config import *
import genAsm
import getreg


def codeGen(x, nextUseTable):
	start = x[0]
	end = x[1]
	for lineNo in (start,end):
		codeGeneratorPerLine(lineNo, nextUseTable)
	forceGenerate(end) #last line of basic block that doesn't needs use of nextUseTable
	# Write all the registers back to Memory


def codeGeneratorPerLine(lineNo, nextUseTable):
	
	string instrType = None
	## long switch case for deciphering the kind of instruction store that in instrType
	def instrTypeFunc(x):
    return {
        '+': add,
        '-': sub, # a long switch block TODO
    }.get(x, None)



	if ir[lineNo].type in type_4:

		locationDst = getreg.getreg(lineNo, nextUseTable)

		regSrc1 = addrDes[ir[lineNo].src1]['register']
		if regSrc1 is not None and regSrc1 != locationDst:
			genAsm.genInstr("movl %" + regSrc1 + ", %" + locationDst)
		elif regSrc1 is None and regSrc1 != locationDst:
			genAsm.genInstr("movl $" + regSrc1 + ", %" + locationDst)


		regSrc2 = addrDes[ir[lineNo].src2]['register']
		if regSrc2 == None:
			genAsm.genInstr(instrType + " $" + regSrc2 + ", %" + locationDst)
		else:
			genAsm.genInstr(instrType + " %" + regSrc2 + ", %" + locationDst)


		addrDes[ir[lineNo].dst]['register'] = locationDst
		addrDes[ir[lineNo].dst]['memory'] = False

		for x in regDes:
			if regDes[x] == ir[lineNo].dst
				regDes[x] = None
		regDes[locationDst] = ir[lineNo].dst

		if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
			for x in regDes:
				if regDes[x] == ir[lineNo].src1
					regDes[x] = None

		if nextUseTable[lineNo][ir[lineNo].src2]['nextUse'] is None:
			for x in regDes:
				if regDes[x] == ir[lineNo].src2
					regDes[x] = None

	elif ir[lineNo].type in type_3:
		











