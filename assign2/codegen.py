import input_ir
import blocks
import symbol
import nextUse


# Corresponds to 4 operand instructions
type_4 = ['+', '-', 'x', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!=', '<=', '>=']

# Corresponds to 3 operand instructions
type_3 = ['=', '!', '+=', '-=', 'x=', '/=', '%=', '&=',
          '|=', '^=', '<<=', '>>=', '*', 'ifgoto', 'callint']

# Corresponds to 2 operand instructions
type_2 = ['++', '--', 'label', 'print', 'scan', 'callvoid', 'goto', 'retint']

type_1 = ['retvoid']

instr_types = type_4 + type_3 + type_2 + type_1

# Symbol Table object
ST = symbol.symbolTable()

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

ir = []

for i in raw_ir:
    ir.append(instruction3AC(i))

bbl = blocks.findBlocks(ir)

print bbl

retVal = nextUse.nextUseTable(bbl[1], ST, ir, type_1, type_2, type_3, type_4)
for key, value in retVal.iteritems():
    print key, value


regDes = {
    'esp': None,
    'ebp': None,
    'eax': None,
    'ebx': None,
    'ecx': None,
    'edx': None,
    'esi': None,
    'edi': None,
    'r8D': None,
    'r9D': None,
    'r10D': None,
    'r11D': None,
    'r12D': None,
    'r13D': None,
    'r14D': None,
    'r15D': None
}

addrDes = {}

machineCode = []

# for block in bbl:
#     currNextUse = nextUse.nextUseTable(block, ir, type_1, type_2, type_3, type_4)
#     start, end = block
#     for insnum in range(start, end+1):
#         currIns = ir[insnum]
#         if currIns.type == 'retvoid':
#             machineCode.append('ret')
#         elif currIns.type == 'retint':
#             
# .
# .
# .
#     