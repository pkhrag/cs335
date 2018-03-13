import ply.yacc as yacc
import sys
import os
from lexer import tokens, data
from pprint import pprint


# def p_expression_plus(p):
#     'expression : expression PLUS term'
#     p[0] = p[1] + p[3]

# def p_star(p):
#     '''start : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''
#     p[0] = "<START> <PackageClause>" + p[1] + "</PackageClause>" + "<SEMICOLON/> <ImportDecl>" + str(p[3]) + "</ImportDecl> <SEMICOLON/> </START>"

# def p_import_decl_rep(p):
# 	'''ImportDeclRep : ImportDeclRep ImportDecl 
# 					 | epsilon'''
# 	if len(p) == 3:
# 		if p[1]:
# 			p[0] = p[1] + p[2]
# 		else:
# 			p[0] = p[2]

# def p_package_clause(p):
#     '''PackageClause : PACKAGE PackageName'''
#     p[0] = "<PACKAGE/>" + "<PackageName>" + p[2] + "</PackageName>"

# def p_package_name(p):
#     '''PackageName : IDENTIFIER '''
#     p[0] = "<IDENTIFIER>" + p[1] + "</IDENTIFIER>"

# def p_import_decl(p):
# 	'''ImportDecl : IMPORT SEMICOLON'''
# 	p[0] = "<IMPORT/> <SEMICOLON/>"

# def p_toplevel_decl_rep(p):
# 	'''TopLevelDeclRep : epsilon 
# 					   | TopLevelDeclRep TopLevelDecl'''

# def p_toplevel_decl(p):
# 	'''TopLevelDecl : epsilon'''

# def p_empty(p):
# 	'''epsilon :'''

# def p_import_decl(p):

def p_start(p):
	'''start : expression'''
	# p[0] = "<start>" + p[1] + "</start>"
	p[0] = ['start', p[1]]

def p_expression_plus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        # p[0] = "<expr>" + p[1] + "</expr> + " + p[3]
        p[0] = ["expression", p[1], '+', p[3]]
    else:
        # p[0] = "<expr>" + p[1] + "</expr> - " + p[3]
        p[0] = ["expression", p[1], '-', p[3]]
        # p[0] = p[1] - p[3]
# def p_expression_minus(p):
#     'expression : '

def p_expression_term(p):
    'expression : term'
    # p[0] = "<term>" + p[1] + "</term>"
    p[0] = ["expression", p[1]]

def p_term_times(p):
    'term : term STAR factor'
    # p[0] = "<term>" + p[1] + "</term> * " + "<factor>" + p[3] + "</factor>"
    p[0] = ["term", p[1], "*", p[3]]

# def p_term_div(p):
#     'term : term DIVIDE factor'
#     p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = ["term", p[1]]

def p_factor_num(p):
    'factor : INTEGER'
    # p[0] = str(p[1])
    p[0] = ["factor", str(p[1])]

# def p_factor_expr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]



# Error rule for syntax errors


def p_error(p):
  print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

try:
  s = data
  print(s)
except EOFError:
  print("khatam bc")
if not s:
  print("bas kar")
result = parser.parse(s)
# with open("tree.xml", "w") as f:
	# f.write(result)
print(result)
