# -*- coding: utf-8 -*-

"""
	This file uses ply(a python lib) to finish lab2
	Author: Qiu Zihao
	
	Python version: 3.5.2
	Lib version:	ply 3.10
"""

import sys
import ply.lex as lex
import ply.yacc as yacc

from semanticAnalysis import SemAnalysis

from trans2MIPS import Translate2MIPS

# global variable, if some error occurs, it will be set to 1
errorflag = 0

# new a SemAnalysis object
SemAnalysis = SemAnalysis()

# ------------------------------
# lexical analysis
# ------------------------------

# list of token names

# handle reserved words!! very important
reserved = {
	'if' : 'IF',
	'else' : 'ELSE',
	'while': 'WHILE',
	'return' : 'RETURN',
	'struct' : 'STRUCT',
	'int' : 'TYPE',
	'float' : 'TYPE',
}

non_reserved_tokens = (
	'INT', 'FLOAT', 'ID',
	'SEMI', 'COMMA', 'ASSIGNOP', 'RELOP',
	'PLUS', 'MINUS', 'STAR', 'DIV',
	'AND', 'OR', 'DOT', 'NOT',
	'LP', 'RP', 'LB', 'RB', 'LC', 'RC',
)

tokens = list(non_reserved_tokens) + list(set(reserved.values()))  # use set to remove duplications

# regular expression rules for tokens
t_SEMI = r';'
t_COMMA = r','
t_ASSIGNOP = r'='
t_RELOP = r'>=|<=|==|!=|>|<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_DIV = r'/'
t_AND = r'&&'
t_OR = r'\|\|'
t_DOT = r'\.'
t_NOT = r'!'
t_LP = '\('
t_RP = '\)'
t_LB = '\['
t_RB = '\]'
t_LC = '\{'
t_RC = '\}'
# a string containing ignored characters (spaces and tabs)
t_ignore = ' \t'  

# a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


