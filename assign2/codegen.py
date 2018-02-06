import input_ir
import blocks
import symbol
import nextUse
import genAsm
import getreg
from config import *



# Creates IR table


class instruction3AC:
    def __init__(self, instr):
        insType = instr[1]

        if not(insType in instr_types):
            raise ValueError('Instruction ' + insType + ' not defined')

        self.type = insType

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

            # callint var_name function_name
            if (self.type != 'ifgoto'):
                ST.insert(self.dst, "int")

            self.src1 = instr[3]

        elif insType in type_2:
            if len(instr) != 3:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))

            self.dst = instr[2]

            if (self.type == 'label'):
                ST.insert(self.dst, "void")

        else:
            if len(instr) != 2:
                raise ValueError('Inappropriate number of operands in ' +
                                 ', '.join(i for i in instr))


# Use input function made by dutta
raw_ir = input_ir.dutta_input()

for i in raw_ir:
    ir.append(instruction3AC(i))

bbl = blocks.findBlocks()

print bbl

retVal = nextUse.nextUseTable(bbl[1])
for key, value in retVal.iteritems():
    print key, value


init_symbols.initializeGlobals()
getreg.createAddrDesc()
