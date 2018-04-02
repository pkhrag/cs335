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

def checkId(identifier, typeOf):
    if typeOf == "*":
        if scopeDict[currScope].getInfo(identifier) is not None:
            info = scopeDict[currScope].getInfo(identifier)
            return True
        return False

    if typeOf == "*!s":
        if scopeDict[currScope].getInfo(identifier) is not None:
            info = scopeDict[currScope].getInfo(identifier)
            if info['type'] is not 'type':
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
            if checkId(name, '*'):
                raise NameError("Name " + name + " already defined")
            scopeDict[lastScope].insert(name, 'type')
            scopeDict[lastScope].updateArgList(name, 'child', scopeDict[currScope])


def deleteScope():
    global currScope
    currScope = scopeStack.pop()
    currScope = scopeStack[-1]

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
    ('left', 'STAR', 'DIVIDE','MOD'),
)


# ------------- IR GENERATION -----------

class Node:
    def __init__(self):
        self.idList = []
        self.code = []
        self.type = None
        self.next = None
        self.place = None
        self.extra = None



def default(typeOf):
  if typeOf == "int_t":
    return str(0)


def expressionListLength(x):
  l = 0
  while x is not None:
    x = x.next
    l += 1
  return l

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
        p[0] = ["Type", "(", p[2], ")"]
    else:
        p[0] = ["Type", p[1]]

def p_type_name(p):
    '''TypeName : TypeToken
                | QualifiedIdent'''
    p[0] = ["TypeName", p[1]]

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
        p[0] = ["TypeToken", p[1]]
    else:
        if not checkId(p[2], p[1]):
            raise TypeError("Typename " + p[2] + " not defined")
        p[0] = ["TypeToken", p[1], p[2]]

