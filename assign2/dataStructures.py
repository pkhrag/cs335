from config import *


# Creates IR table


class instruction3AC:
    def __init__(self, instr):
        insType = instr[1]

        if not(insType in instr_types):
            raise ValueError('Instruction ' + insType + ' not defined')

        self.type = insType
        self.instr = ', '.join(i for i in instr)

        if insType in type_4:
            if len(instr) != 5:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))
            self.dst = instr[2]

            ST.insert(self.dst, "int")

            self.src1 = instr[3]
            self.src2 = instr[4]

        elif insType in type_3:
            if len(instr) != 4:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))
            self.dst = instr[2]
            self.src1 = instr[3]

            # callint var_name function_name
            if (self.type == 'callint'):
                if ST.lookUp(self.src1):
                    ST.updateArgList(self.src1, "type", "func")
                else:
                    ST.insert(self.src1, "func")
            if (self.type != 'ifgoto'):
                ST.insert(self.dst, "int")


        elif insType in type_2:
            if len(instr) != 3:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))

            self.dst = instr[2]

            if(self.type == 'callvoid'):
                if ST.lookUp(self.dst):
                    ST.updateArgList(self.dst, "type", "func")
                else:
                    ST.insert(self.dst, "func")

            elif (self.type == 'label'):
                if ST.lookUp(self.dst) is False:
                    ST.insert(self.dst, "void")

	    elif (self.type != 'goto'):
		if ST.lookUp(self.dst) is False:
		    ST.insert(self.dst, "int")
		
        else:
            if len(instr) != 2:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))


# Initializes addrDes
def createAddrDesc():
    table = ST.globalSymbolList

    for symbol in table:
        if ST.table[symbol]['type'] != 'void':
            addrDes[symbol] = {"register": None, "memory": False}
