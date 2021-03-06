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
			'x': "imul", 
			'/': "idivl",
			'%': "mod",
			'&': "and", 
			'|': "or", 
			'^': "xor", 
			'==': "cmp", 
			'<': "cmp",
			'>': "cmp",
			'!=': "cmp",
			'<=': "cmp",
			'>=': "cmp",
			'=': "movl",
			'!': "notl",
			'+=': "addl",
			'-=': "subl",
			'x=': "imul",
			'&=': "and",
			'|=': "or",
			'^=': "xor",
			'*': "movl",
			'++': "incl",
			'--': "decl",
			'label' : "label",
			'print': "call printf",#todo
			'scan' : "call scanf",#todo
			'ifgoto': "jne",
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

		# For shitty divide and mod 
		if ir[lineNo].type == '/' or ir[lineNo].type == '%':
			
			edx = regDes['edx']
			eax = regDes['eax']
			
			if edx is not None:
				genAsm.genInstr("movl %edx, " + edx)
			if eax is not None:
				genAsm.genInstr("movl %eax, " + eax)

			
			genAsm.genInstr("movl $0, %edx")
			if addrDes[ir[lineNo].src1]['register'] is not None:
				dividend = addrDes[ir[lineNo].src1]['register']
				genAsm.genInstr("movl %" + dividend + ", %eax")
			else:
				dividend = ir[lineNo].src1
				genAsm.genInstr("movl " + dividend + ", %eax")

			if addrDes[ir[lineNo].src2]['register'] is not None:
				divisor = addrDes[ir[lineNo].src2]['register']
				genAsm.genInstr("idivl %" + divisor)
			else:
				divisor = ir[lineNo].src2
				genAsm.genInstr("idivl " + divisor)
			
			
			if ir[lineNo].type == '/':
				if addrDes[ir[lineNo].dst]['register'] is None:
					genAsm.genInstr("movl %eax, " + ir[lineNo].dst)
				else:
					quet = addrDes[ir[lineNo].dst]['register']
					genAsm.genInstr("movl %eax, %" + quet)
					addrDes[ir[lineNo].dst]['memory'] = False
			else:
				if addrDes[ir[lineNo].dst]['register'] is None:
					genAsm.genInstr("movl %edx, " + ir[lineNo].dst)
				else:
					quet = addrDes[ir[lineNo].dst]['register']
					genAsm.genInstr("movl %edx, %" + quet)
					addrDes[ir[lineNo].dst]['memory'] = False

			if edx is not None:
				genAsm.genInstr("movl (" + edx + "), %edx")
			if eax is not None:
				genAsm.genInstr("movl (" + eax + "), %eax")


			return
		
		regSrc1 = addrDes[ir[lineNo].src1]['register']
		locationDst = getreg.getreg(lineNo, nextUseTable)
		
		isInMemory = addrDes[ir[lineNo].dst]['memory']
		#if isInMemory:
		#	genAsm.genInstr('movl ('+ir[lineNo].dst+'), %'+locationDst)



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
			genAsm.genInstr("subl $1, %" + locationDst)
		elif ir[lineNo].type == '<':
			genAsm.genInstr("addl $1, %" + locationDst)


		## for all types
		if regSrc2 == None:
			genAsm.genInstr(instrType + " (" + ir[lineNo].src2 + "), %" + locationDst)

		else:
			genAsm.genInstr(instrType + " %" + regSrc2 + ", %" + locationDst)


		## for compare types
		if ir[lineNo].type in comparators:
			var = regDes['eax']
			if var is None: 
				genCompare(ir[lineNo].type)
				genAsm.genInstr("movzbl %al, %" + locationDst)
			else:
				if locationDst != 'eax':
					genAsm.genInstr("movl %eax, " + var)
				genCompare(ir[lineNo].type)
				genAsm.genInstr("movzbl %al, %" + locationDst)
				if locationDst != 'eax':
					genAsm.genInstr("movl (" + var + "), %eax")




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
			regDst = addrDes[ir[lineNo].dst]['register']
			if regDst is None:
				genAsm.genInstr("cmp $0, (" + ir[lineNo].dst + ")")
			else:
				genAsm.genInstr("cmp $0, %" + regDst)


			genAsm.genInstr(instrType + " " + ir[lineNo].src1)

		## immediate instructions a+=3 types, what about =,a,b and =,a,4 ???? LOST IT COMPLETELY!
		elif check_int(ir[lineNo].src1):
			locationDst = getreg.getreg(lineNo, nextUseTable)
			isRegDst = addrDes[ir[lineNo].dst]['register']
			if isRegDst is None:
				genAsm.genInstr(instrType + " $" + str(locationDst) + ", " + ir[lineNo].dst)
				addrDes[ir[lineNo].dst]['memory'] = True
				
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
			if ir[lineNo].type == 'callint':
				
			         genAsm.genInstr(instrType + ' ' + ir[lineNo].src1)
     		          	 genAsm.genInstr('movl %eax, ' + ir[lineNo].dst)
                                 addrDes[ir[lineNo].dst]['register'] = None
                                 addrDes[ir[lineNo].dst]['memory'] = True

			

			## in general a+=b type instructions and a=b ??
			else:
				isRegSrc = addrDes[ir[lineNo].src1]['register']
	
		
				## added NOWW
				isInMemory = addrDes[ir[lineNo].dst]['memory']
				#print "heya"
				#print isInMemory
				if isInMemory:
					genAsm.genInstr('movl ('+ir[lineNo].dst+'), %'+locationDst)
				## ----------
		
		
				## if source variable is in memory
				if isRegSrc is None:

					if ir[lineNo].type == '*':
						genAsm.genInstr("movl ("+ir[lineNo].src1+"), %"+locationDst)
						genAsm.genInstr(instrType + " (%" + locationDst + "), %"+locationDst)
						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False

					else:
						genAsm.genInstr(instrType + " (" + ir[lineNo].src1 + "), %" + locationDst)
						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False


				## if source variable is in register already
				else :
					
					if ir[lineNo].type == '*':
						genAsm.genInstr(instrType+ " (%" + isRegSrc + "), %" + locationDst)	
						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False
					
					elif locationDst != isRegSrc:
						genAsm.genInstr(instrType + " %" + isRegSrc + ", %" + locationDst)
						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False
					else:
						
						genAsm.genInstr("movl %" + isRegSrc + ", " + ir[lineNo].src1)
						addrDes[ir[lineNo].src1]['register'] = None
						addrDes[ir[lineNo].src1]['memory'] = True
						
						### DOUBT HERE ------------ where is the instruction ???
						genAsm.genInstr(instrType + " %" + isRegSrc + ", %" + locationDst)
						### ---- ADDED NOWW ----

						addrDes[ir[lineNo].dst]['register'] = locationDst
						addrDes[ir[lineNo].dst]['memory'] = False



				for x in regDes:
		                        if regDes[x] == ir[lineNo].dst:
                		                regDes[x] = None
               			regDes[locationDst] = ir[lineNo].dst


				## delete register occurrences if source variable is not used again in bbl
				# if nextUseTable[lineNo][ir[lineNo].src1]['nextUse'] is None:
				# 	for x in regDes:
				# 		if regDes[x] == ir[lineNo].src1:
				# 			regDes[x] = None

	elif ir[lineNo].type in type_2:

		if ir[lineNo].type in ["++","--","!"]:

			isRegDst = addrDes[ir[lineNo].dst]['register']

			## if in memory directly use incr a.
			if isRegDst is None:
				genAsm.genInstr(instrType + " " + ir[lineNo].dst)

			## else increment a in register
			else:
				genAsm.genInstr(instrType + " %" + ir[lineNo].dst)
				addrDes[ir[lineNo].dst]['memory'] = False

		elif ir[lineNo].type == 'label':
			genAsm.genLabel(ir[lineNo].dst)
			if ST.table[ir[lineNo].dst]['type'] == "func":
				genAsm.genInstr("pushl %ebp")
				genAsm.genInstr("movl %esp,  %ebp")

		elif ir[lineNo].type == 'print':
			if addrDes[ir[lineNo].dst]['register'] is None:
				genAsm.genInstr("pushl " + ir[lineNo].dst)
				genAsm.genInstr("pushl $outFormat")
				genAsm.genInstr(instrType)
				
			else:
				genAsm.genInstr("pushl %" + addrDes[ir[lineNo].dst]['register'])
				genAsm.genInstr("pushl $outFormat")
				genAsm.genInstr(instrType)

		elif ir[lineNo].type == 'scan':
			if addrDes[ir[lineNo].dst]['register'] is None:
				genAsm.genInstr("pushl $" + ir[lineNo].dst)
				genAsm.genInstr("pushl $inFormat")
				genAsm.genInstr(instrType)
				
			else:
				genAsm.genInstr("pushl $" + regDes[addrDes[ir[lineNo].dst]['register']])
				genAsm.genInstr("pushl $inFormat")
				genAsm.genInstr(instrType)
				addrDes[ir[lineNo].dst]["memory"] = True
				genAsm.genInstr("movl (" + ir[lineNo].dst + "), %" + addrDes[ir[lineNo].dst]['register'])
						

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
	



