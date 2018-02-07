from config import *
import genAsm
import getreg


def codeGen(x, nextUseTable):
	start = x[0]
	end = x[1]
 	# print "heya"
	for lineNo in range(start,end+1):
		# print "hee heya"
		codeGeneratorPerLine(lineNo, nextUseTable)
	
	## Write all the registers back to Memory
	## TODO


def codeGeneratorPerLine(lineNo, nextUseTable):
	
	instrType = "heya"
	## need to segregate instrType on the basis of immediate?
	## long switch case for deciphering the kind of instruction store that in instrType
	def instrTypeFunc(x):
	    return {
	        '+': "add",
	        '-': "sub", # a long switch block TODO
	        'x': "mult",
	        '/': "div",
	        '%': "mod",
	        '&': "and",
	        '|': "or",
	        '^': "xor",
	        '<<': "lsh",
	        '>>': "rsh",
	        '==': "ise",
	        '<': "lt",
	        '>': "gt",
	        '!=': "neq",
	        '<=': "lte",
	        '>=': "gte",
	        '=': "move",
	        '=!': "not",
	        '+=': "add",
	        '-=': "sub",
	        'x': "mult",
	        '/': "idiv",
	        '%=': "mod",
	        '&=': "and",
	        '|=': "or",
	        '^=': "xor",
	        '<<=': "lsh",
	        '>>=': "rsh",
	        '*': "lea",
	        '++': "incr",
	        'label' : "label",
	        'print': "print",
	        'scan' : "scan",
	        'ifgoto': "ifgoto",
	        'callint': "call",
	        'callvoid': "call",
	        'goto': "jmp",
	        'retint': "ret",
	        'retvoid': "ret"

	    }.get(x, "not defined instruction")

 	instrType = instrTypeFunc(ir[lineNo].type)

 	if instrType == "not defined instruction":
 		raise ValueError('Instruction ' + instrType + ' not defined in x86')

	if ir[lineNo].type in type_4:

		locationDst = getreg.getreg(lineNo, nextUseTable)
		# print "heya"
		regSrc1 = addrDes[ir[lineNo].src1]['register']
		if regSrc1 is not None and regSrc1 != locationDst:
			genAsm.genInstr("movl %" + regSrc1 + ", %" + locationDst)
		elif regSrc1 is None and regSrc1 != locationDst:
			genAsm.genInstr("movl $" + ir[lineNo].src1 + ", %" + locationDst)


		regSrc2 = addrDes[ir[lineNo].src2]['register']
		if regSrc2 == None:
			genAsm.genInstr(instrType + " $" + ir[lineNo].src2 + ", %" + locationDst)
		else:
			genAsm.genInstr(instrType + " %" + regSrc2 + ", %" + locationDst)


		addrDes[ir[lineNo].dst]['register'] = locationDst
		addrDes[ir[lineNo].dst]['memory'] = False

		for x in regDes:
			if regDes[x] == ir[lineNo].dst:
				regDes[x] = None
		regDes[locationDst] = ir[lineNo].dst

		if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
			for x in regDes:
				if regDes[x] == ir[lineNo].src1:
					regDes[x] = None

		if nextUseTable[lineNo][ir[lineNo].src2]['nextUse'] is None:
			for x in regDes:
				if regDes[x] == ir[lineNo].src2:
					regDes[x] = None
	





	elif ir[lineNo].type in type_3:

		## ifgoto type
		if ir[lineNo].type == 'ifgoto':
			pass
			##TODO

		## immediate instructions a+=3 types
		elif check_int(ir[lineNo].src1):
			locationDst = getreg.getreg(lineNo, nextUseTable)
			isRegDst = addrDes[ir[lineNo].dst]['register']
			if isRegDst is None:
				genAsm.genInstr(instrType + " $" + str(locationDst) + ", $" + ir[lineNo].dst)
			else:
				genAsm.genInstr(instrType + " $" + str(locationDst) + ", %" + isRegDst)

			## if destination is not used next
			if nextUseTable[lineNo][ir[lineNo].dst]['nextUse'] is None:
				for x in regDes:
					if regDes[x] == ir[lineNo].dst:
						regDes[x] = None
		
		else:
			locationDst = getreg.getreg(lineNo, nextUseTable)
			
			## function call
			if locationDst == 'eax':
				pass
				##TODO

			## in general a+=b type instructions
			else:
				isRegSrc = addrDes[ir[lineNo].src1]['register']
			
				## if source variable is in memory	
				if isRegSrc is None:
					
					genAsm.genInstr(instrType + " $" + ir[lineNo].src1 + ", %" + locationDst)
					addrDes[ir[lineNo].dst]['register'] = locationDst
					addrDes[ir[lineNo].dst]['memory'] = False
					

				## if source variable is in register already
				else :
					genAsm.genInstr(instrType + " %" + isRegSrc + ", %" + locationDst)

				## delete register occurrences if source variable is not used again in bbl
				if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
					for x in regDes:
						if regDes[x] == ir[lineNo].src1:
							regDes[x] = None



	elif ir[lineNo].type in type_2:

		if ir[lineNo].type in ["++","--"]:

			isRegDst = addrDes[ir[lineNo].dst]['register']

			## if in memory directly use incr a.
			if isRegDst is None:
				genAsm.genInstr(instrType + " $" + ir[lineNo].dst)

			## else increment a in register
			else:
				genAsm.genInstr(instrType + " %" + ir[lineNo].dst)

		elif ir[lineNo].type == 'label':
			pass
			#TODO
		elif ir[lineNo].type == 'print':
			pass
			#TODO
		elif ir[lineNo].type == 'scan':
			pass
			#TODO
		elif ir[lineNo].type == 'callvoid':
			pass
			#TODO
		elif ir[lineNo].type == 'goto':
			pass
			#TODO
		elif ir[lineNo].type == 'retint':
			pass
			#TODO


	elif ir[lineNo].type in type_1:
		pass
		#TODO for retvoid


				