from config import *
import genAsm

# finds and returns an empty register. returns None if not exist.
def emptyReg():
    for key, value in regDes.iteritems():
        if key != 'esp' and key != 'ebp':
            if value == None:
                return key
    return None

# Returns if register is required for Op operation
def regImp(instrNum):
    # if
    return True


def splitReg(reg, var):
    if addrDes[var]['memory'] is False:
        genAsm.genInstr("movl %" + reg + ", " + var)
        addrDes[var]['memory'] = True
    addrDes[var]['register'] = None
    regDes[reg] = None

# finds and splits a register
def regAlloc(instrNum, nextUseTable, shiftType = False):
    farthest = 0
    reg = None
    for key, value in regDes.iteritems():
        if key != 'esp' and key != 'ebp' and (shiftType == False or key != 'ecx'):
            var = value
            if (var not in nextUseTable[instrNum]) or (nextUseTable[instrNum][var]['nextUse'] is None):
                splitReg(key, var)
                return key
            else:
                if nextUseTable[instrNum][var]['nextUse'] > farthest:
                    farthest = nextUseTable[instrNum][var]['nextUse']
                    reg = key

    var = regDes[reg]
    splitReg(reg, var)
    return reg

# Returns the register name if possible, otherwise return None, i.e., use default memory location.
# No immediate operation in IR except for assignment, and returns the number itself in case of assignment.
def getreg(instrNum, nextUseTable):
    if ir[instrNum].type in type_4:
        # x = y Op z
        x = ir[instrNum].dst
        y = ir[instrNum].src1
        z = ir[instrNum].src2
        if (addrDes[y]['register'] != None) and (nextUseTable[instrNum][y]['nextUse'] is None):
            reg = addrDes[y]['register']
            if addrDes[y]['memory'] is False:
                genAsm.genInstr("movl %" + reg + ", " + y)
                addrDes[y]['memory'] = True
                addrDes[y]['register'] = None
            return reg
        elif emptyReg() != None:
            return emptyReg()
        else:
            if nextUseTable[instrNum][x]['nextUse'] is not None or regImp(instrNum):
                return regAlloc(instrNum,nextUseTable)
            else:
                return None # Use it's default memory location defined in .data section

    elif ir[instrNum].type in type_3:
        # x Op= y
        x = ir[instrNum].dst
        y = ir[instrNum].src1
        if check_int(y) and ir[instrNum].type != 'pload':
            return int(y, 10)
        if ir[instrNum].type == 'callint':
            if regDes['eax']:
                var = regDes['eax']
                splitReg('eax', var)
            return 'eax'
        else:
            # shifting case
            if ir[instrNum].type == '<<=' or ir[instrNum].type == '>>=':
                if addrDes[x]['register'] != 'ecx':
                    return addrDes[x]['register']
                elif emptyReg() != None:
		    if addrDes[x]['register'] == 'ecx':
			genAsm.genInstr('movl %ecx, ' + x)
		    	addrDes[x]['memory'] = True
                    return emptyReg()
                else:
		    if addrDes[x]['register'] == 'ecx':
			genAsm.genInstr('movl %ecx, ' + x)
		    	addrDes[x]['memory'] = True
                    if nextUseTable[instrNum][x]['nextUse'] is not None or regImp(instrNum):
                        return regAlloc(instrNum, nextUseTable, True)
                    else:
                        return None # Use it's default memory location defined in .data section

            # x Op= y ~ x = x Op y, so same rule as above
            # If already in register, return it
            if addrDes[x]['register']:
                return addrDes[x]['register']
            elif emptyReg() != None:
                return emptyReg()
            else:
                if nextUseTable[instrNum][x]['nextUse'] is not None or regImp(instrNum):
                    return regAlloc(instrNum, nextUseTable)
                else:
                    return None # Use it's default memory location defined in .data section

    elif ir[instrNum].type in type_2:
        # x++ or retint x
        x = ir[instrNum].dst
        if ir[instrNum].type == 'retint':
            if regDes['eax']:
                var = regDes['eax']
                splitReg('eax', var)
            return 'eax'
        else:
            # x Op= y ~ x = x Op y, so same rule as above
            # If already in register, return it
            if addrDes[x]['register']:
                return addrDes[x]['register']
            elif emptyReg() != None:
                return emptyReg()
            else:
                if nextUseTable[instrNum][x]['nextUse'] is None or regImp(instrNum):
                    return regAlloc(instrNum, nextUseTable)
                else:
                    return None # Use it's default memory location defined in .data section
