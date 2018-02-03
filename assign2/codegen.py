import input_ir

type_4 = ['+', '-', 'x', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!', '<=', '>=']
type_3 = 

instr_types = type_4 + ['=', '++', '--', '*', 'label', 'ifgoto', 'print', 'scan', 'ret', 'call']


class Instruction3AC:
    def __init__(self, instr):
        insType = instr[1]

        if not(insType in instr_types):
            raise ValueError('Instruction "' + insType + '" not defined')
        
        self.type = insType
        in1 = 


# Use input function made by dutta
raw_ir = input_ir.dutta_input()
ir = []

for i in raw_ir:
    ir.append(Instruction3AC(i))
