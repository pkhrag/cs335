import input_ir
import blocks
import symbol


# Corresponds to 4 operand instructions
type_4 = ['+', '-', 'x', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!=', '<=', '>=']

# Corresponds to 3 operand instructions
type_3 = ['=', '!', '+=', '-=', 'x=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '*', 'ifgoto']

# Corresponds to 2 operand instructions
type_2 = ['++', '--', 'label', 'print', 'scan', 'call', 'goto']

# Corresponds to 1 operand instructions
type_1 = ['ret']

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


# Use input function made by dutta
raw_ir = input_ir.dutta_input()

ir = []

for i in raw_ir:
    ir.append(instruction3AC(i))

bbl = blocks.findBlocks(ir)

print ir
print bbl
print ST.table
