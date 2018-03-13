
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND AND_ASSIGN AND_XOR AND_XOR_ASSIGN ASSIGN BREAK CASE COLON COMMA CONST CONTINUE DECR DEFAULT DIVIDE DIVIDE_ASSIGN DOT ELSE EQUALS FLOAT FOR FUNC GOTO GREATER HEX IDENTIFIER IF IMAGINARY IMPORT INCR INTEGER LCURL LESSER LESS_EQUALS LOGICAL_AND LOGICAL_OR LPAREN LSHIFT LSHIFT_ASSIGN LSQUARE MINUS MINUS_ASSIGN MOD MOD_ASSIGN MORE_EQUALS NOT NOT_ASSIGN OCTAL OR OR_ASSIGN PACKAGE PLUS PLUS_ASSIGN QUICK_ASSIGN RANGE RCURL RETURN RPAREN RSHIFT RSHIFT_ASSIGN RSQUARE RUNE SEMICOLON STAR STAR_ASSIGN STRING STRUCT SWITCH TYPE VAR XOR XOR_ASSIGNstart : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRepPackageClause : PACKAGE PackageNamePackageName : IDENTIFIERImportDeclRep : ImportDeclRep ImportDecl\n\t\t\t\t\t | epsilonImportDecl : IMPORT ImportSpec \n\t\t\t\t  | IMPORT LPAREN ImportSpecRep RPAREN ImportSpecRep : ImportSpecRep ImportSpec\n\t\t\t\t\t  | epsilon  ImportSpec : PackageNameDotOpt ImportPath  PackageNameDotOpt : DOT \n\t                      | PackageName ImportPath : STRING TopLevelDeclRep : TopLevelDeclRep TopLevelDecl \n\t\t\t\t\t   | epsilonTopLevelDecl : epsilonepsilon : '
    
_lr_action_items = {'RPAREN':([15,20,21,22,23,25,],[-17,-9,24,-10,-13,-8,]),'STRING':([6,17,18,19,],[-3,-12,23,-11,]),'SEMICOLON':([1,5,6,],[4,-2,-3,]),'PACKAGE':([0,],[2,]),'LPAREN':([12,],[15,]),'IMPORT':([4,7,8,11,16,22,23,24,],[-17,-5,12,-4,-6,-10,-13,-7,]),'IDENTIFIER':([2,12,15,20,21,22,23,25,],[6,6,-17,-9,6,-10,-13,-8,]),'DOT':([12,15,20,21,22,23,25,],[19,-17,-9,19,-10,-13,-8,]),'$end':([3,4,7,8,9,10,11,13,14,16,22,23,24,],[0,-17,-5,-17,-1,-15,-4,-16,-14,-6,-10,-13,-7,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'TopLevelDeclRep':([8,],[9,]),'PackageClause':([0,],[1,]),'TopLevelDecl':([9,],[14,]),'ImportSpec':([12,21,],[16,25,]),'epsilon':([4,8,9,15,],[7,10,13,20,]),'PackageName':([2,12,21,],[5,17,17,]),'ImportDecl':([8,],[11,]),'ImportPath':([18,],[22,]),'start':([0,],[3,]),'ImportSpecRep':([15,],[21,]),'PackageNameDotOpt':([12,21,],[18,18,]),'ImportDeclRep':([4,],[8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep','start',4,'p_start','parser.py',11),
  ('PackageClause -> PACKAGE PackageName','PackageClause',2,'p_package_clause','parser.py',16),
  ('PackageName -> IDENTIFIER','PackageName',1,'p_package_name','parser.py',20),
  ('ImportDeclRep -> ImportDeclRep ImportDecl','ImportDeclRep',2,'p_import_decl_rep','parser.py',26),
  ('ImportDeclRep -> epsilon','ImportDeclRep',1,'p_import_decl_rep','parser.py',27),
  ('ImportDecl -> IMPORT ImportSpec','ImportDecl',2,'p_import_decl','parser.py',34),
  ('ImportDecl -> IMPORT LPAREN ImportSpecRep RPAREN','ImportDecl',4,'p_import_decl','parser.py',35),
  ('ImportSpecRep -> ImportSpecRep ImportSpec','ImportSpecRep',2,'p_import_spec_rep','parser.py',42),
  ('ImportSpecRep -> epsilon','ImportSpecRep',1,'p_import_spec_rep','parser.py',43),
  ('ImportSpec -> PackageNameDotOpt ImportPath','ImportSpec',2,'p_import_spec','parser.py',50),
  ('PackageNameDotOpt -> DOT','PackageNameDotOpt',1,'p_package_name_dot_opt','parser.py',54),
  ('PackageNameDotOpt -> PackageName','PackageNameDotOpt',1,'p_package_name_dot_opt','parser.py',55),
  ('ImportPath -> STRING','ImportPath',1,'p_import_path','parser.py',62),
  ('TopLevelDeclRep -> TopLevelDeclRep TopLevelDecl','TopLevelDeclRep',2,'p_toplevel_decl_rep','parser.py',68),
  ('TopLevelDeclRep -> epsilon','TopLevelDeclRep',1,'p_toplevel_decl_rep','parser.py',69),
  ('TopLevelDecl -> epsilon','TopLevelDecl',1,'p_toplevel_decl','parser.py',76),
  ('epsilon -> <empty>','epsilon',0,'p_empty','parser.py',79),
]