from config import *
import genAsm
import getreg


def codeGen(x, nextUseTable):
	start = x[0]
	end = x[1]
 	# print "heya"
	flag = 0
	if ir[end].type == 'retint' or ir[end].type == 'retvoid' or ir[end].type == 'goto' or ir[end].type == 'callint' or ir[end].type == 'callvoid'  :
		flag = 1

	for lineNo in range(start,end+1-flag):
		genAsm.genInstr("# " + ir[lineNo].instr)
		# print "hee heya"
		codeGeneratorPerLine(lineNo, nextUseTable)

	## Write all the registers back to Memory
	for reg, symbol in regDes.iteritems():
		if symbol is not None and addrDes[symbol]['memory'] is False:
			genAsm.genInstr('movl %' + reg + ', ' + symbol)
						# regDes[reg] = None
						#  addrDes[symbol]['register'] = None
			addrDes[symbol]['memory'] = True

	if flag:
		genAsm.genInstr("# " + ir[end].instr)
		codeGeneratorPerLine(end, nextUseTable)

comparators = ['<=','>=','<','>','==','!=']

def codeGeneratorPerLine(lineNo, nextUseTable):

	instrType = "heya"
	## need to segregate instrType on the basis of immediate?
	## long switch case for deciphering the kind of instruction store that in instrType
	def instrTypeFunc(x):
		return {
			'+': "addl",
			'-': "subl",
			'x': "imul", #todo
			'/': "div", #todo
			'%': "mod", #todo
			'&': "and", #todo
			'|': "or", #todo
			'^': "xor", #todo
			'==': "cmp", 
			'<': "cmp",
			'>': "cmp",
			'!=': "cmp",
			'<=': "cmp",
			'>=': "cmp",
			'=': "movl",
			'=!': "not",#todo
			'+=': "addl",
			'-=': "subl",
			'x=': "imul",#todo
			'/': "div",#todo
			'%=': "mod",#todo
			'&=': "and",#todo
			'|=': "or",#todo
			'^=': "xor",#todo
			'*': "lea",#todo
			'++': "inc",#todo
			'--': "dec",#todo
			'label' : "label",
			'print': "print",#todo
			'scan' : "scan",#todo
			'ifgoto': "ifgoto",#todo
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

		regSrc1 = addrDes[ir[lineNo].src1]['register']
		locationDst = getreg.getreg(lineNo, nextUseTable)
		# print "heya"
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

		## for compare types
		if ir[lineNo].type == '>=':
			genAsm.genInstr("addl $1, %" + locationDst)
		elif ir[lineNo].type == '<':
			genAsm.genInstr("subl $1, %" + locationDst)


		## for all types
		if regSrc2 == None:
			genAsm.genInstr(instrType + " (" + ir[lineNo].src2 + "), %" + locationDst)

		else:
			genAsm.genInstr(instrType + " %" + regSrc2 + ", %" + locationDst)


		## for compare types
		var = regDes['eax']
		if var is None: 
			genCompare(ir[lineNo].type)
			if ir[lineNo].type in comparators:
					genAsm.genInstr("movzbl %al, %" + locationDst)
		else:
			genAsm.genInstr("movl %eax, " + var)
			genCompare(ir[lineNo].type)
			if ir[lineNo].type in comparators:
					genAsm.genInstr("movzbl %al, %" + locationDst)
			genAsm.genInstr("movl (" + var + "), %eax")



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
				## Only dutta can do this
		if ir[lineNo].type == 'ifgoto':
			pass
			#TODO

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
							genAsm.genInstr(instrType + ' ' + ir[lineNo].src1)
							genAsm.genInstr('movl %eax, ' + ir[lineNo].dst)

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
					genAsm.genLabel(ir[lineNo].dst)
					if ST.table[ir[lineNo].dst]['type'] == "func":
						genAsm.genInstr("pushl %ebp")
						genAsm.genInstr("movl %esp,  %ebp")

		elif ir[lineNo].type == 'print':
			pass
			#TODO
		elif ir[lineNo].type == 'scan':
			pass
			#TODO
		elif ir[lineNo].type == 'callvoid':
					genAsm.genInstr(instrType + " " + ir[lineNo].dst)

		elif ir[lineNo].type == 'goto':
					genAsm.genInstr(instrType + ' ' + ir[lineNo].dst)

		elif ir[lineNo].type == 'retint':
					locationDst = getreg.getreg(lineNo, nextUseTable)
					if check_int(ir[lineNo].dst):
						genAsm.genInstr('movl $' + ir[lineNo].dst + ', %' + locationDst)
					else:
						regDst = addrDes[ir[lineNo].dst]['register']
						if (regDst is None):
							genAsm.genInstr('movl (' + ir[lineNo].dst + '), %' + locationDst)
						else :
							genAsm.genInstr('movl %' + regDst + ', %' + locationDst)

					genAsm.genInstr("leave")
					genAsm.genInstr(instrType)




	elif ir[lineNo].type in type_1:
			genAsm.genInstr("leave")
			genAsm.genInstr(instrType)





def genCompare(symbolType):

	if symbolType == '<=' or symbolType == '<':
		genAsm.genInstr("setle  %al")


	elif symbolType == '!=':
		genAsm.genInstr("setne %al")

	elif symbolType == '>' or symbolType == '>=':

		genAsm.genInstr("setg %al")

	elif symbolType == '==':
		genAsm.genInstr("sete %al")
	



