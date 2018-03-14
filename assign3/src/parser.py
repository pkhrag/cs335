import ply.yacc as yacc
import sys
import os
from lexer import tokens, data
from pprint import pprint


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

# ----------------  START --------------------------------
def p_start(p):
    '''start : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''
    p[0] = ["start", p[1], ";", p[3], p[4]]
# --------------------------------------------------------


# ---------- PACKAGE CLAUSE --------------------
def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''
    p[0] = ["PackageClause", "package", p[2]]


def p_package_name(p):
    '''PackageName : IDENTIFIER'''
    p[0] = ["PackageName", p[1]]

def p_package_name_dot_opt(p):
  ''' PackageNameDotOpt : DOT
                        | PackageName
                        | epsilon'''
  if p[1]== '.':
    p[0] = ["PackageNam", "."]
  else:
    p[0] = ["PackageNameDotOpt", p[1]]
# -----------------------------------------------


# --------- IMPORT DECLARATIONS ---------------
def p_import_decl_rep(p):
  '''ImportDeclRep : epsilon
           | ImportDeclRep ImportDecl SEMICOLON'''
  if len(p) == 4:
    p[0] = ["ImportDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["ImportDeclRep", p[1]]

def p_import_decl(p):
  '''ImportDecl : IMPORT ImportSpec
          | IMPORT LPAREN ImportSpecRep RPAREN '''
  if len(p) == 3:
    p[0] = ["ImportDecl", "import", p[2]]
  else:
    p[0] = ["ImportDecl", "import", "(", p[3], ")"]

def p_import_spec_rep(p):
  ''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOLON
            | epsilon '''
  if len(p) == 4:
    p[0] = ["ImportSpecRep", p[1], p[2], ";"]
  else:
    p[0] = ["ImportSpecRep", p[1]]

def p_import_spec(p):
  ''' ImportSpec : PackageNameDotOpt ImportPath '''
  p[0] = ["ImportSpec", p[1], p[2]]

def p_import_path(p):
  ''' ImportPath : STRING '''
  p[0] = ["ImportPath", p[1]]
# -------------------------------------------------------


