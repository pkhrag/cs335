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
	for reg, symbol in regDes.iteritems():
		if symbol is not None:
			genAsm.genInstr('movl %' + reg + ', ' + symbol)
	## TODO


def codeGeneratorPerLine(lineNo, nextUseTable):
	
	instrType = "heya"
	## need to segregate instrType on the basis of immediate?
	## long switch case for deciphering the kind of instruction store that in instrType
	def instrTypeFunc(x):
		return {
			'+': "addl",
			'-': "subl", # a long switch block TODO
			'x': "imul",
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
			'=': "movl",
			'=!': "not",
			'+=': "add",
			'-=': "sub",
			'x': "mult",
			'/': "div",
			'%=': "mod",
			'&=': "and",
			'|=': "or",
			'^=': "xor",
			'<<=': "lsh",
			'>>=': "rsh",
			'*': "lea",
			'++': "inc",
			'--': "dec",
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
			genAsm.genInstr("movl (" + ir[lineNo].src1 + "), %" + locationDst)
		else:
			if addrDes[ir[lineNo].src1]['memory'] is False:
				genAsm.genInstr("movl %" + regSrc1 + ", " + ir[lineNo].src1)
				regDes[regSrc1] = ir[lineNo].dst
				addrDes[ir[lineNo].src1]['register'] = None
				addrDes[ir[lineNo].src1]['memory'] = True

		regSrc2 = addrDes[ir[lineNo].src2]['register']
		if regSrc2 == None:
			genAsm.genInstr(instrType + " (" + ir[lineNo].src2 + "), %" + locationDst)
		else:
			genAsm.genInstr(instrType + " %" + regSrc2 + ", %" + locationDst)

# TODO:- what if x is not in register
		addrDes[ir[lineNo].dst]['register'] = locationDst
		addrDes[ir[lineNo].dst]['memory'] = False

		for x in regDes:
			if regDes[x] == ir[lineNo].dst:
				regDes[x] = None
		regDes[locationDst] = ir[lineNo].dst

		# if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
		# 	for x in regDes:
		# 		if regDes[x] == ir[lineNo].src1:
		# 			regDes[x] = None

		# if nextUseTable[lineNo][ir[lineNo].src2]['nextUse'] is None:
		# 	for x in regDes:
		# 		if regDes[x] == ir[lineNo].src2:
		# 			regDes[x] = None
	





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
				genAsm.genInstr(instrType + " $" + str(locationDst) + ", " + ir[lineNo].dst)
			else:
				genAsm.genInstr(instrType + " $" + str(locationDst) + ", %" + isRegDst)

			## if destination is not used next
			# if nextUseTable[lineNo][ir[lineNo].dst]['nextUse'] is None:
			# 	for x in regDes:
			# 		if regDes[x] == ir[lineNo].dst:
			# 			regDes[x] = None
		
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
					
					genAsm.genInstr(instrType + " (" + ir[lineNo].src1 + "), %" + locationDst)
					addrDes[ir[lineNo].dst]['register'] = locationDst
					addrDes[ir[lineNo].dst]['memory'] = False
					

				## if source variable is in register already
				else :
					if locationDst != isRegSrc:
						genAsm.genInstr(instrType + " %" + isRegSrc + ", %" + locationDst)
						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False
					else:
						genAsm.genInstr("movl %" + isRegSrc + ", " + ir[lineNo].src1)
						addrDes[ir[lineNo].src1]['register'] = None
						addrDes[ir[lineNo].src1]['memory'] = True
						
				## delete register occurrences if source variable is not used again in bbl
				# if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
				# 	for x in regDes:
				# 		if regDes[x] == ir[lineNo].src1:
				# 			regDes[x] = None

	elif ir[lineNo].type in type_2:

		if ir[lineNo].type in ["++","--"]:

			isRegDst = addrDes[ir[lineNo].dst]['register']

			## if in memory directly use incr a.
			if isRegDst is None:
				genAsm.genInstr(instrType + " " + ir[lineNo].dst)

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


				