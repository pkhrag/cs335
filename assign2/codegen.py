import input_ir
import blocks
import symbol
import nextUse
import genAsm
import codeGenerator
import dataStructures
from config import *



# Use input function made by dutta
raw_ir = input_ir.dutta_input()


# Intitialize data structures to be used throught out the code 
for i in raw_ir:
    ir.append(dataStructures.instruction3AC(i))
dataStructures.createAddrDesc()

# intitialize the global variables 
genAsm.initializeGlobals()

bbl = blocks.findBlocks()
## Code generator crux part (text part of .s file)
# print "heya"    
for x in bbl:
    nextUseTable = nextUse.nextUseTable(x)
    codeGenerator.codeGen(x,nextUseTable)

genAsm.closeFile()