def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PointerType'''
    p[0] = ["TypeLit", p[1]]

def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
    p[0] = ["TypeOpt", p[1]]
# -------------------------------------------------------





# ------------------- ARRAY TYPE -------------------------
def p_array_type(p):
  '''ArrayType : LSQUARE ArrayLength RSQUARE ElementType'''
  p[0] = ["ArrayType", "[", p[2], "]", p[4]]

def p_array_length(p):
  ''' ArrayLength : Expression '''
  p[0] = ["ArrayLength", p[1]]

def p_element_type(p):
  ''' ElementType : Type '''
  p[0] = ["ElementType", p[1]]

# --------------------------------------------------------


# ----------------- STRUCT TYPE ---------------------------
def p_struct_type(p):
  '''StructType : CreateFuncScope STRUCT LCURL FieldDeclRep RCURL EndScope'''
  p[0] = ["StructType", "struct", "{", p[4], "}"]

def p_field_decl_rep(p):
  ''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                  | epsilon '''
  if len(p) == 4:
    p[0] = ["FieldDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["FieldDeclRep", p[1]]

def p_field_decl(p):
  ''' FieldDecl : IdentifierList Type TagOpt'''
  p[0] = ["FieldDecl", p[1], p[2], p[3]]

def p_TagOpt(p):
  ''' TagOpt : Tag
             | epsilon '''
  p[0] = ["TagOpt", p[1]]

def p_Tag(p):
  ''' Tag : STRING '''
  p[0] = ["Tag", p[1]]
# ---------------------------------------------------------


# ------------------POINTER TYPES--------------------------
def p_point_type(p):
    '''PointerType : STAR BaseType'''
    p[0] = ["PointerType", "*", p[2]]

def p_base_type(p):
    '''BaseType : Type'''
    p[0] = ["BaseType", p[1]]
# ---------------------------------------------------------


# ---------------FUNCTION TYPES----------------------------
def p_sign(p):
    '''Signature : Parameters ResultOpt'''
    p[0] = ["Signature", p[1], p[2]]

def p_result_opt(p):
    '''ResultOpt : Result
                 | epsilon'''
    p[0] = ["ResultOpt", p[1]]

def p_result(p):
    '''Result : Parameters
              | Type'''
    p[0] = ["Result", p[1]]

def p_params(p):
    '''Parameters : LPAREN ParameterListOpt RPAREN'''
    p[0] = ["Parameters", "(", p[2], ")"]

def p_param_list_opt(p):
    '''ParameterListOpt : ParametersList
                             | epsilon'''
    p[0] = ["ParameterListOpt", p[1]]

def p_param_list(p):
    '''ParametersList : Type
                      | IdentifierList Type
                      | ParameterDeclCommaRep'''
    if len(p) == 3:
        p[0] = ["ParametersList", p[1], p[2]]
    else:
        p[0] = ["ParametersList", p[1]]

def p_param_decl_comma_rep(p):
    '''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
                             | ParameterDecl COMMA ParameterDecl'''
    p[0] = ["ParameterDeclCommaRep", p[1], ",", p[3]]

def p_param_decl(p):
    '''ParameterDecl : IdentifierList Type
                     | Type'''
    if len(p) == 3:
        p[0] = ["ParameterDecl", p[1], p[2]]
    else:
        p[0] = ["ParameterDecl", p[1]]
# ---------------------------------------------------------


#-----------------------BLOCKS---------------------------
def p_block(p):
    '''Block : LCURL StatementList RCURL'''
    p[0] = ["Blocks", "{" , p[2], "}"]

def p_stat_list(p):
    '''StatementList : StatementRep'''
    p[0] = ["StatementList", p[1]]

def p_stat_rep(p):
    '''StatementRep : StatementRep Statement SEMICOLON
                    | epsilon'''
    if len(p) == 4:
        p[0] = ["StatementRep", p[1], p[2], ';']
    else:
        p[0] = ["StatementRep", p[1]]
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
        p[0] = ["ConstDecl", "const", p[2]]
    else:
        p[0] = ["ConstDecl", "const", '(', p[3], ')']

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | epsilon'''
    if len(p) == 4:
        p[0] = ["ConstSpecRep", p[1], p[2], ';']
    else:
        p[0] = ["ConstSpecRep", p[1]]

def p_const_spec(p):
    '''ConstSpec : IdentifierList Type ASSIGN ExpressionList'''
    p[0] = ["ConstSpec", p[1], p[2], "=", p[4]]
    #TODO insert type in symbol table

#def p_type_expr_list(p):
#    '''TypeExprListOpt : '''
#    p[0] = ["TypeExprListOpt", p[1], "=", p[3]]

def p_identifier_list(p):
    '''IdentifierList : IDENTIFIER IdentifierRep'''
    p[0] = ["IdentifierList", p[1], p[2]]
    if checkId(p[1], "*"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        scopeDict[currScope].insert(p[1], None)

def p_identifier_rep(p):
    '''IdentifierRep : IdentifierRep COMMA IDENTIFIER
                     | epsilon'''
    if len(p) == 4:
        p[0] = ["IdentifierRep", p[1], ",", p[3]]
        if checkId(p[3], "*"):
            raise NameError("Name " + p[3] + " already exists, can't redefine")
        else:
            scopeDict[currScope].insert(p[3], None)
    else:
        p[0] = ["IdentifierRep", p[1]]

def p_expr_list(p):
    '''ExpressionList : Expression ExpressionRep'''
    p[0] = ["ExpressionList", p[1], p[2]]

def p_expr_rep(p):
    '''ExpressionRep : ExpressionRep COMMA Expression
                     | epsilon'''
    if len(p) == 4:
        p[0] = ["ExpressionRep", p[1], ',', p[3]]
    else:
        p[0] = ["ExpressionRep", p[1]]
# -------------------------------------------------------


# ------------------TYPE DECLARATIONS-------------------
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPAREN TypeSpecRep RPAREN'''
    if len(p) == 5:
        p[0] = ["TypeDecl", "type", "(", p[3], ")"]
    else:
        p[0] = ["TypeDecl", "type", p[2]]

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpecRep TypeSpec SEMICOLON
                   | epsilon'''
    if len(p) == 4:
        p[0] = ["TypeSpecRep", p[1], p[2], ";"]
    else:
        p[0] = ["TypeSpecRep", p[1]]

def p_type_spec(p):
    '''TypeSpec : AliasDecl
                | TypeDef'''
    p[0] = ["TypeSpec", p[1]]

def p_alias_decl(p):
    '''AliasDecl : IDENTIFIER ASSIGN Type'''
    p[0] = ["AliasDecl", p[1], '=', p[3]]
    if checkId(p[1], "*"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        scopeDict[currScope].insert(p[1], None)
# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''
    p[0] = ["TypeDef", p[1], p[2]]
    if checkId(p[1], "*!s"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        scopeDict[currScope].insert(p[1], None)
# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------
def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPAREN VarSpecRep RPAREN'''
    if len(p) == 3:
        p[0] = ["VarDecl", "var", p[2]]
    else:
        p[0] = ["VarDecl", "var", "(", p[3], ")"]

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpecRep VarSpec SEMICOLON
                  | epsilon'''
    if len(p) == 4:
        p[0] = ["VarSpecRep", p[1], p[2], ";"]
    else:
#        p[0] = p[1]
        p[0] = ["VarSpecRep", p[1]]

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''
    if p[2] == '=':
        '''
      p[0] = Node()
      if(len(p[1].code) != len(p[2].code)):
        print "Error: mismatch in number of identifiers and expressions for asisgnment"
        sys.exit()

      p[0].code = p[1].code
      for i in range(0, len(p[2])):
        p[0].code.append(["=",p[1].code[i][1],p[2][i].place])
      pass
        '''
        p[0] = ["VarSpec", p[1], "=", p[3]]
    else:
        p[0] = ["VarSpec", p[1], p[2], p[3]]

def p_expr_list_opt(p):
    '''ExpressionListOpt : ASSIGN ExpressionList
                         | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListOpt", "=", p[2]]
    else:
        p[0] = ["ExpressionListOpt", p[1]]
# -------------------------------------------------------


# ----------------SHORT VARIABLE DECLARATIONS-------------
def p_short_var_decl(p):
  ''' ShortVarDecl : IDENTIFIER QUICK_ASSIGN Expression '''
  p[0] = ["ShortVarDecl", p[1], ":=", p[3]]
  if checkId(p[1], "*"):
    raise NameError("Name " + p[1] + " already exists, can't redefine")
  else:
    scopeDict[currScope].insert(p[1], None)
# -------------------------------------------------------



# ----------------FUNCTION DECLARATIONS------------------
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName CreateFuncScope Function EndScope
                    | FUNC FunctionName CreateFuncScope Signature EndScope'''
    p[0] = ["FunctionDecl", "func", p[2], p[4]]

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
    if checkId(p[1], "*"):
        raise NameError("Name " + p[1] + " already exists, can't redefine")
    else:
        scopeDict[currScope].insert(p[1], "func")

def p_func(p):
    '''Function : Signature FunctionBody'''
    p[0] = ["Function", p[1], p[2]]
    # print p[-2]

def p_func_body(p):
    '''FunctionBody : Block'''
    p[0] = ["FunctionBody", p[1]]
# -------------------------------------------------------


# ----------------------OPERAND----------------------------
def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''
    if len(p) == 2:
        p[0] = ["Operand", p[1]]
    else:
        p[0] = ["Operand", "(", p[2], ")"]

def p_literal(p):
    '''Literal : BasicLit'''
               #| CompositeLit'''
    p[0] = ["Literal", p[1]]

def p_basic_lit(p):
    '''BasicLit : INTEGER
                | OCTAL
                | HEX
                | FLOAT
                | IMAGINARY
                | RUNE
                | STRING'''
    p[0] = ["BasicLit",str(p[1])]

def p_operand_name(p):
    '''OperandName : IDENTIFIER'''
    p[0] = ["OperandName", p[1]]
    if not checkId(p[1], "**"):
        raise NameError("Identifier " + p[1] + " not defined")
# ---------------------------------------------------------


# -------------------QUALIFIED IDENTIFIER----------------
def p_quali_ident(p):
    '''QualifiedIdent : IDENTIFIER DOT TypeName'''
    p[0] = ["QualifiedIdent", p[1], ".", p[3]]
    if not checkId(p[1], "package"):
        raise NameError("Package " + p[1] + " not included")

# -------------------------------------------------------


# ------------------PRIMARY EXPRESSIONS--------------------
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | PrimaryExpr Selector
                   | Conversion
                   | PrimaryExpr Index
                   | PrimaryExpr Slice
                   | PrimaryExpr TypeAssertion
                   | PrimaryExpr Arguments'''
    if len(p) == 2:
        p[0] = ["PrimaryExpr", p[1]]
    else:
        p[0] = ["PrimaryExpr", p[1], p[2]]

def p_selector(p):
    '''Selector : DOT IDENTIFIER'''
    p[0] = ["Selector", ".", p[2]]
    #TODO struct

def p_index(p):
    '''Index : LSQUARE Expression RSQUARE'''
    p[0] = ["Index", "[", p[2], "]"]

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

def p_argument(p):
    '''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''
    p[0] = ["Arguments", "(", p[2], ")"]

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                             | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListTypeOpt", p[1], p[2]]
    else:
        p[0] = ["ExpressionListTypeOpt", p[1]]

#def p_comma_opt(p):
#    '''CommaOpt : COMMA
#                | epsilon'''
#    if p[1] == ",":
#        p[0] = ["CommaOpt", ","]
#    else:
#        p[0] = ["CommaOpt", p[1]]

def p_expr_list_comma_opt(p):
    '''ExpressionListCommaOpt : COMMA ExpressionList
                              | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListCommaOpt", ",", p[2]]
    else:
        p[0] = ["ExpressionListCommaOpt", p[1]]
# ---------------------------------------------------------


#----------------------OPERATORS-------------------------
def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression BinaryOp Expression'''
    if len(p) == 4:
        p[0] = ["Expression", p[1], p[2], p[3]]
    else:
        p[0] = ["Expression", p[1]]

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                     | epsilon'''
    p[0] = ["ExpressionOpt", p[1]]

def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr
                 | UnaryOp UnaryExpr
                 | NOT UnaryExpr'''
    if len(p) == 2:
        p[0] = ["UnaryExpr", p[1]]
    elif p[1] == "!":
        p[0] = ["UnaryExpr", "!", p[2]]
    else:
        p[0] = ["UnaryExpr", p[1], p[2]]

def p_binary_op(p):
    '''BinaryOp : LOGICAL_OR
                | LOGICAL_AND
                | RelOp
                | AddMulOp'''
    if p[1] == "||":
        p[0] = ["BinaryOp", "||"]
    elif p[1] == "&&":
        p[0] = ["BinaryOp", "&&"]
    else:
        p[0] = ["BinaryOp", p[1]]

def p_rel_op(p):
    '''RelOp : EQUALS
             | NOT_ASSIGN
             | LESSER
             | GREATER
             | LESS_EQUALS
             | MORE_EQUALS'''
    if p[1] == "==":
        p[0] = ["RelOp", "=="]
    elif p[1] == "!=":
        p[0] = ["RelOp", "!="]
    elif p[1] == "<":
        p[0] = ["RelOp", "<"]
    elif p[1] == ">":
        p[0] = ["RelOp", ">"]
    elif p[1] == "<=":
        p[0] = ["RelOp", "<="]
    elif p[1] == ">=":
        p[0] = ["RelOp", ">="]

def p_add_mul_op(p):
    '''AddMulOp : UnaryOp
                | OR
                | XOR
                | DIVIDE
                | MOD
                | LSHIFT
                | RSHIFT'''
    if p[1] == "/":
        p[0] = ["AddMulOp", "/"]
    elif p[1] == "%":
        p[0] = ["AddMulOp", "%"]
    elif p[1] == "|":
        p[0] = ["AddMulOp", "|"]
    elif p[1] == "^":
        p[0] = ["AddMulOp", "^"]
    elif p[1] == "<<":
        p[0] = ["AddMulOp", "<<"]
    elif p[1] == ">>":
        p[0] = ["AddMulOp", ">>"]
    else:
        p[0] = ["AddMulOp", p[1]]

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
    p[0] = ["Conversion", p[1], p[2],  "(", p[4], ")"]
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
                 | ForStmt '''
    if len(p) == 2:
        p[0] = ["Statement", p[1]]
    else:
        p[0] = ["Statement", p[2]]



def p_simple_stmt(p):
  ''' SimpleStmt : epsilon
                 | ExpressionStmt
                 | IncDecStmt
                 | Assignment
                 | ShortVarDecl '''
  p[0] = ["SimpleStmt", p[1]]


def p_labeled_statements(p):
  ''' LabeledStmt : Label COLON Statement '''
  p[0] = ["LabeledStmt", p[1], ":", p[3]]

def p_label(p):
  ''' Label : IDENTIFIER '''
  p[0] = ["Label", p[1]]
  if checkId(p[1], "label"):
    raise NameError("Label " + p[1] + " already exists, can't redefine")
  else:
    scopeDict[0].insert(p[1], "label")


def p_expression_stmt(p):
  ''' ExpressionStmt : Expression '''
  p[0] = ["ExpressionStmt", p[1]]

def p_inc_dec(p):
  ''' IncDecStmt : Expression INCR
                 | Expression DECR '''
  if p[2] == '++':
    p[0] = ["IncDecStmt", p[1], "++"]
  else:
    p[0] = ["IncDecStmt", p[1], "--"]


def p_assignment(p):
  ''' Assignment : ExpressionList assign_op ExpressionList'''
  p[0] = ["Assignment", p[1], p[2], p[3]]

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
  ''' IfStmt : IF Expression CreateScope Block EndScope ElseOpt '''
  p[0] = ["IfStmt", "if", p[2], p[4], p[6]]

def p_SimpleStmtOpt(p):
  ''' SimpleStmtOpt : SimpleStmt SEMICOLON
                    | epsilon '''
  if len(p) == 3:
    p[0] = ["SimpleStmtOpt", p[1], ";"]
  else :
    p[0] = ["SimpleStmtOpt", p[1]]

def p_else_opt(p):
  ''' ElseOpt : ELSE IfStmt
              | ELSE CreateScope Block EndScope
              | epsilon '''
  if len(p) == 3:
    p[0] = ["ElseOpt", "else", p[2]]
  elif len(p) == 5:
    p[0] = ["ElseOpt", "else", p[3]]
  else:
    p[0] = ["ElseOpt", p[1]]

# ----------------------------------------------------------------





# ----------- SWITCH STATEMENTS ---------------------------------

def p_switch_statement(p):
  ''' SwitchStmt : ExprSwitchStmt
                 | TypeSwitchStmt '''
  p[0] = ["SwitchStmt", p[1]]


def p_expr_switch_stmt(p):
  ''' ExprSwitchStmt : SWITCH ExpressionOpt LCURL ExprCaseClauseRep RCURL'''
  p[0] = ["ExpressionStmt", "switch", p[2], p[3], "{", p[5], "}"]

def p_expr_case_clause_rep(p):
  ''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
                        | epsilon'''
  if len(p) == 3:
    p[0] = ["ExprCaseClauseRep", p[1], p[2]]
  else:
    p[0] = ["ExprCaseClauseRep", p[1]]

def p_expr_case_clause(p):
  ''' ExprCaseClause : ExprSwitchCase COLON StatementList'''
  p[0] = ["ExprCaseClause", p[1], ":", p[3]]

def p_expr_switch_case(p):
  ''' ExprSwitchCase : CASE ExpressionList
                     | DEFAULT '''
  if len(p) == 3:
    p[0] = ["ExprSwitchCase", "case", p[2]]
  else:
    p[0] = ["ExprSwitchCase", p[1]]

def p_type_switch_stmt(p):
  ''' TypeSwitchStmt : SWITCH SimpleStmtOpt TypeSwitchGuard LCURL TypeCaseClauseOpt RCURL'''
  p[0] = ["TypeSwitchStmt", "switch", p[2], p[3],"{", p[5], "}"]


def p_type_switch_guard(p):
  ''' TypeSwitchGuard : IdentifierOpt PrimaryExpr DOT LPAREN TYPE RPAREN '''

  p[0] = ["TypeSwitchGuard", p[1], p[2], ".", "(", "type", ")"]

def p_identifier_opt(p):
  ''' IdentifierOpt : IDENTIFIER QUICK_ASSIGN
                    | epsilon '''
  #TODO
  if len(p) == 3:
    p[0] = ["IdentifierOpt", p[1], ":="]
  else:
    p[0] = ["IdentifierOpt", p[1]]

def p_type_case_clause_opt(p):
  ''' TypeCaseClauseOpt : TypeCaseClauseOpt TypeCaseClause
                        | epsilon '''
  if len(p) == 3:
    p[0] = ["TypeCaseClauseOpt", p[1], p[2]]
  else:
    p[0] = ["TypeCaseClauseOpt", p[1]]

def p_type_case_clause(p):
  ''' TypeCaseClause : TypeSwitchCase COLON StatementList'''
  p[0] = ["TypeCaseClause", p[1], ":", p[3]]


def p_type_switch_case(p):
  ''' TypeSwitchCase : CASE TypeList
                     | DEFAULT '''
  if len(p) == 3:
    p[0] = ["TypeSwitchCase", p[1], p[2]]
  else:
    p[0] = ["TypeSwitchCase", p[1]]

def p_type_list(p):
  ''' TypeList : Type TypeRep'''
  p[0] = ["TypeList", p[1], p[2]]

def p_type_rep(p):
  ''' TypeRep : TypeRep COMMA Type
              | epsilon '''
  if len(p) == 4:
    p[0] = ["TypeRep", p[1], ",", p[3]]
  else:
    p[0] = ["TypeRep", p[1]]

# -----------------------------------------------------------






# --------- FOR STATEMENTS AND OTHERS (MANDAL) ---------------
def p_for(p):
  '''ForStmt : FOR CreateScope ConditionBlockOpt Block EndScope'''
  p[0] = ["ForStmt", "for", p[3], p[4]]

def p_conditionblockopt(p):
  '''ConditionBlockOpt : epsilon
             | Condition
             | ForClause
             | RangeClause'''
  p[0] = ["ConditionBlockOpt", p[1]]

def p_condition(p):
  '''Condition : Expression '''
  p[0] = ["Condition", p[1]]

def p_forclause(p):
  '''ForClause : SimpleStmt SEMICOLON ConditionOpt SEMICOLON SimpleStmt'''
  p[0] = ["ForClause", p[1], ";", p[3], ";", p[5]]

# def p_initstmtopt(p):
#   '''InitStmtOpt : epsilon
#            | InitStmt '''
#   p[0] = ["InitStmtOpt", p[1]]

# def p_init_stmt(p):
#   ''' InitStmt : SimpleStmt'''
#   p[0] = ["InitStmt", p[1]]


def p_conditionopt(p):
  '''ConditionOpt : epsilon
          | Condition '''
  p[0] = ["ConditionOpt", p[1]]

# def p_poststmtopt(p):
#   '''PostStmtOpt : epsilon
#            | PostStmt '''
#   p[0] = ["PostStmtOpt", p[1]]

# def p_post_stmt(p):
#   ''' PostStmt : SimpleStmt '''
#   # p[0] = ["PostStmt", p[1]]

def p_rageclause(p):
  '''RangeClause : ExpressionIdentListOpt RANGE Expression'''
  p[0] = ["RangeClause", p[1], "range", p[3]]

def p_expression_ident_listopt(p):
  '''ExpressionIdentListOpt : epsilon
             | ExpressionIdentifier'''
  p[0] = ["ExpressionIdentListOpt", p[1]]

def p_expressionidentifier(p):
  '''ExpressionIdentifier : ExpressionList ASSIGN'''
  if p[2] == "=":
    p[0] = ["ExpressionIdentifier", p[1], "="]
  else:
    p[0] = ["ExpressionIdentifier", p[1], ":="]

def p_return(p):
  '''ReturnStmt : RETURN ExpressionListPureOpt'''
  p[0] = ["ReturnStmt", "return", p[2]]

def p_expressionlist_pure_opt(p):
  '''ExpressionListPureOpt : ExpressionList
             | epsilon'''
  p[0] = ["ExpressionListPureOpt", p[1]]

def p_break(p):
  '''BreakStmt : BREAK LabelOpt'''
  p[0] = ["BreakStmt", "break", p[2]]

def p_continue(p):
  '''ContinueStmt : CONTINUE LabelOpt'''
  p[0] = ["ContinueStmt", "continue", p[2]]

def p_labelopt(p):
  '''LabelOpt : Label
        | epsilon '''
  p[0] = ["LabelOpt", p[1]]

def p_goto(p):
  '''GotoStmt : GOTO Label '''
  p[0] = ["GotoStmt", "goto", p[2]]
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
    p[0].code = [["package",str(p[2].idList[0])]]

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
    p[0].code = [["import"] + p[2].idList]

  else:
    # p[0] = ["ImportDecl", "import", "(", p[3], ")"]
    p[0] = Node()
    for i in p[3].idList:
      p[0].code.append(["import", i])

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
    toPrint = ""
    toPrint += str(lineNo)
    for j in range(0,len(rootNode.code[i])):
      toPrint += ", " + rootNode.code[i][j]

    print toPrint
    lineNo += 1

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

printList(rootNode)
file_name = file_name.split("/")[-1].split(".")[0] + ".html"
sys.stdout = open(file_name, "w+")
print "<!DOCTYPE html>\
<html><head>"
print "<b style='color:red'>Start</b><br>"

#printResult(result, "" , "")
print "</head></html>"