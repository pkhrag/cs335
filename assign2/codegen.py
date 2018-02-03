import input_ir

type_4 = ['+', '-', 'x', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!=', '<=', '>=']

type_3 = ['=', '!', '+=', '-=', 'x=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '*', 'ifgoto']

type_2 = ['++', '--', 'label', 'print', 'scan', 'call', 'goto']

type_1 = ['ret']

instr_types = type_4 + type_3 + type_2 + type_1


class instruction3AC:
    def __init__(self, instr):
        insType = instr[1]

        if not(insType in instr_types):
            raise ValueError('Instruction "' + insType + '" not defined')

        self.type = insType

        if insType in type_4:
            if len(instr) != 5:
                raise ValueError('Inappropriate number of operands')
            self.dst = instr[2]
            self.src1 = instr[3]
            self.src2 = instr[4]

        elif insType in type_3:
            if len(instr) != 4:
                raise ValueError('Inappropriate number of operands')
            self.dst = instr[2]
            self.src1 = instr[3]

        elif insType in type_2:
            if len(instr) != 3:
                raise ValueError('Inappropriate number of operands')
            self.dst = instr[2]


# Use input function made by dutta
raw_ir = input_ir.dutta_input()

ir = []

for i in raw_ir:
    ir.append(Instruction3AC(i))
