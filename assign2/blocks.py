def findBlocks(ir):
    bbl = []
    start = 0

    for index, instr in enumerate(ir):
        if instr.type == 'goto' or instr.type == 'ifgoto' or instr.type == 'call' or instr.type == 'ret':
            bbl.append((start, index))
            start = index + 1
        elif index > start and instr.type == 'label':
            bbl.append((start, index - 1))
            start = index

    return bbl
