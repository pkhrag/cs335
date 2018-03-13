import ply.yacc as yacc
import sys
import os
from lexer import tokens, data
from pprint import pprint


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
        p[0] = ["IdentifierRep", p[1], ",", str(p[2])]
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
    if len(p) == 5
        p[0] = ["TypeDecl", "type", "(", p[3], ")"]
    else:
        p[0] = ["TypeDecl", "type", p[1]]

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

# TODO
def p_var_decl(p):
    '''VarDecl : epsilon'''
    p[0] = ["VarDecl", p[1]]

#TODO
def p_expr(p):
    '''Expression : epsilon'''
    p[0] = ["Expression", p[1]]

def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
    p[0] = ["TypeOpt", p[1]]

#TODO
def p_type(p):
    '''Type : epsilon'''
    p[0] = ["Type", p[1]]


#TODO
def p_sign(p):
    '''Signature : epsilon'''
    p[0] = ["Signature", p[1]]

#TODO
def p_block(p):
    '''Block : epsilon'''
    p[0] = ["Block", p[1]]


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
		print final
	


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

print(result)
