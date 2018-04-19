import ply.yacc as yacc
import sys
import os
from symbol import symbolTable
# from lexer import tokens, data
from lexer import *

# ----------------------SYMBOL TABLE---------------------
scopeDict = {}
scopeDict[0] = symbolTable()

scopeStack = [0]
currScope = 0
scopeSeq = 0
varSeq = 0
firstFunc = True
labelSeq = 1
labelDict = {}



def assignTypeCheck(a,b):
    if a == b:
        return True
    if b.startswith('lit') and a==b[3:]:
        return True
    

    return False


def oprnTypeCheck(a,b,op):

    if a.startswith('*') and b.startswith('*'):
            return False

    if op == '+' or op == '-':
        
        if a == b:
            return True
        if a.startswith('lit') and a[3:] == b:
            return True
        if b.startswith('lit') and b[3:] == a:
            return True

        if a.startswith('lit') and b.startswith('lit') and a[3:] == b[3:]:
            return True

        if a.startswith('*') and (b=='int_t' or b=='litint_t'):
            return True

        if b.startswith('*') and (a=='int_t' or a=='litint_t'):
            return True
    
    else :

        if a == b:
            return True
        if a.startswith('lit') and a[3:] == b:
            return True
        if b.startswith('lit') and b[3:] == a:
            return True

        if a.startswith('lit') and b.startswith('lit') and a[3:] == b[3:]:
            return True


    return False




def checkId(identifier, typeOf):
    if typeOf == "global":
        if scopeDict[0].getInfo(identifier) is not None:
            return True
        return False

    if typeOf == "*":
        if scopeDict[currScope].getInfo(identifier) is not None:
            return True
        return False

    if typeOf == "label":
    	if scopeDict[0].getInfo(identifier) is not None:
    		return True
    	return False

    if typeOf == "*!s":
        if scopeDict[currScope].getInfo(identifier) is not None:
            info = scopeDict[currScope].getInfo(identifier)
            if info['type'] != ('type'+identifier):
                return True
        return False

    for scope in scopeStack[::-1]:
        if scopeDict[scope].getInfo(identifier) is not None:
            info = scopeDict[scope].getInfo(identifier)
            if typeOf == "**" or info['type'] == typeOf:
                return True

    return False


def addScope(name=None):

    global scopeSeq
    global currScope
    scopeSeq += 1
    lastScope = currScope
    currScope = scopeSeq
    scopeStack.append(currScope)
    scopeDict[currScope] = symbolTable()
    scopeDict[currScope].setParent(lastScope)
    if name is not None:
        if type(name) is list:
            scopeDict[lastScope].insert(name[1], 'func')
            scopeDict[lastScope].updateArgList(name[1], 'child', scopeDict[currScope])
        else:
            temp = currScope
            currScope = lastScope
            if checkId(name, '*'):
                raise NameError("Name " + name + " already defined")
            currScope = temp
            scopeDict[lastScope].insert(name, 'type'+name)
            scopeDict[lastScope].updateArgList(name, 'child', scopeDict[currScope])


def deleteScope():
    global currScope
    currScope = scopeStack.pop()
    currScope = scopeStack[-1]

def newTemp():
    global varSeq
    toRet = 'var'+str(varSeq)
    varSeq += 1
    return toRet

def newLabel():
    global labelSeq
    toret = 'label' + str(labelSeq)
    labelSeq += 1
    return toret


def findInfo(name, Scope=-1):
    if Scope > -1:
        if scopeDict[Scope].getInfo(name) is not None:
            return scopeDict[Scope].getInfo(name)
        raise NameError("Identifier " + name + " is not defined!")

    for scope in scopeStack[::-1]:
        if scopeDict[scope].getInfo(name) is not None:
            info = scopeDict[scope].getInfo(name)
            return info

    raise NameError("Identifier " + name + " is not defined!")

def findScope(name):
    for scope in scopeStack[::-1]:
        if  scopeDict[scope].getInfo(name) is not None:
            return scope

    raise NameError("Identifier " + name + " is not defined!")

def findLabel(name):
	for scope in scopeStack[::-1]:
		if name in scopeDict[scope].extra:
			return scopeDict[scope].extra[name]
	raise ValueError("Not in any loop scope")

