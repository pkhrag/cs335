from config import *


def nextUseTable(x):

    start = x[0]
    end = x[1]
    tableToRet = {}

    for i in range(start, end + 1):
        tableToRet[i] = {}

    listOfSymbols = set([])
    for i in range(start, end + 1):

        if ir[i].type in type_4:
            listOfSymbols.add(ir[i].dst)
            if ST.lookUp(ir[i].src1):
                listOfSymbols.add(ir[i].src1)

            if ST.lookUp(ir[i].src2):
                listOfSymbols.add(ir[i].src2)

        elif ir[i].type in type_3:

            if ir[i].type != 'ifgoto' and ir[i].type != 'callint':

                listOfSymbols.add(ir[i].dst)
                if ST.lookUp(ir[i].src1):
                    listOfSymbols.add(ir[i].src1)
            else:
                listOfSymbols.add(ir[i].dst)

                # We are not storing liveness value of label - they can't be used again (same names)

        elif ir[i].type in type_2:

            if ir[i].type == '++' or ir[i].type == '--' or ir[i].type == 'print' or ir[i].type == 'retint':
                listOfSymbols.add(ir[i].dst)

            elif ir[i].type == 'scan':
                listOfSymbols.add(ir[i].dst)

    for i in range(start, end + 1):
        for j in listOfSymbols:
            tableToRet[i][j] = {}
            tableToRet[i][j]["live"] = False
            tableToRet[i][j]["nextUse"] = False

    for i in range(end, start - 1, -1):

        if i != end:
            for k in tableToRet[i]:
                tableToRet[i][k] = tableToRet[i + 1][k].copy()

        if ir[i].type in type_4:

            (tableToRet[i])[ir[i].dst]["live"] = False
            (tableToRet[i])[ir[i].dst]["nextUse"] = False

            if ST.lookUp(ir[i].src1):
                (tableToRet[i])[ir[i].src1]["live"] = True
                (tableToRet[i])[ir[i].src1]["nextUse"] = i

            if ST.lookUp(ir[i].src2):
                (tableToRet[i])[ir[i].src2]["live"] = True
                (tableToRet[i])[ir[i].src2]["nextUse"] = i

        elif ir[i].type in type_3:

            if ir[i].type != 'ifgoto' and ir[i].type != 'callint':

                (tableToRet[i])[ir[i].dst]["live"] = False
                (tableToRet[i])[ir[i].dst]["nextUse"] = False

                if ST.lookUp(ir[i].src1):
                    (tableToRet[i])[ir[i].src1]["live"] = True
                    (tableToRet[i])[ir[i].src1]["nextUse"] = i
            else:
                (tableToRet[i])[ir[i].dst]["live"] = True
                (tableToRet[i])[ir[i].dst]["nextUse"] = i

                # We are not storing liveness value of label - they can't be used again (same names)

        elif ir[i].type in type_2:

            if ir[i].type == '++' or ir[i].type == '--' or ir[i].type == 'print' or ir[i].type == 'retint':
                (tableToRet[i])[ir[i].dst]["live"] = True
                (tableToRet[i])[ir[i].dst]["nextUse"] = i

            elif ir[i].type == 'scan':
                (tableToRet[i])[ir[i].dst]["live"] = False
                (tableToRet[i])[ir[i].dst]["nextUse"] = False

    for i in range(start, end):
        tableToRet[i] = tableToRet[i + 1]

    return tableToRet
