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


def generateInstr():
    pass


def createAddrDesc(ST):
    table = ST.getTable()

    for symbol in table.iterkeys():
        print symbol
        if symbol['type'] == 'int':
            addrDes[symbol] = {"register": None, "memory": None}

    print addrDes


def getreg(instr):
    pass