# C-- comment (ignore)
def t_ccode_comment(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
	t.lexer.lineno += t.value.count('\n')
	pass


def t_ID(t):
	r'[A-Za-z_]([A-Za-z0-9_])*'
	t.type = reserved.get(t.value, 'ID')   # check for reserved words
	return t


def t_FLOAT(t):
	r'((([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+))[Ee][+-]?[0-9]*)|((([1-9][0-9]*)|0)\.[0-9]+)'
	num_str = t.value
	if 'e' in num_str and len(num_str.split('e')[1])==0:
		print('Error type A at Line %d: not a legal float number %s' %(t.lineno, t.value))
	elif 'E' in num_str and len(num_str.split('E')[1])==0:
		print('Error type A at Line %d: not a legal float number %s' %(t.lineno, t.value))
	else:
		t.value = float(t.value)
		return t


# must find oct number, dec number and hex number !!
def t_INT(t):
	r'(0[0-9A-WYZa-wz][0-9A-Za-z]*)|(0[Xx][0-9A-Za-z]+)|(([1-9][0-9]*)|0)'
	num_str = t.value
	if num_str == '0' or num_str[0] != '0':      # it's a dec number, return directly
		return t
	elif num_str[1] in ['x', 'X']:     # maybe it's a hex number
		hex_flag = True
		for i in range(len(num_str[2:])):
			if not num_str[2:][i] in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','A','B','C','D','E','F']:
				hex_flag = False
		if not hex_flag:
			print('Error type A at Line %d: not a legal hex number %s' %(t.lineno, t.value))
		else:
			t.value = str(int(num_str, 16))
			return t
	else:                                                # maybe it's a oct number
		oct_flag = True
		for i in range(len(num_str[1:])):
			if not num_str[1:][i] in ['0','1','2','3','4','5','6','7']:
				oct_flag = False
		if not oct_flag:
			print('Error type A at Line %d: not a legal oct number %s' %(t.lineno, t.value))
		else:
			t.value = str(int(num_str, 8))
			return t
	

# error handling rule
def t_error(t):
	print('Error type A at Line %d: Mysterious character "%s"' %(t.lineno, t.value[0]))
	global errorflag           # using global variable 'errorflag'
	errorflag = 1
	t.lexer.skip(1)


# ------------------------------
# syntax analysis
# ------------------------------

# this class is used to build a syntax analysis tree
class Node:
	def __init__(self, node_type, p, children=None, leaf=None):
		self.node_type = node_type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf
		self.lineno = p.lineno(0)

# output a syntax analysis tree
# pre-order traversal
# input: root node, init indent; output to stdout
def SynAnaTree(root, indent):
	# root -> left child -> right child
	if root == None:
		return
	print(' '*indent, end='')
	if type(root) == list and len(root) == 2 and root[0] in ['ID', 'TYPE', 'INT', 'FLOAT', 'RELOP']:
		print(root[0]+': '+str(root[1]))          # terminal symbols(ID,TYPE,INT,FLOAT)
		return
	elif type(root) == str and root in tokens:
		print(root)                          # any other terminal symbols
		return                   
	else:                                    # non-terminal symbols
		print(root.type+' ('+str(root.lineno)+')')   # in ply, lineno start from 0
		for i in range(len(root.children)):
			SynAnaTree(root.children[i], indent+2)

# grammer
# use tokens defined above!!
"""
	Program		: 	ExtDefList	 
	ExtDefList	:	ExtDef ExtDefList	 
	   			|	/*empty*/		 
	ExtDef		:	Specifier ExtDecList SEMI 	 
    	  		|	Specifier SEMI			 
				|	Specifier FunDec CompSt	 		 
	ExtDecList	:	VarDec		 
	   			|	VarDec COMMA ExtDecList	 

/*Specifiers*/
	Specifier		:	TYPE		 
					|	StructSpecifier		 
	StructSpecifier	:	STRUCT OptTag LC DefList RC  
					|	STRUCT Tag		 
	OptTag			:	ID	 
					|	/*empty*/ 
	Tag				:	ID	 

/*Declarators*/
	VarDec		:	ID	 
       			| 	VarDec LB INT RB	 
	FunDec		: 	ID LP VarList RP	 
				|	ID LP RP		 
				|	error RP		 
	VarList		:	ParamDec COMMA VarList	 
				|	ParamDec		 
	ParamDec	:	Specifier VarDec	 
		 
/*Statements*/	
	CompSt		:	LC DefList StmtList RC		 
	StmtList	:	Stmt StmtList		 
			 	|	/*empty*/		 		
	Stmt		:	Exp SEMI		 
    	 		|	CompSt			 
				|	RETURN Exp SEMI		 
				|	IF LP Exp RP Stmt
				|	IF LP Exp RP Stmt ELSE Stmt	 
				|	WHILE LP Exp RP Stmt	 

/*Local Definitions*/
	DefList	:	Def DefList		 
			|	/*empty*/ 
	Def		:	Specifier DecList SEMI	  
	DecList	:	Dec			 
			|	Dec COMMA DecList	 
	Dec		:	VarDec			 
    		|	VarDec ASSIGNOP Exp 

/*Expressions*/
	Exp		:	Exp ASSIGNOP Exp	 
    		|	Exp AND Exp		 
			| 	Exp OR Exp		 
			|	Exp RELOP Exp		 
			|	Exp PLUS Exp		 
			|	Exp MINUS Exp	 
			|	Exp STAR Exp		 
			|	Exp DIV Exp		 
			| 	LP Exp RP		 
			|	MINUS Exp	 
			|	NOT Exp			 
			|	ID LP Args RP	 
			|	ID LP RP		 
			|	Exp LB Exp RB		 
			|	Exp DOT ID		 
			|	ID		 
			|	INT			 
			|	FLOAT			  
	Args	:	Exp COMMA Args		 
     		|	Exp			 
"""
# precedence 

precedence = (
	('right', 'ASSIGNOP'),
	('left', 'OR'),
	('left', 'AND'),
	('left', 'RELOP'),
	('left', 'PLUS', 'MINUS'),
	('left', 'STAR', 'DIV'),
	('right', 'NOT'),
	('left', 'DOT', 'LB', 'RB', 'LP', 'RP'),
	('nonassoc', 'if_then'),
	('nonassoc', 'ELSE'),
	('nonassoc', 'STRUCT', 'RETURN', 'WHILE'),
)


# program is the initial grammer unit
def p_program(p):
	'Program : ExtDefList'
	p[0] = Node('Program', p, [p[1]], p[0])

# each program can produce some ExtDefList
# ExtDefList represents several ExtDef
def p_extdeflist(p):
	'''ExtDefList	: ExtDef ExtDefList
	           		| empty'''
	if len(p) != 2:
		p[0] = Node('ExtDefList', p, [p[1], p[2]], p[0])
	else:
		pass

# ExtDef represents a global variable, a structure or a function
def p_extdef_1(p):                                                # structure
	'ExtDef	:	Specifier SEMI'
	p[0] = Node('ExtDef', p, [p[1], 'SEMI'], p[0])

	struct_info = SemAnalysis.procSpecifier(p[1])

	# check if there have duplicated struct names
	for item in SemAnalysis.getSymbolTable():
		if item[0] == 'global struct' and item[1][0] == struct_info[0]:
			print('Error type 16 at Line %d: Duplicated name \"%s\"' %(p[1].lineno, struct_info[0].split(' ')[1]))
		if item[0] == 'global struct': # nested struct can also cause duplicated name !!
			for var_definiton in item[1][1]:
				if type(var_definiton[0]) == tuple and var_definiton[0][0] == struct_info[0]:
					print('Error type 16 at Line %d: Duplicated name \"%s\"' %(p[1].lineno, struct_info[0].split(' ')[1]))
	
	SemAnalysis.addInSymbolTable(['global struct', struct_info])


def p_extdef_2(p):                                                # function
	'ExtDef :	Specifier FunDec CompSt'
	p[0] = Node('ExtDef', p, [p[1], p[2], p[3]], p[0])
	
	fundec = SemAnalysis.procFunDec(p[2]) # [func_name, var_list]
	func_name = fundec[0]
	func_var_list = fundec[1]

	return_type = SemAnalysis.procSpecifier(p[1], 'func')
		
	# check if there has redefined function
	if func_name in SemAnalysis.getFuncName():
		print('Error type 4 at Line %d: Redefined function \"%s\"' %(p[1].lineno, func_name))

	compst = SemAnalysis.procCompSt(p[3], func_var_list, func_name, return_type)

	SemAnalysis.addInSymbolTable(['func', return_type, SemAnalysis.procFunDec(p[2]), compst])


# this function is used to deal wtih declaration of a function
# do nothing but add this declaration into SymbolTable
def p_extdef_funcDec(p):
	'ExtDef : Specifier FunDec SEMI'
	specifier = SemAnalysis.procSpecifier(p[1])
	funcdec = SemAnalysis.procFunDec(p[2])

	if SemAnalysis.checkFuncRedec(specifier, funcdec):
		print('Error type 19 at Line %d: Inconsistent declaration of function \"%s\"' %(p[1].lineno, funcdec[0]))
	else:
		SemAnalysis.addInSymbolTable(['func-dec', specifier, funcdec, p[1].lineno])


def p_extdef_3(p):                                                # global variable, it may also has a definition of a structure
	'ExtDef	:	Specifier ExtDecList SEMI'
	p[0] = Node('ExtDef', p, [p[1], p[2], 'SEMI'], p[0])

	Specifier = SemAnalysis.procSpecifier(p[1])
	extdeclist = SemAnalysis.procExtDecList(p[2], [])

	structType = None   # use this variable to allow add one struct type in a declist

	for item in extdeclist:
		specifier = Specifier
		if '[' in item:         # it's an array, need to reshape it
			item = item.replace(']', '').split('[')

			if type(specifier) == str:      # basic type
				for dim in item[1:]:
					specifier += '-' + dim
				item = item[0]
				SemAnalysis.addInSymbolTable(['global variable', specifier, item])

			elif 'struct' in specifier[0]:  # struct type
				if specifier[0] != 'struct UNknownType' and structType == None:   # it's a definition of a struct as well
					SemAnalysis.addInSymbolTable(['global struct', specifier])
					structType = specifier[0]	
				
				var_list = specifier[1]
				specifier = specifier[0]
				
				for dim in item[1:]:
					specifier += '-' + dim
				item = item[0]
				SemAnalysis.addInSymbolTable(['global variable', (specifier, var_list), item])

		else:                   # add it to SymbolTable directly
			if type(specifier) == tuple and specifier[0] != 'struct UNknownType': # it also has a definition of a structure
				SemAnalysis.addInSymbolTable(['global struct', specifier])	

			SemAnalysis.addInSymbolTable(['global variable', specifier, item])


# ExtDecList represents some definitions to variable
def p_extdeclist_1(p):
	'ExtDecList : VarDec'
	p[0] = Node('ExtDecList', p, [p[1]], p[0])

def p_extdeclist_2(p):
	'''ExtDecList : VarDec COMMA ExtDecList	 '''
	p[0] = Node('ExtDecList', p, [p[1], 'COMMA', p[3]], p[0])


# specifier represents type desciption
def p_specifier_TYPE(p):
	'Specifier : TYPE'
	p[0] = Node('Sepcifier', p, [['TYPE', p[1]]], p[0])


def p_specifier_structspecifier(p):
	'Specifier : StructSpecifier'
	p[0] = Node('Sepcifier', p, [p[1]], p[0])


# desciption of structure
def p_structspecifier_1(p):
	'StructSpecifier : STRUCT OptTag LC DefList RC' 
	p[0] = Node('StructSpecifier', p, ['STRUCT', p[2], 'LC', p[4], 'RC'], p[0])

def p_structspecifier_2(p):
	'StructSpecifier : STRUCT Tag' 
	p[0] = Node('StructSpecifier', p, ['STRUCT', p[2]], p[0])


# OptTag represents struct name
def p_opttag_ID(p):
	'OptTag : ID'
	p[0] = Node('OptTag', p, [['ID', p[1]]], p[0])

def p_opttag_empty(p):
	'OptTag : empty'
	pass

# Tag represents variable name
def p_tag(p):
	'Tag :	ID'
	p[0] = Node('Tag', p, [['ID', p[1]]], p[0])


# VarDec represents definition to a variable
def p_vardec_ID(p):
	'VarDec : ID'
	p[0] = Node('VarDec', p, [['ID', p[1]]], p[0])


def p_vardec_vardeclbintrb(p):
	'VarDec : VarDec LB INT RB'
	p[0] = Node('VarDec', p, [p[1], 'LB', ['INT', p[3]], 'RB'], p[0])


# FunDec represents definition to a function head
def p_fundec_1(p):
	'FunDec : ID LP VarList RP' 
	p[0] = Node('FunDec', p, [['ID', p[1]], 'LP', p[3], 'RP'], p[0]) 

def p_fundec_2(p):
	'FunDec : ID LP RP' 
	p[0] = Node('FunDec', p, [['ID', p[1]], 'LP', 'RP'], p[0])


# VarList contains several ParamDec
def p_varlist_1(p):
	'VarList : ParamDec COMMA VarList' 
	p[0] = Node('VarList', p, [p[1], 'COMMA', p[3]], p[0]) 

def p_varlist_2(p):
	'VarList : ParamDec'
	p[0] = Node('VarList', p, [p[1]], p[0])


# ParamDec represents a definition to formal parameter
def p_paramdec(p):
	'ParamDec	:	Specifier VarDec'
	p[0] = Node('ParamDec', p, [p[1], p[2]], p[0])


# CompSt represents { statement block }
def p_compst(p):
	'CompSt	: LC DefList StmtList RC'
	p[0] = Node('CompSt', p, ['LC', p[2], p[3], 'RC'], p[0])


# StmtList represents several statements(Stmt)
def p_stmtlist(p):
	'''StmtList	: Stmt StmtList
	            | empty'''
	if len(p) != 2:
		p[0] = Node('StmtList', p, [p[1], p[2]], p[0])
	else:
		pass


# Stmt represents a statement
def p_stmt_1(p):
	'Stmt :	Exp SEMI' 
	p[0] = Node('Stmt', p, [p[1], 'SEMI'], p[0])

def p_stmt_2(p):
	'Stmt : CompSt' 
	p[0] = Node('Stmt', p, [p[1]], p[0])

def p_stmt_3(p):
	'Stmt : IF LP Exp RP Stmt %prec if_then'
	p[0] = Node('Stmt', p, ['IF', 'LP', p[3], 'RP', p[5]], p[0])

def p_stmt_4(p):
	'Stmt : WHILE LP Exp RP Stmt'
	p[0] = Node('Stmt', p, ['WHILE', 'LP', p[3], 'RP', p[5]], p[0])

def p_stmt_5(p):
	'Stmt : IF LP Exp RP Stmt ELSE Stmt'
	p[0] = Node('Stmt', p, ['IF', 'LP', p[3], 'RP', p[5], 'ELSE', p[7]], p[0])

def p_stmt_6(p):
	'Stmt : RETURN Exp SEMI'
	p[0] = Node('Stmt', p, ['RETURN', p[2], 'SEMI'], p[0])


# DefList represents a string of definitions to variables 
def p_deflist(p):
	'''DefList	: Def DefList 
	            | empty'''
	if len(p) != 2:
		p[0] = Node('DefList', p, [p[1], p[2]], p[0])
	else:
		pass


# Def represents a definition to a variable
def p_def(p):
	'Def : Specifier DecList SEMI'
	p[0] = Node('Def', p, [p[1], p[2], 'SEMI'], p[0])
	
	""" semantic analysis: find every symbol and put it into SymbolTable """
	""" Local Definitions !!!! """
	SemAnalysis.procDef(p[0], 'local')


# member in DecList
def p_declist_1(p):
	'DecList	:	Dec'
	p[0] = Node('DecList', p, [p[1]], p[0]) 

def p_declist_2(p):
	'DecList	: Dec COMMA DecList'
	p[0] = Node('DecList', p, [p[1], 'COMMA', p[3]], p[0])


def p_dec_1(p):
	'Dec	:	VarDec' 
	p[0] = Node('Dec', p, [p[1]], p[0])

def p_dec_2(p):
	'Dec	: VarDec ASSIGNOP Exp '
	p[0] = Node('Dec', p, [p[1], 'ASSIGNOP', p[3]], p[0])


# expressions
def p_exp_ASSIGNOP(p):
	'Exp : Exp ASSIGNOP Exp'
	p[0] = Node('Exp', p, [p[1], 'ASSIGNOP', p[3]], p[0])

def p_exp_AND(p):
	'Exp : Exp AND Exp'
	p[0] = Node('Exp', p, [p[1], 'AND', p[3]], p[0])

def p_exp_OR(p):
	'Exp : Exp OR Exp'
	p[0] = Node('Exp', p, [p[1], 'OR', p[3]], p[0])

def p_exp_RELOP(p):
	'Exp : Exp RELOP Exp'
	p[0] = Node('Exp', p, [p[1], ['RELOP', p[2]], p[3]], p[0])

def p_exp_PLUS(p):
	'Exp : Exp PLUS Exp'
	p[0] = Node('Exp', p, [p[1], 'PLUS', p[3]], p[0])

def p_exp_MINUS(p):
	'Exp : Exp MINUS Exp'
	p[0] = Node('Exp', p, [p[1], 'MINUS', p[3]], p[0])

def p_exp_STAR(p):
	'Exp : Exp STAR Exp'
	p[0] = Node('Exp', p, [p[1], 'STAR', p[3]], p[0])

def p_exp_DIV(p):
	'Exp : Exp DIV Exp'
	p[0] = Node('Exp', p, [p[1], 'DIV', p[3]], p[0])

def p_exp_LPRP(p):
	'Exp : LP Exp RP'
	p[0] = Node('Exp', p, ['LP', p[2], 'RP'], p[0])

def p_exp_MINUS_2(p):
	'Exp : MINUS Exp'
	p[0] = Node('Exp', p, ['MINUS', p[2]], p[0])

def p_exp_NOT(p):
	'Exp : NOT Exp'
	p[0] = Node('Exp', p, ['NOT', p[2]], p[0])

def p_exp_IDLPRP(p):
	'Exp : ID LP Args RP'
	p[0] = Node('Exp', p, [['ID', p[1]], 'LP', p[3], 'RP'], p[0])

def p_exp_IDLPRP2(p):
	'Exp : ID LP RP'
	p[0] = Node('Exp', p, [['ID', p[1]], 'LP', 'RP'], p[0])

def p_exp_LBRB(p):
	'Exp : Exp LB Exp RB'
	p[0] = Node('Exp', p, [p[1], 'LB', p[3], 'RB'], p[0]) 

def p_exp_DOTID(p):
	'Exp : Exp DOT ID'
	p[0] = Node('Exp', p, [p[1], 'DOT', ['ID', p[3]]], p[0])

def p_exp_ID(p):
	'Exp : ID'
	p[0] = Node('Exp', p, [['ID', p[1]]], p[0])

def p_exp_INT(p):
	'Exp : INT'
	p[0] = Node('Exp', p, [['INT', p[1]]], p[0])

def p_exp_FLOAT(p):
	'Exp : FLOAT'
	p[0] = Node('Exp', p, [['FLOAT', p[1]]], p[0])
	

# Args represents parameters list		  
def p_args_1(p):
	'Args : Exp COMMA Args'
	p[0] = Node('Args', p, [p[1], 'COMMA', p[3]], p[0])

def p_args_2(p):
	'Args : Exp' 
	p[0] = Node('Args', p, [p[1]], p[0]) 


# handle with empty
def p_empty(p):
	'empty :'
	pass


"""
	error rule for syntax error 
"""
# error will be process by this function first
def p_error(p):
	global errorflag
	errorflag = 1
	pass


# print error info
def error_msg(lineno ,msg, nearby_str=None):
	if nearby_str==None:
		print('Error type B at Line %d: Syntax Error, %s' %(lineno, msg))
	else:
		print('Error type B at Line %d: Syntax Error, %s, near \'%s\'' %(lineno, msg, nearby_str))

def p_extdef_error(p):
	'ExtDef : error SEMI'
	error_msg(p.lineno(0), 'Wrong ExtDef', p[1].value)

def p_fundec_error(p):
	'FunDec : error RP'
	error_msg(p.lineno(0), 'Wrong FunDec', p[1].value)

def p_compst_error(p):
	'CompSt : error RC'
	error_msg(p.lineno(0), 'Wrong CompSt', p[1].value)

def p_stmt_error(p):
	'Stmt : error SEMI'
	error_msg(p.lineno(0), 'Wrong Stmt', p[1].value)

def p_def_error(p):
	'Def : Specifier error SEMI'
	error_msg(p.lineno(0), 'Wrong Def', p[2].value)


"""
	start here
	first is the lexical analysis
"""
# read file from command line
if len(sys.argv) > 2:
	print('Wrong! Only accept ONE file!')

if len(sys.argv) == 1:
	print('Wrong! No input file!')

# try to read file into text
filename = sys.argv[1]
try:
	infile = open(filename, 'r')
except IOError:
	print('The file does not exist.')
text = infile.read()


# build the lexer
lexer = lex.lex()


"""
	output the result of lexical analysis
	IF you use lexer together with parser, line number will get wrong!!!
"""

"""
# feed the input into the lexer
lexer.input(text)

# tokenize
while True:
	tok = lexer.token()
	if not tok:
		break      # no more input
	print(tok)
"""

"""
	start syntax analysis
"""

# build the parser
parser = yacc.yacc()

LCRC = 0
line_num = 1
for s in text:
	if s=='\n':
		line_num += 1
	elif s=='{':
		LCRC += 1
	elif s=='}':
		LCRC -= 1
	if LCRC < 0:
		error_msg(line_num, 'lack \'{\'')
if LCRC > 0:
	error_msg(line_num, 'lack \'}\'')

# result is a Node object and represents a syntax analysis tree
# start tracking to record line numbers
result = parser.parse(text, tracking=True)   # root of parsing tree
"""
if errorflag == 0:    # there is no lexical error
	# output a syntax analysis tree
	SynAnaTree(result, 0)        
"""

SemAnalysis.checkUndefFunc()


"""
	do translation here
"""
# build translation model
translation = Translate2MIPS(SemAnalysis.getSymbolTable(), result, SemAnalysis, tokens)

translation()