# ------------------DECLARATIONS and SCOPE------------------------
def p_toplevel_decl_rep(p):
  '''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOLON
                     | epsilon'''
  if len(p) == 4:
    p[0] = ["TopLevelDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["TopLevelDeclRep", p[1]]

def p_toplevel_decl(p):
  '''TopLevelDecl : Declaration
                  | FunctionDecl'''
  p[0] = ["TopLevelDecl", p[1]]

def p_decl(p):
  '''Declaration : ConstDecl
                 | TypeDecl
                 | VarDecl'''
  p[0] = ["Declaration", p[1]]
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
    '''ConstSpec : IdentifierList TypeExprListOpt'''
    p[0] = ["ConstSpec", p[1], p[2]]

def p_type_expr_list(p):
    '''TypeExprListOpt : TypeOpt ASSIGN ExpressionList
                       | epsilon'''
    if len(p) == 4:
        p[0] = ["TypeExprListOpt", p[1], "=", p[3]]
    else:
        p[0] = ["TypeExprListOpt", p[1]]

def p_identifier_list(p):
    '''IdentifierList : IDENTIFIER IdentifierRep'''
    p[0] = ["IdentifierList", str(p[1]), p[2]]

def p_identifier_rep(p):
    '''IdentifierRep : IdentifierRep COMMA IDENTIFIER
                     | epsilon'''
    if len(p) == 4:
        p[0] = ["IdentifierRep", p[1], ",", str(p[3])]
    else:
        p[0] = ["IdentifierRep", p[1]]

def p_expr_list(p):
    '''ExpressionList : Expression ExpressionRep'''
    p[0] = ["ExpressionList", p[1], p[2]]

def p_expr_rep(p):
    '''ExpressionRep : ExpressionRep COMMA Expression
                     | epsilon'''
    if len(p) == 4:
        p[0] = ["ExpressionRep", p[1], ',', p[2]]
    else:
        p[0] = ["ExpressionRep", p[1]]
# -------------------------------------------------------


# ----------------FUNCTION DECLARATIONS------------------
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName Function
                    | FUNC FunctionName Signature'''
    p[0] = ["FunctionDecl", "func", p[1], p[2]]

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''
    p[0] = ["FunctionName", str(p[1])]

def p_func(p):
    '''Function : Signature FunctionBody'''
    p[0] = ["Function", p[1], p[2]]

def p_func_body(p):
    '''FunctionBody : Block'''
    p[0] = ["FunctionBody", p[1]]
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
    p[0] = ["AliasDecl", str(p[1]), '=', p[3]]
# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''
    p[0] = ["TypeDef", str(p[1]), p[2]]
# -------------------------------------------------------


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
        p[0] = ["VarSpecRep", p[1]]

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''
    if p[2] == '=':
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


# -----------------------TYPES---------------------------
def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
    p[0] = ["TypeOpt", p[1]]

def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPAREN Type RPAREN'''
    if len(p) == 4:
        p[0] = ["Type", "(", p[2], ")"]
    else:
        p[0] = ["Type", p[1]]

def p_type_name(p):
    '''TypeName : IDENTIFIER
                | QualifiedIdent'''
    p[0] = ["TypeName", p[1]]

def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PointerType'''
    p[0] = ["TypeLit", p[1]]
# -------------------------------------------------------


# -------------------QUALIFIED IDENTIFIER----------------
def p_quali_ident(p):
    '''QualifiedIdent : PackageName DOT IDENTIFIER'''
    p[0] = ["QualifiedIdent", p[1], ".", str(p[3])]
# -------------------------------------------------------


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
        p[0] = ["UnaryOp", "+"]
    elif p[1] == '&':
        p[0] = ["UnaryOp", "&"]

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
  '''StructType : STRUCT LCURL FieldDeclRep RCURL'''
  p[0] = ["StructType", "struct", "{", p[3], "}"]

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


# ------------------PRIMARY EXPRESSIONS--------------------
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | Conversion
                   | PrimaryExpr Selector
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
    p[0] = ["Selector", ".", str(p[2])]

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
    '''ExpressionListTypeOpt : ExpressionList CommaOpt
                             | Type ExpressionListCommaOpt CommaOpt'''
    if len(p) == 3:
        p[0] = ["ExpressionListTypeOpt", p[1], p[2]]
    else:
        p[0] = ["ExpressionListTypeOpt", p[1], p[2], p[3]]

def p_comma_opt(p):
    '''CommaOpt : COMMA
                | epsilon'''
    if p[1] == ",":
        p[0] = ["CommaOpt", ","]
    else:
        p[0] = ["CommaOpt", p[1]]

def p_expr_list_comma_opt(p):
    '''ExpressionListCommaOpt : COMMA ExpressionList
                              | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListCommaOpt", ",", p[2]]
    else:
        p[0] = ["ExpressionListCommaOpt", p[1]]
# ---------------------------------------------------------


# -----------------CONVERSIONS-----------------------------
def p_conversion(p):
    '''Conversion : Type LPAREN Expression CommaOpt RPAREN'''
    p[0] = ["Conversion", p[1], "(", p[3], p[4], ")"]
# ---------------------------------------------------------


# ----------------------OPERAND----------------------------
def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''
    if len(p) == 2:
        p[0] = ["Operand", p[1]]
    else:
        p[0] = ["Operand", "(". p[2], ")"]

def p_literal(p):
    '''Literal : BasicLit
               | CompositeLit'''
    p[0] = ["Literal", p[1]]

def p_basic_lit(p):
    '''BasicLit : INTEGER
                | FLOAT
                | IMAGINARY
                | RUNE
                | STRING'''
    p[0] = ["BasicLit", str(p[1])]

def p_operand_name(p):
    '''OperandName : IDENTIFIER
                   | QualifiedIdent'''
    p[0] = ["OperandName", p[1]]
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
    '''Parameters : LPAREN ParameterListCommaOpt RPAREN'''
    p[0] = ["Parameters", "(", p[2], ")"]

def p_param_list_comma_opt(p):
    '''ParameterListCommaOpt : ParametersList CommaOpt
                             | epsilon'''
    if len(p) == 3:
        p[0] = ["ParameterListCommaOpt", p[1], p[2]]
    else:
        p[0] = ["ParameterListCommaOpt", p[1]]

def p_param_list(p):
    '''ParametersList : ParameterDecl ParameterDeclCommaRep'''
    p[0] = ["ParametersList", p[1], p[2]]

def p_param_decl_comma_rep(p):
    '''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
                             | epsilon'''
    if len(p) == 4:
        p[0] = ["ParameterDeclCommaRep", p[1], ",", p[3]]
    else:
        p[0] = ["ParameterDeclCommaRep", p[1]]

def p_param_decl(p):
    '''ParameterDecl : IdentifierList Type
                     | Type'''
    if len(p) == 3:
        p[0] = ["ParameterDecl", p[1], p[2]]
    else:
        p[0] = ["ParameterDecl", p[1]]
# ---------------------------------------------------------


# -----------------COMPOSITE LITERALS----------------------
def p_comp_lit(p):
    '''CompositeLit : LiteralType LiteralValue'''
    p[0] = ["CompositeLit", p[1], p[2]]

def p_lit_type(p):
    '''LiteralType : StructType
                   | ArrayType
                   | ElementType
                   | TypeName'''
    p[0] = ["LiteralType", p[1]]

def p_lit_val(p):
    '''LiteralValue : LPAREN ElementListCommaOpt RPAREN'''
    p[0] = ["LiteralValue", "{", p[2], "}"]

def p_elem_list_comma_opt(p):
    '''ElementListCommaOpt : ElementList CommaOpt
                           | epsilon'''
    if len(p) == 3:
        p[0] = ["ElementListCommaOpt", p[1], p[2]]
    else:
        p[0] = ["ElementListCommaOpt", p[1]]

def p_elem_list(p):
    '''ElementList : KeyedElement KeyedElementCommaRep'''
    p[0] = ["ElementList", p[1], p[2]]

def p_key_elem_comma_rep(p):
    '''KeyedElementCommaRep : KeyedElementCommaRep COMMA KeyedElement
                            | epsilon'''
    if len(p) == 4:
        p[0] = ["KeyedElementCommaRep", p[1], ",", p[3]]
    else:
        p[0] = ["KeyedElementCommaRep", p[1]]

def p_key_elem(p):
    '''KeyedElement : Key COLON Element
                    | Element'''
    if len(p) == 4:
        p[0] = ["KeyedElement", p[1], ":", p[3]]
    else:
        p[0] = ["KeyedElement", p[1]]

def p_key(p):
    '''Key : FieldName
           | Expression
           | LiteralValue'''
    p[0] = ["Key", p[1]]

def p_field_name(p):
    '''FieldName : IDENTIFIER'''
    p[0] = ["FieldName", p[1]]

def p_elem(p):
    '''Element : Expression
               | LiteralValue'''
    p[0] = ["Element", p[1], p[2]]
# ---------------------------------------------------------


#TODO
def p_stat(p):
    '''Statement : epsilon'''
    p[0] = ["Statement", p[1]]



def p_empty(p):
  '''epsilon : '''
  p[0] = "epsilon"

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


# Build the parser
parser = yacc.yacc()



def printResult(graph, prev, after):

  word = ""

  if type(graph) is list:
    for i in range (1,len(graph)):
      if type(graph[i]) is list:
        if word != "":
          word = word + " " +graph[i][0]
        else:
          word = graph[i][0]
      else:
        if word != "":
          word += " "+graph[i]
        else:
          word = graph[i]



    if prev != "" and after != "":
      final = prev + " " + word + " "+ after
    elif prev == "" and after == "":
      final = word
    elif prev == "":
      final = word + " " + after
    else :
      final = prev + " " +word
    print final.replace(" epsilon", "")



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






try:
  s = data
  print(s)
except EOFError:
  print("khatam bc")
if not s:
  print("bas kar")
result = parser.parse(s)

print "start"
printResult(result, "" , "")

