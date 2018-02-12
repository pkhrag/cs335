from config import *
# Returns a list of tuples containing starting and ending index of basic blocks.
# Takes instruction lists as input


def findBlocks():
    bbl = []
    start = 0

    for index, instr in enumerate(ir):
        # End of current basic block
        if instr.type == 'goto' or instr.type == 'ifgoto' or instr.type == 'callint' or instr.type == 'callvoid' or instr.type == 'ret' or instr.type == 'print' or instr.type == 'scan':
            bbl.append((start, index))
            start = index + 1
        # Starting new basic block
        elif index > start and instr.type == 'label':
            # print "hey"
            bbl.append((start, index - 1))
            start = index

        elif index == len(ir)-1:
            bbl.append((start,index))

    return bbl
