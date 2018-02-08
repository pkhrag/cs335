import symbol


# Corresponds to 4 operand instructions
# x is multiply and * is dereference
type_4 = ['+', '-', 'x', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!=', '<=', '>=']

# Corresponds to 3 operand instructions
type_3 = ['=', '+=', '-=', 'x=', '&=',
          '|=', '^=', '<<=', '>>=', 
          # '*',
           'ifgoto', 'callint']

# Corresponds to 2 operand instructions
type_2 = ['++', '!', '--', 'label', 'print', 'scan', 'callvoid', 'goto', 'retint']

type_1 = ['retvoid']

instr_types = type_4 + type_3 + type_2 + type_1

# Symbol Table object
ST = symbol.symbolTable()

# IR instructions list
ir = []

# Register Descriptor
regDes = {
    'esp': None,
    'ebp': None,
    'eax': None,
    'ebx': None,
    'ecx': None,
    'edx': None,
    'esi': None,
    'edi': None
}
   #  'r8D': None,
   #  'r9D': None,
   #  'r10D': None,
   #  'r11D': None,
   #  'r12D': None,
   #  'r13D': None,
   #  'r14D': None,
   #  'r15D': None

# Address Descriptor
addrDes = {}

# Stack of symbols to keep track of the function return variables, implemented through list.
stack = []

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

