def findBlocks(ir):
    bbl = []
    start = 0

    for index, instr in enumerate(ir):
        if instr.type == 'goto' or instr.type == 'ifgoto' or instr.type == 'call':
            bbl.append((start, index))
            start = index + 1
        elif index > 0 and instr.type == 'label':
            bbl.append((start, index - 1))
            start = index

    return bbl