# ------------------------------------------------------
precedence = (
    ('right','ASSIGN', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_ASSIGN'),
    ('left', 'LESSER', 'GREATER','LESS_EQUALS','MORE_EQUALS'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIVIDE','MOD')
)

# ------------- IR GENERATION -----------

class Node:
    def __init__(self):
        self.idList = []
        self.code = []
        self.typeList = []
        self.placelist = []
        self.extra = {}



# def defaultType(typeOf):
#   if typeOf == "int_t":
#     return str(0)


# --------------------------------------------------------

rootNode = None

# ------------------------START----------------------------
def p_start(p):
    '''start : SourceFile'''
    p[0] = p[1]
    global rootNode
    rootNode = p[0]
# -------------------------------------------------------


# -----------------------TYPES---------------------------
def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPAREN Type RPAREN'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_type_name(p):
    '''TypeName : TypeToken
                | QualifiedIdent'''
    p[0] = p[1]

def p_type_token(p):
    '''TypeToken : INT_T
                 | FLOAT_T
                 | UINT_T
                 | COMPLEX_T
                 | RUNE_T
                 | BOOL_T
                 | STRING_T
                 | TYPE IDENTIFIER'''
    if len(p) == 2:
        p[0] = Node()
        p[0].typeList.append(p[1])
        if p[1] == 'int_t':
            p[0].extra['sizeList'] = [4]
        else:
            p[0].extra['sizeList'] = [1]
    else:
        if not checkId(p[2], '**'):
            raise TypeError("Typename " + p[2] + " not defined")
        p[0] = Node()
        info = findInfo(p[2], 0)
        # print info['type']
        p[0].typeList.append(info['type'])
        # TODO struct size

def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PointerType'''
    p[0] = p[1]

def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
    p[0] = p[1]
# -------------------------------------------------------





# ------------------- ARRAY TYPE -------------------------
def p_array_type(p):
  '''ArrayType : LSQUARE ArrayLength RSQUARE ElementType'''
  p[0] = Node()
  p[0].code = p[2].code + p[4].code
  p[0].typeList.append("*" + p[4].typeList[0])
  newVar = newTemp()
  p[0].code.append(['=', newVar, p[2].placelist[0]])
  p[0].extra['sizeList'] = [newVar] + p[4].extra['sizeList']

def p_array_length(p):
  ''' ArrayLength : Expression '''
  p[0] = p[1]

def p_element_type(p):
  ''' ElementType : Type '''
  p[0] = p[1]

# --------------------------------------------------------


# ----------------- STRUCT TYPE ---------------------------
def p_struct_type(p):
  '''StructType : CreateFuncScope STRUCT LCURL FieldDeclRep RCURL EndScope'''
  p[0] = p[4]
  info = findInfo(p[-1], 0)
  p[0].typeList = [info['type']]

def p_field_decl_rep(p):
  ''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                  | epsilon '''
  if len(p) == 4:
    # Useless for now
    p[0] = p[1]
    p[0].idList += p[2].idList
    p[0].typeList += p[2].typeList
  else:
    p[0] = p[1]

def p_field_decl(p):
  ''' FieldDecl : IdentifierList Type'''
  p[0] = p[1]
  for i in p[0].idList:
    scopeDict[currScope].updateArgList(i, 'type', p[2].typeList[0])
# ---------------------------------------------------------


# ------------------POINTER TYPES--------------------------
def p_point_type(p):
    '''PointerType : STAR BaseType'''
    p[0] = p[2]
    p[0].typeList[0] = "*"+p[0].typeList[0]
    p[0].extra['sizeList'] = ['inf'] + p[0].extra['sizeList']

def p_base_type(p):
    '''BaseType : Type'''
    p[0] = p[1]
# ---------------------------------------------------------


# ---------------FUNCTION TYPES----------------------------
def p_sign(p):
    '''Signature : Parameters TypeOpt'''
    p[0] = p[1]


    scopeDict[0].insert(p[-2][1],'signatureType')
    if len(p[2].typeList) == 0:
        scopeDict[0].updateArgList(p[-2][1], 'retType', 'void')
    else:
        scopeDict[0].updateArgList(p[-2][1], 'retType', p[2].typeList[0])

    p[0].extra['fName'] = p[-2][1]
    info = findInfo(p[-2][1],0)
    if 'label' not in info:
        labeln = newLabel()
        scopeDict[0].updateArgList(p[-2][1], 'label', labeln)
        scopeDict[0].updateArgList(p[-2][1], 'child', scopeDict[currScope])

    p[0].typeList = p[2].typeList



def p_params(p):
    '''Parameters : LPAREN ParameterListOpt RPAREN'''
    p[0] = p[2]

def p_param_list_opt(p):
    '''ParameterListOpt : ParametersList
                             | epsilon'''
    p[0] = p[1]

def p_param_list(p):
    '''ParametersList : ParameterDecl
                      | ParameterDeclCommaRep'''
    p[0] = p[1]

def p_param_decl_comma_rep(p):
    '''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
                             | ParameterDecl COMMA ParameterDecl'''
    p[0] = p[1]
    p[0].idList += p[3].idList
    p[0].typeList += p[3].typeList
    p[0].placelist += p[3].placelist

def p_param_decl(p):
    '''ParameterDecl : IdentifierList Type
                     | Type'''
    if len(p) == 3:
        p[0] = p[1]
        for x in p[1].idList:
            scopeDict[currScope].updateArgList(x, 'type', p[2].typeList[0])
            p[0].typeList.append(p[2].typeList[0])
    else:
        p[0] = p[1]
# ---------------------------------------------------------


#-----------------------BLOCKS---------------------------
def p_block(p):
    '''Block : LCURL StatementList RCURL'''
    p[0] = p[2]

def p_stat_list(p):
    '''StatementList : StatementRep'''
    p[0] = p[1]

def p_stat_rep(p):
    '''StatementRep : StatementRep Statement SEMICOLON
                    | epsilon'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].code += p[2].code
    else:
        p[0] = p[1]
# -------------------------------------------------------


# ------------------DECLARATIONS and SCOPE------------------------
def p_decl(p):
  '''Declaration : ConstDecl
                 | TypeDecl
                 | VarDecl'''
  p[0] = p[1]

def p_toplevel_decl(p):
  '''TopLevelDecl : Declaration
                  | FunctionDecl'''
  p[0] = p[1]
# -------------------------------------------------------


# ------------------CONSTANT DECLARATIONS----------------
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                 | CONST LPAREN ConstSpecRep RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | epsilon'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].code += p[2].code
    else:
        p[0] = p[1]

def p_const_spec(p):
    '''ConstSpec : IdentifierList Type ASSIGN ExpressionList'''
    p[0] = Node()
    p[0].code = p[1].code + p[4].code

    if(len(p[1].placelist) != len(p[4].placelist)):
        raise ValueError("Error: mismatch in number of identifiers and expressions for asisgnment")

    for x in range(len(p[1].placelist)):
        if (p[4].typeList[x]).startswith('lit'):
          #  if p[2].typeList[0] != p[4].typeList[x][3:] :
           #     raise TypeError('Type of ' + p[1].idList[x] + ' doesn\'t match with expresstion!')
            p[0].code.append(["=", p[1].placelist[x], p[4].placelist[x]])

        p[1].placelist[x] = p[4].placelist[x]
        scope = findScope(p[1].idList[x])
        scopeDict[scope].updateArgList(p[1].idList[x], 'place', p[1].placelist[x])

        # type insertion
        scopeDict[scope].updateArgList(p[1].idList[x], 'type', p[2].typeList[0])
        #if p[2].typeList[0] != p[4].typeList[x] :
         #   raise TypeError('Type of ' + p[1].idList[x] + ' doesn\'t match with expresstion!')
        tcheck = assignTypeCheck(p[2].typeList[0],p[4].typeList[x])
        if not tcheck:
             raise TypeError('Type of ' + p[1].idList[x] + ' doesn\'t match with expresstion!')


    #TODO type checking

def p_identifier_list(p):
    '''IdentifierList : IDENTIFIER IdentifierRep'''
    p[0]= p[2]
    p[0].idList = [p[1]] + p[0].idList
    if checkId(p[1], "*"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        scopeDict[currScope].insert(p[1], None)
        nameTemp = newTemp()
        p[0].placelist = [nameTemp] + p[0].placelist
        scopeDict[currScope].updateArgList(p[1], 'place', nameTemp)

def p_identifier_rep(p):
    '''IdentifierRep : IdentifierRep COMMA IDENTIFIER
                     | epsilon'''
    if len(p) == 4:
        if checkId(p[3], "*"):
            raise NameError("Name " + p[3] + " already exists, can't redefine")
        else:
            p[0] = p[1]
            scopeDict[currScope].insert(p[3], None)
            nameTemp = newTemp()
            p[0].placelist = p[0].placelist + [nameTemp]
            scopeDict[currScope].updateArgList(p[3], 'place', nameTemp)
            p[0].idList.append(p[3])


    else:
        p[0] = p[1]

def p_expr_list(p):
    '''ExpressionList : Expression ExpressionRep'''
    #p[0] = ["ExpressionList", p[1], p[2]]
    p[0] = p[2]
    p[0].code = p[1].code+p[0].code
    p[0].placelist = p[1].placelist + p[0].placelist
    p[0].typeList = p[1].typeList + p[0].typeList
    if 'AddrList' not in p[1].extra:
        p[1].extra['AddrList'] = ['None']
    p[0].extra['AddrList'] += p[1].extra['AddrList']


def p_expr_rep(p):
    '''ExpressionRep : ExpressionRep COMMA Expression
                     | epsilon'''
    if len(p) == 4:
    	p[0] = p[1]
    	p[0].code += p[3].code
    	p[0].placelist += p[3].placelist
    	p[0].typeList += p[3].typeList
        if 'AddrList' not in p[3].extra:
            p[3].extra['AddrList'] = ['None']
        p[0].extra['AddrList'] += p[3].extra['AddrList']

    else:
    	p[0] = p[1]
        p[0].extra['AddrList'] = []
# ------------------------------------------------------


# ------------------TYPE DECLARATIONS-------------------
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPAREN TypeSpecRep RPAREN'''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = p[2]
        # p[0] = ["TypeDecl", "type", p[2]]

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpecRep TypeSpec SEMICOLON
                   | epsilon'''
    if len(p) == 4:
        p[0] = Node()
    else:
        p[0] = p[1]

def p_type_spec(p):
    '''TypeSpec : TypeDef'''
    p[0] = p[1]
# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''
    if checkId(p[1], "*!s"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        # print p[2].typeList
        scopeDict[currScope].insert(p[1], p[2].typeList[0])
        # print findInfo(p[1])
    p[0] = Node()
# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------
def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPAREN VarSpecRep RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[3]

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpecRep VarSpec SEMICOLON
                  | epsilon'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].code += p[2].code
    else:
        p[0] = p[1]

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''
    if p[2] == '=':
        p[0] = Node()
        p[0].code = p[1].code + p[3].code

        if(len(p[1].placelist) != len(p[3].placelist)):
            raise ValueError("Error: mismatch in number of identifiers and expressions for asisgnment")

        for x in range(len(p[1].placelist)):
            scope = findScope(p[1].idList[x])
            if (p[3].typeList[x]).startswith('lit'):
                p[0].code.append(["=", p[1].placelist[x], p[3].placelist[x]])
                scopeDict[scope].updateArgList(p[1].idList[x], 'type', p[3].typeList[x][3:])
            else:
                scopeDict[scope].updateArgList(p[1].idList[x], 'type', p[3].typeList[x])

            p[1].placelist[x] = p[3].placelist[x]
            scopeDict[scope].updateArgList(p[1].idList[x], 'place', p[1].placelist[x])
    else:
        if len(p[3].placelist) == 0:
            p[0] = p[1]
            p[0].code += p[2].code
            if p[2].typeList[0][0] == '*':
                newVar = newTemp()
                p[0].code.append(['=', newVar, 1])
                for item in p[2].extra['sizeList']:
                    p[0].code.append(['x=', newVar, item])
            for x in range(len(p[1].idList)):
                scope = findScope(p[1].idList[x])
                scopeDict[scope].updateArgList(p[1].idList[x], 'type', p[2].typeList[0])
                if p[2].typeList[0][0] == '*':
                    p[0].code.append(['array', p[1].placelist[x], newVar])
                    scopeDict[scope].updateArgList(p[1].idList[x], 'sizeList', p[2].extra['sizeList'])
            return

        p[0] = Node()
        p[0].code = p[1].code + p[3].code
        if(len(p[1].placelist) != len(p[3].placelist)):
            raise ValueError("Error: mismatch in number of identifiers and expressions for asisgnment")

        for x in range(len(p[1].placelist)):
            if not (p[3].typeList[x]).startswith('lit'):
                p[0].code.append(["=", p[1].placelist[x], p[3].placelist[x]])

            p[1].placelist[x] = p[3].placelist[x]

            #TODO typelist check required
            scope = findScope(p[1].idList[x])
            scopeDict[scope].updateArgList(p[1].idList[x], 'place', p[1].placelist[x])
            scopeDict[scope].updateArgList(p[1].idList[x], 'type', p[2].typeList[0])
            if p[2].typeList[0][0] == '*':
                scopeDict[scope].updateArgList(p[1].idList[x], 'sizeList', p[2].extra['sizeList'])


            tcheck = assignTypeCheck(p[2].typeList[0], p[3].typeList[x])
            if not tcheck:
                raise TypeError("Error : type of " +p[1].idList[x] + " doesnt match with expression ")

def p_expr_list_opt(p):
    '''ExpressionListOpt : ASSIGN ExpressionList
                         | epsilon'''

    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = p[1]
# -------------------------------------------------------


# ----------------SHORT VARIABLE DECLARATIONS-------------
def p_short_var_decl(p):
  ''' ShortVarDecl : IDENTIFIER QUICK_ASSIGN Expression '''
  if checkId(p[1], "*"):
    raise NameError("Name " + p[1] + " already exists, can't redefine")
  else:
    scopeDict[currScope].insert(p[1], None)
  p[0] = Node()
  newVar = newTemp()
  p[0].code = p[3].code
  p[0].code.append(['=', newVar, p[3].placelist[0]])
  scopeDict[currScope].updateArgList(p[1], 'place', newVar)
  scopeDict[currScope].updateArgList(p[1], 'type', p[3].typeList[0])
# -------------------------------------------------------



# ----------------FUNCTION DECLARATIONS------------------
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName CreateScope Function EndScope
                    | FUNC FunctionName CreateScope Signature EndScope'''


    if not len(p[4].code):
        p[0] = Node()
        return

    p[0] = Node()
    global firstFunc
    if firstFunc:
        firstFunc = False
        p[0].code = [["goto", "label0"]]
    info = findInfo(p[2][1])
    label = info['label']

    p[0].code.append(['label', label])
    p[0].code += p[4].code

def p_create_func_scope(p):
    '''CreateFuncScope : '''
    addScope(p[-1])

def p_create_scope(p):
    '''CreateScope : '''
    addScope()

def p_delete_scope(p):
    '''EndScope : '''
    deleteScope()

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''
    p[0] = ["FunctionName", p[1]]


def p_func(p):
    '''Function : Signature funMark FunctionBody'''
    # TODO typechecking of return type. It should be same as defined in signature
    p[0] = p[3]
    for x in range(len(p[1].idList)):
        info = findInfo(p[1].idList[x])
        p[0].code = [['pload', info['place'], len(p[1].idList) - x - 1]] + p[0].code

    if checkId(p[-2][1], "signatureType"):
        if p[-2][1] == "main":
            scopeDict[0].updateArgList("main", "label", "label0")
            scopeDict[0].updateArgList("main", 'child', scopeDict[currScope])

        info = findInfo(p[-2][1])
        info['type'] = 'func'
    else:
        raise NameError('no signature for ' + p[-2][1] + '!')


def p_funMark(p):
    ''' funMark : '''

    fName =  p[-1].extra['fName']
    scopeDict[currScope].updateExtra('fName', fName)
    if len(p[-1].typeList) > 0:
        scopeDict[currScope].updateExtra('retT', p[-1].typeList[0])

    else:
        scopeDict[currScope].updateExtra('retT', 'void')

def p_func_body(p):
    '''FunctionBody : Block'''
    p[0] = p[1]
# -------------------------------------------------------


# ----------------------OPERAND----------------------------
def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_literal(p):
    '''Literal : BasicLit'''
               #| CompositeLit'''
    p[0] = p[1]

def p_basic_lit(p):
    '''BasicLit : I INTEGER
                | I OCTAL
                | I HEX
                | F FLOAT
                | C IMAGINARY
                | R RUNE
                | S STRING'''
    p[0] = Node()
    name = newTemp()
    p[0].code.append(["=", name, p[2]])
    p[0].placelist.append(name)
    p[0].typeList.append('lit' + p[1])

def p_I(p):
    ''' I : '''
    p[0] = 'int_t'


def p_R(p):
    ''' R : '''
    p[0] = 'rune_t'


def p_F(p):
    ''' F : '''
    p[0] = 'float_t'

def p_C(p):
    ''' C : '''
    p[0] = 'complex_t'

def p_S(p):
    ''' S : '''
    p[0] = 'string_t'


def p_operand_name(p):
    '''OperandName : IDENTIFIER'''
    if not checkId(p[1], "**"):
        raise NameError("Identifier " + p[1] + " not defined")
    p[0] = Node()
    info = findInfo(p[1])
    #print info


    if info['type'] == 'func' or info['type'] == 'signatureType':
        p[0].typeList = [info['retType']]
        p[0].placelist.append(info['label'])
    else:
        p[0].typeList = [info['type']]
        p[0].placelist.append(info['place'])
        p[0].extra['layerNum'] = 0
        p[0].extra['operand'] = p[1]
    p[0].idList = [p[1]]
# ---------------------------------------------------------


# -------------------QUALIFIED IDENTIFIER----------------
def p_quali_ident(p):
    '''QualifiedIdent : IDENTIFIER DOT TypeName'''
    if not checkId(p[1], "package"):
        raise NameError("Package " + p[1] + " not included")
    p[0] = Node()
    p[0].typeList.append(p[1]+p[2]+p[3].typeList[0])

# -------------------------------------------------------


# ------------------PRIMARY EXPRESSIONS--------------------
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | PrimaryExpr Selector
                   | Conversion
                   | PrimaryExpr LSQUARE Expression RSQUARE
                   | PrimaryExpr Slice
                   | PrimaryExpr TypeAssertion
                   | PrimaryExpr LPAREN ExpressionListTypeOpt RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '[':
        p[0] = p[1]
        p[0].code += p[3].code

        info = findInfo(p[1].extra['operand'])
        sizeList = info['sizeList']

        if p[1].extra['layerNum'] == len(sizeList) - 1:
            raise IndexError('Dimension of the array ' + p[1].extra['operand'] + " doesn't match")

        newVar = newTemp()
        p[0].code.append(['=', newVar, p[3].placelist[0]])
        for item in sizeList[p[1].extra['layerNum']+1:]:
            p[0].code.append(['x=', newVar, item])

        newPlace = newTemp()
        p[0].code.append(['+', newPlace, p[0].placelist[0], newVar])
        p[0].placelist = [newPlace]
        if p[1].extra['layerNum'] == len(sizeList) - 2:
            newPlace2 = newTemp()
            p[0].code.append(['load', newPlace2, newPlace])
            p[0].placelist = [newPlace2]


        p[0].extra['AddrList'] = [newPlace]
        p[0].typeList = [p[1].typeList[0][1:]]
        p[0].extra['layerNum'] += 1

    elif p[2] == '(':
        p[0] = p[1]
        p[0].code += p[3].code


        listVal = []
        for key,value in enumerate(scopeDict[currScope].table):
            currInfo = findInfo(value,currScope)
            listVal.append(value)
            p[0].code.append(['push', currInfo['place']])



        if len(p[3].placelist):
            for x in p[3].placelist:
                p[0].code.append(['push', x])




        info = findInfo(p[1].idList[0], 0)
        if info['retType'] == 'void':
            p[0].code.append(['callvoid', info['label']])
        else:
            newPlace = newTemp()
            p[0].placelist = [newPlace]
            p[0].code.append(['callint', newPlace, info['label']])
        #TODO type checking



        t = newTemp()
        if len(p[3].placelist):
            for x in p[3].placelist:
                p[0].code.append(['pop', t])

        for value in listVal[::-1]:
            currInfo = findInfo(value,currScope)
            p[0].code.append(['pop', currInfo['place']])



        p[0].typeList = [p[1].typeList[0]]
    else:
        if not len(p[2].placelist):
            p[0] = Node()
        else:
            p[0] = p[1]
            p[0].placelist = p[2].placelist
            p[0].typeList = p[2].typeList

def p_selector(p):
    '''Selector : DOT IDENTIFIER'''
    p[0] = Node()
    info = findInfo(p[-1].idList[0])
    structName = info['type']
    for x in range(len(structName)):
        if structName[x] != '*':
            break
    structName = structName[x+4:]
    infoStruct = findInfo(structName, 0)
    newScopeTable = infoStruct['child']
    if p[2] not in newScopeTable.table:
        raise NameError("Identifier " + p[2] + " is not defined in struct " + structName)

    s = p[-1].idList[0] + "." + p[2]
    if checkId(s,'*'):
        info = findInfo(s)
        p[0].placelist = [info['place']]
        p[0].typeList = [info['type']]
    else:
        p[0].placelist = [newTemp()]
        typedata = newScopeTable.getInfo(p[2])
        p[0].typeList = [typedata['type']]
        scopeDict[currScope].insert(s,p[0].typeList[0])
        scopeDict[currScope].updateArgList(s,'place',p[0].placelist[0])


def p_slice(p):
    '''Slice : LSQUARE ExpressionOpt COLON ExpressionOpt RSQUARE
             | LSQUARE ExpressionOpt COLON Expression COLON Expression RSQUARE'''
    if len(p) == 6:
        p[0] = ["Slice", "[", p[2], ":", p[4], "]"]
    else:
        p[0] = ["Slice", "[", p[2], ":", p[4], ":", p[6], "]"]

def p_type_assert(p):
    '''TypeAssertion : DOT LPAREN Type RPAREN'''
    p[0] = ["TypeAssertion", ".", "(", p[3], ")"]

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                             | epsilon'''
    p[0] = p[1]
# ---------------------------------------------------------


#----------------------OPERATORS-------------------------
def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression LOGICAL_OR Expression
                  | Expression LOGICAL_AND Expression
                  | Expression EQUALS Expression
                  | Expression NOT_ASSIGN Expression
                  | Expression LESSER Expression
                  | Expression GREATER Expression
                  | Expression LESS_EQUALS Expression
                  | Expression MORE_EQUALS Expression
                  | Expression OR Expression
                  | Expression XOR Expression
                  | Expression DIVIDE Expression
                  | Expression MOD Expression
                  | Expression LSHIFT Expression
                  | Expression RSHIFT Expression
                  | Expression PLUS Expression
                  | Expression MINUS Expression
                  | Expression STAR Expression
                  | Expression AND Expression'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].code += p[3].code
        newPlace = newTemp()
        if p[2] == "*":
            p[0].code.append(["x",newPlace,p[1].placelist[0], p[3].placelist[0] ])
        elif p[2] == '&&':
            p[0].code.append(["&",newPlace,p[1].placelist[0], p[3].placelist[0] ])
        elif p[2] == '||':
            p[0].code.append(["|",newPlace,p[1].placelist[0], p[3].placelist[0] ])
        else:
            p[0].code.append([p[2],newPlace,p[1].placelist[0], p[3].placelist[0] ])
        p[0].placelist = [newPlace]

        #TODO typechecking based on typeList and update type of p[0]
        checkt = oprnTypeCheck(p[1].typeList[0], p[3].typeList[0], p[2])
        if not checkt:
            raise TypeError("Expression1 of type: " + p[1].typeList[0] + " with operator: " + p[2] + " with Expression2 of type: " + p[3].typeList)

    else:
        p[0] = p[1]

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                     | epsilon'''
    p[0] = p[1]

def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr
                 | UnaryOp UnaryExpr
                 | NOT UnaryExpr'''
    if len(p) == 2:
   	p[0] = p[1]

    elif p[1] == "!":
        p[0] = p[2]
        newPlace = newTemp()
        p[0].code.append(["!", newPlace, p[2].placelist[0]])
        p[0].placelist = [newPlace]
    else:
        p[0] = p[2]
        newPlace = newTemp()
        if p[1][1] == "-" or p[1][1] == '+':

            newPlace2 = newTemp()
            p[0].code.append(['=',newPlace2, 0])
            p[0].code.append([p[1][1],newPlace, newPlace2, p[2].placelist[0]])

        else:

            if p[1][1] == '*':
                p[0].code.append(['load', newPlace, p[2].placelist[0]])
                if p[2].typeList[0][0] != '*':
                    raise TypeError("Type of deference expression is not a valid pointer type")
                p[0].typeList[0] = p[2].typeList[0][1:]

            else:
                p[0].code.append(['addr', newPlace, p[2].placelist[0]])
                p[0].typeList[0] = '*' + p[2].typeList[0]

        p[0].placelist = [newPlace]

def p_unary_op(p):
    '''UnaryOp : PLUS
               | MINUS
               | STAR
               | AND '''
    if p[1] == '+':
        p[0] = ["UnaryOp", "+"]
    elif p[1] == '-':
        p[0] = ["UnaryOp", "-"]
    elif p[1] == '*':
        p[0] = ["UnaryOp", "*"]
    elif p[1] == '&':
        p[0] = ["UnaryOp", "&"]
# -------------------------------------------------------




# -----------------CONVERSIONS-----------------------------
def p_conversion(p):
    '''Conversion : TYPECAST Type LPAREN Expression RPAREN'''
    p[0] = p[4]
    p[0].typeList = [p[1].typeList[0]]
# ---------------------------------------------------------






# ---------------- STATEMENTS -----------------------
def p_statement(p):
    '''Statement : Declaration
                 | LabeledStmt
                 | SimpleStmt
                 | ReturnStmt
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
                 | CreateScope Block EndScope
                 | IfStmt
                 | SwitchStmt
                 | ForStmt
                 | PrintStmt
                 | ScanStmt'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_print_stmt(p):
    ''' PrintStmt : PRINT Expression'''
    p[0] = p[2]
    p[0].code.append(['print', p[2].placelist[0]])

def p_scan_stmt(p):
    ''' ScanStmt : SCAN Expression'''
    p[0] = Node()
    p[0].code.append(['scan', p[2].placelist[0]])



def p_simple_stmt(p):
  ''' SimpleStmt : epsilon
                 | ExpressionStmt
                 | IncDecStmt
                 | Assignment
                 | ShortVarDecl '''
  p[0] = p[1]


def p_labeled_statements(p):
  ''' LabeledStmt : Label COLON Statement '''
  if checkId(p[1][1], "label"):
    raise NameError("Label " + p[1][1] + " already exists, can't redefine")

  newl = ''
  if p[1][1] in labelDict:
  	scopeDict[0].insert(p[1][1], "label")
  	scopeDict[0].updateArgList(p[1][1], 'label', labelDict[p[1][1]][1])
  	labelDict[p[1][1]][0] = True
  	newl = labelDict[p[1][1]][1]
  else:
  	newl = newLabel()
  	scopeDict[0].insert(p[1][1], "label")
  	scopeDict[0].updateArgList(p[1][1], 'label', newl)
  	labelDict[p[1][1]] = [True, newl]

  p[0] = p[3]
  p[0].code = [['label',newl]] + p[0].code

def p_label(p):
  ''' Label : IDENTIFIER '''
  p[0] = ["Label", p[1]]



def p_expression_stmt(p):
  ''' ExpressionStmt : Expression '''
  p[0] = Node()
  p[0].code = p[1].code

def p_inc_dec(p):
  ''' IncDecStmt : Expression INCR
                 | Expression DECR '''
  p[0] = Node()
  p[0].code = p[1].code
  p[0].code.append([p[2], p[1].placelist[0]])

def p_assignment(p):
  ''' Assignment : ExpressionList assign_op ExpressionList'''
  if len(p[1].placelist) != len(p[3].placelist):
      raise ValueError("Number of expressions are not equal")
  p[0] = Node()
  p[0].code = p[1].code
  p[0].code += p[3].code
  for x in range(len(p[1].placelist)):
      p[0].code.append([p[2][1][1], p[1].placelist[x], p[3].placelist[x]])
      if p[1].extra['AddrList'][x] != 'None':
        p[0].code.append(['store', p[1].extra['AddrList'][x], p[1].placelist[x]])

      if p[2][1][1] == '=':
        checkt = assignTypeCheck(p[1].typeList[x], p[3].typeList[x])
        if not checkt:
            raise TypeError('mismatch of type of expression in LHS and RHS of = operator')
  #TODO type checking

def p_assign_op(p):
  ''' assign_op : AssignOp'''
  p[0] = ["assign_op", p[1]]

def p_AssignOp(p):
  ''' AssignOp : PLUS_ASSIGN
               | MINUS_ASSIGN
               | STAR_ASSIGN
               | DIVIDE_ASSIGN
               | MOD_ASSIGN
               | AND_ASSIGN
               | OR_ASSIGN
               | XOR_ASSIGN
               | LSHIFT_ASSIGN
               | RSHIFT_ASSIGN
               | ASSIGN '''
  p[0] = ["AssignOp", p[1]]


def p_if_statement(p):
  ''' IfStmt : IF Expression CreateScope Block EndScope ElseOpt'''
  p[0] = Node()
  p[0].code = p[2].code
  label1 = newLabel()
  newVar = newTemp()
  p[0].code += [['=', newVar, p[2].placelist[0]]]
  newVar2 = newTemp()
  p[0].code += [['=',newVar2,'0']]
  p[0].code += [['!=',newVar,newVar, newVar2]]
  newVar3 = newTemp()
  p[0].code += [['=',newVar3, '1']]
  p[0].code += [['-',newVar,newVar,newVar3]]
  p[0].code += [['ifgoto',newVar, label1]]
  p[0].code += p[4].code
  label2 = newLabel()
  p[0].code += [['goto', label2]]
  p[0].code += [['label', label1]]
  p[0].code += p[6].code
  p[0].code += [['label', label2]]


def p_else_opt(p):
  ''' ElseOpt : ELSE IfStmt
              | ELSE CreateScope Block EndScope
              | epsilon '''

  if len(p) == 3:
    p[0] = p[2]
  elif len(p) == 5:
    p[0] = p[3]
  else:
    p[0] = p[1]

# ----------------------------------------------------------------





# ----------- SWITCH STATEMENTS ---------------------------------

def p_switch_statement(p):
  ''' SwitchStmt : ExprSwitchStmt '''
  p[0] = p[1]


def p_expr_switch_stmt(p):
  ''' ExprSwitchStmt : SWITCH Expression CreateScope LCURL StartSwitch ExprCaseClauseRep RCURL EndScope '''
  p[0] = p[2]
  defaultLabel = None
  labnew = newLabel()
  p[0].code += [['goto', labnew]]
  p[0].code += p[6].code
  p[0].code += [['label', labnew]]
  p[0].code += p[6].extra['exprList']

  for i in range(len(p[6].extra['labelList'])):

    if p[6].extra['labelType'][i] == 'default':
        defaultLabel = p[6].extra['labelList'][i]
    else:
        varNew = newTemp()
        p[0].code +=  [['==', varNew, p[2].placelist[0], p[6].placelist[i]]]
        p[0].code += [['ifgoto', varNew, p[6].extra['labelList'][i]]]

  if defaultLabel is not None:
      p[0].code += [['goto', defaultLabel]]


  else:
      l = newLabel()
      p[0].code += [['goto', l]]
      p[0].code += [['label', l]]

  p[0].code += [['label', p[5].extra['end']]]

def p_start_switch(p):
    ''' StartSwitch : '''
    p[0] = Node()
    label2 = newLabel()
    scopeDict[currScope].updateExtra('endFor',label2);
    p[0].extra['end'] = label2




def p_expr_case_clause_rep(p):
  ''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
                        | epsilon'''
  if len(p) == 3:
    p[0] = p[1]
    p[0].code += p[2].code
    p[0].placelist += p[2].placelist
    p[0].extra['labelList'] += p[2].extra['labelList']
    p[0].extra['labelType'] += p[2].extra['labelType']
    p[0].extra['exprList'] += p[2].extra['exprList']


  else:
    p[0] = p[1]
    p[0].extra['labelList'] = []
    p[0].extra['labelType'] = []
    p[0].extra['exprList'] = [[]]



def p_expr_case_clause(p):
  ''' ExprCaseClause : ExprSwitchCase COLON StatementList '''
  p[0] = Node()
  label = newLabel()
  p[0].code = [['label', label]]
  p[0].code += p[3].code
  p[0].extra['labelList'] = [label]
  lab = findLabel('endFor')
  p[0].code.append(['goto', lab])
  p[0].extra['exprList'] = p[1].extra['exprList']
  p[0].placelist = p[1].placelist
  p[0].extra['labelType'] = p[1].extra['labelType']


def p_expr_switch_case(p):
  ''' ExprSwitchCase : CASE Expression
                     | DEFAULT '''
  if len(p) == 3:
    p[0] = p[2]
    p[0].extra['labelType'] = ['case']
    p[0].extra['exprList'] = p[2].code

  else:
    p[0] = Node()
    p[0].extra['labelType'] = ['default']
    p[0].placelist = ['heya']
    p[0].extra['exprList'] = [[]]

# -----------------------------------------------------------




# --------- FOR STATEMENTS AND OTHERS (MANDAL) ---------------
def p_for(p):
  '''ForStmt : FOR CreateScope ConditionBlockOpt Block EndScope'''
  p[0] = Node()
  label1 = p[3].extra['before']
  p[0].code = p[3].code+p[4].code

  if 'forInc' in p[3].extra:
      p[0].code += p[3].extra['forInc']

  p[0].code += [['goto', label1]]
  label2 = p[3].extra['after']
  p[0].code += [['label', label2]]


def p_conditionblockopt(p):
  '''ConditionBlockOpt : epsilon
             | Condition
             | ForClause'''
             # | RangeClause'''
  p[0] = p[1]

def p_condition(p):
  '''Condition : Expression '''
  p[0] = p[1]

def p_forclause(p):
  '''ForClause : SimpleStmt SEMICOLON ConditionOpt SEMICOLON SimpleStmt'''
  p[0] = p[1]
  label1 = newLabel()
  p[0].code += [['label', label1]]
  p[0].extra['before'] = label1
  p[0].code += p[3].code
  label2 = newLabel()
  scopeDict[currScope].updateExtra('beginFor',label1)
  scopeDict[currScope].updateExtra('endFor',label2)

  p[0].extra['after'] = label2
  if len(p[3].placelist) != 0:
    newVar = newTemp()
    newVar2 = newTemp()
    p[0].code += [['=', newVar, p[3].placelist[0]],['=',newVar2,'1'],['-',newVar,newVar2,newVar],['ifgoto', newVar, label2]]
  # p[0].code += p[5].code
  p[0].extra['forInc'] = p[5].code




def p_conditionopt(p):
  '''ConditionOpt : epsilon
          | Condition '''
  p[0] = p[1]

def p_return(p):
  '''ReturnStmt : RETURN ExpressionPureOpt'''
  p[0] = p[2]

  retT = scopeDict[currScope].extra['retT'];
  fName = scopeDict[currScope].extra['fName'];



  if len(p[2].placelist) != 0:
    checkt = assignTypeCheck(retT, p[2].typeList[0])
    if not checkt:
        raise TypeError('function ' + fName+ ' return type: ' + retT + ' doesnt matches with return stmt: ' +p[2].typeList[0])
    p[0].code.append(["retint", p[2].placelist[0]])
  else:
    if(retT != 'void'):
        raise TypeError('function ' + fName+ ' return type: ' + retT + ' doesnt matches with return stmt: void')
    p[0].code.append(["retvoid"])

def p_expression_pure_opt(p):
  '''ExpressionPureOpt : Expression
             | epsilon'''
  p[0] = p[1]

def p_break(p):
  '''BreakStmt : BREAK LabelOpt'''
  if type(p[2]) is list:
  	if p[2][1] not in labelDict:
  		newl = newLabel()
  		labelDict[p[2][1]] = [False, newl]
  	p[0] = Node()
  	p[0].code = [['goto', labelDict[p[2][1]][1]]]
  else:
  	lab = findLabel('endFor')
  	p[0] = Node()
  	p[0].code.append(['goto', lab])

def p_continue(p):
  '''ContinueStmt : CONTINUE LabelOpt'''
  if type(p[2]) is list:
  	if p[2][1] not in labelDict:
  		newl = newLabel()
  		labelDict[p[2][1]] = [False, newl]
  	p[0] = Node()
  	p[0].code = [['goto', labelDict[p[2][1]][1]]]
  else:
  	lab = findLabel('beginFor')
  	p[0] = Node()
  	p[0].code.append(['goto', lab])

def p_labelopt(p):
  '''LabelOpt : Label
        | epsilon '''
  p[0] = p[1]

def p_goto(p):
  '''GotoStmt : GOTO Label '''
  if p[2][1] not in labelDict:
  	newl = newLabel()
  	labelDict[p[2][1]] = [False, newl]
  p[0] = Node()
  p[0].code = [['goto', labelDict[p[2][1]][1]]]

# -----------------------------------------------------------


# ----------------  SOURCE FILE --------------------------------
def p_source_file(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''
    p[0] = p[1]
    p[0].code += p[3].code
    p[0].code += p[4].code

def p_import_decl_rep(p):
  '''ImportDeclRep : epsilon
           | ImportDeclRep ImportDecl SEMICOLON'''
  if len(p) == 4:
    # p[0] = ["ImportDeclRep", p[1], p[2], ";"]
    p[0] = p[1]
    p[0].code += p[2].code
    # print p[2].code
    # print p[0].next.next.code

  else:
    p[0] = p[1]

def p_toplevel_decl_rep(p):
  '''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOLON
                     | epsilon'''
  if len(p) == 4:
    p[0] = p[1]
    # print type(p[1])
    p[0].code += p[2].code
  else:
    p[0] = p[1]
    '''

    p[0] = ["TopLevelDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["TopLevelDeclRep", p[1]]'''
# --------------------------------------------------------


# ---------- PACKAGE CLAUSE --------------------
def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''
    # p[0] = ["PackageClause", "package", p[2]]
    p[0] = p[2]
    # p[0].code = [["package",str(p[2].idList[0])]]

def p_package_name(p):
    '''PackageName : IDENTIFIER'''
    # p[0] = ["PackageName", p[1]]
    p[0] = Node()
    p[0].idList.append(str(p[1]))
    # print p[-1]
    if checkId(p[1], "*"):
        raise NameError("Name " + p[1] + " already defined")
    else:
        scopeDict[0].insert(p[1], "package")
# -----------------------------------------------


# --------- IMPORT DECLARATIONS ---------------
def p_import_decl(p):
  '''ImportDecl : IMPORT ImportSpec
          | IMPORT LPAREN ImportSpecRep RPAREN '''
  if len(p) == 3:
    # p[0] = ["ImportDecl", "import", p[2]]
    p[0] = p[2]
    # p[0].code = [["import"] + p[2].idList]

  else:
    # p[0] = ["ImportDecl", "import", "(", p[3], ")"]
    p[0] = Node()
    # for i in p[3].idList:
    #   p[0].code.append(["import", i])

def p_import_spec_rep(p):
  ''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOLON
            | epsilon '''
  if len(p) == 4:
    # p[0] = ["ImportSpecRep", p[1], p[2], ";"]
    p[0] = p[1]
    # p[0].code += p[2].code
    p[0].idList += p[2].idList

  else:
    p[0] = p[1]

def p_import_spec(p):
  ''' ImportSpec : PackageNameDotOpt ImportPath '''
  # p[0] = ["ImportSpec", p[1], p[2]]
  p[0] = p[1]
  if len(p[1].idList) != 0:
    p[0].idList =  p[1].idList[0] + " " + p[2].idList[0]
  else:
    p[0].idList += p[2].idList


def p_package_name_dot_opt(p):
  ''' PackageNameDotOpt : DOT
                        | PackageName
                        | epsilon'''
  if p[1]== '.':
    p[0] = Node()
    p[0].idList.append(".")
  else:
    p[0] = p[1]

def p_import_path(p):
  ''' ImportPath : STRING '''
  # p[0] = ["ImportPath", p[1]]
  p[0] = Node()
  p[0].idList.append(str(p[1]))
# -------------------------------------------------------


def p_empty(p):
  '''epsilon : '''
  p[0] = Node()

# def p_import_decl(p):








# def p_start(p):
#   '''start : expression'''
#   # p[0] = "<start>" + p[1] + "</start>"
#   p[0] = ['start', p[1]]

# def p_expression_plus(p):
#     '''expression : expression PLUS term
#                   | expression MINUS term'''
#     if p[2] == '+':
#         # p[0] = "<expr>" + p[1] + "</expr> + " + p[3]
#         p[0] = ["expression", p[1], '+', p[3]]
#     else:
#         # p[0] = "<expr>" + p[1] + "</expr> - " + p[3]
#         p[0] = ["expression", p[1], '-', p[3]]
#         # p[0] = p[1] - p[3]
# # def p_expression_minus(p):
# #     'expression : '

# def p_expression_term(p):
#     'expression : term'
#     # p[0] = "<term>" + p[1] + "</term>"
#     p[0] = ["expression", p[1]]

# def p_term_times(p):
#     'term : term STAR factor'
#     # p[0] = "<term>" + p[1] + "</term> * " + "<factor>" + p[3] + "</factor>"
#     p[0] = ["term", p[1], "*", p[3]]



# # def p_term_div(p):
# #     'term : term DIVIDE factor'
# #     p[0] = p[1] / p[3]

# def p_term_factor(p):
#     'term : factor'
#     p[0] = ["term", p[1]]

# def p_factor_num(p):
#     'factor : INTEGER'
#     # p[0] = str(p[1])
#     p[0] = ["factor", str(p[1])]

# # def p_factor_expr(p):
# #     'factor : LPAREN expression RPAREN'
# #     p[0] = p[2]



# Error rule for syntax errors


def p_error(p):
  print("Syntax error in input!")
  print(p)


# Build the parser
parser = yacc.yacc()



nonTerminals = []

def toFindNonTerminals(graph):
  if type(graph) is list:
    nonTerminals.append(graph[0])
    for i in range(1,len(graph),1):
      toFindNonTerminals(graph[i])

def printResult(graph, prev, after):

  word = ""

  if type(graph) is list:

    lastFound = 0
    for i in range (len(graph)-1,0,-1):
      if type(graph[i]) is list:
        if word != "":
          if lastFound==1:
            word = graph[i][0]+ " " + word
          else:
            lastFound = 1
            word =  "<b style='color:red'>" + graph[i][0]+ "</b>" + " " + word
        else:
          if lastFound == 1:
            word = graph[i][0]
          else:
            lastFound = 1
            word = "<b style='color:red'>" + graph[i][0] + "</b>"
      else:
        if word != "":
          word =  graph[i] + " " + word
        else:
          word = graph[i]

    # word = '<span style="color:red">' + word + "</span>"

    if prev != "" and after != "":
      final = prev + " " + word + " "+ after
    elif prev == "" and after == "":
      final = word
    elif prev == "":
      final = word + " " + after
    else :
      final = prev + " " +word

    final = (final.replace(" epsilon", ""))
    toFindNT = final.split()
    # print toFindNT


    # print lastFound
    if lastFound == 0:
      for kk in range(len(toFindNT)-1,-1,-1):
        if toFindNT[kk] in nonTerminals:
          lastFound = 1
          toFindNT[kk] = "<b style='color:red'>" + toFindNT[kk] + "</b>"
          break
    final = ' '.join(toFindNT)
    print  final + "<br/>"



    for i in range(len(graph)-1,0,-1):
      prevNew = prev

      for j in range (1,i):
        if type(graph[j]) is list:
          if prevNew != "":
            prevNew += " " + graph[j][0]
          else :
            prevNew = graph[j][0]
        else:
          if prevNew != "":
            prevNew += " " + graph[j]
          else:
            prevNew = graph[j]
      # print "prev " + prevNew
      afterNew = after
      # print "after " + afterNew
      afterNew = printResult(graph[i],prevNew,afterNew)
      # print "afterNew " + afterNew
      after = afterNew


    return after



  word = graph
  # print "after String " + word + after

  if word != "":
    return word+" "+after
  return after

lineNo = 1
def printList(node):
  global lineNo
  for i in range(0,len(rootNode.code)):
    if len(rootNode.code[i]) > 0:
        toPrint = ""
        toPrint += str(lineNo)
        for j in range(0,len(rootNode.code[i])):
          toPrint += ", " + str(rootNode.code[i][j])

        print toPrint
        lineNo += 1


def checkLabel():
	for x in labelDict:
		# print "aas"
		if labelDict[x][0] == False:
			raise NameError("Label " + x + " is not defined but is directed using Goto !")


try:
  s = data
  print(s)
except EOFError:
  print("khatam bc")
if not s:
  print("bas kar")
result = parser.parse(s)

# print nonTTerminals

#print scopeDict[0].table
#print scopeDict[0].parent
#print currScope
#print scopeDict[1].parent
# print nonTerminals
# print rootNode.code
checkLabel()
file_name = file_name.split("/")[-1].split(".")[0] + ".ir"
sys.stdout = open(file_name, "w+")
printList(rootNode)

