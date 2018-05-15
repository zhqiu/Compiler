"""
	this file defines some functions used in semantic analysis
"""

class SemAnalysis(object):
	
	def __init__(self):
		# use the following SymbolTable to do semantic analysis
		# type of SymbolTable is list !!
		# use two global variables to store type and symbol which are under processing
		self.SymbolTable = []
		self.wrongVarInStruct = []       # var in struct with assignment

		# add two functions
		# int read(); & int write(int)
		self.SymbolTable.append(['func', 'int', ['read', []], []])
		self.SymbolTable.append(['func', 'int', ['write', [['int', 'tmp']]], []])

	
	# add new item into self.SymbolTable
	def addInSymbolTable(self, item):
		self.SymbolTable.append(item)


	# return self.SymbolTable
	def getSymbolTable(self):
		return self.SymbolTable


	# check if this function has been redecalared
	# return True if this function has been redecalared(has the same func_name but different specifier or args_list)
	def checkFuncRedec(self, specifier, funcdec):
		redec = False
		func_name = funcdec[0]

		for item in self.SymbolTable:
			if item[0] == 'func-dec' and item[2][0] == func_name:
				if specifier != item[1] or funcdec[1] != item[2][1]:
					redec = True

		return redec


	# process Def in one structure or function
	# Def here are all in structure or function, so NOT in SymbolTable !!!!
	def procDef(self, definition, def_type):
		# Def : Specifier DecList SEMI
		specifier = self.procSpecifier(definition.children[0])

		# because DecList is recursively defined, so I use a function to cope with it
		declist = self.procDecList(definition.children[1], [], specifier)

		defin = self.procArrayType(specifier, declist)

		return defin


	# process array type, eg: ['int', 'a[10]'] => ['int-10', 'a']
	# return new def list, eg: [['int', 'a'], ['int-10', 'b']]
	def procArrayType(self, specifier, declist):
		defin = []
		for item in declist:
			if '[' in item:    # array item
				item_part = (item.replace(']', '')).split('[')
				var_name = item_part[0]  # type: str
				dim = item_part[1:]      # type: list

				new_type_name = specifier
				for dim_num in dim:
					new_type_name += '-' + dim_num

				defin.append([new_type_name, var_name])

			else:
				defin.append([specifier, item])

		return defin


	# return a list, result of procDefList(defList)
	# and do semantic analysis !
	def procCompSt(self, compst, func_var_list, func_name, return_type):
		# CompSt : LC DefList StmtList RC
		if compst == None:
			return []	

		defList = compst.children[1]
		stmtList = compst.children[2]
	
		# add symbols defined in function head to symboltable
		symboltable = []
		for func_var in func_var_list:
			symboltable.append(func_var)

		symboltable += self.procDefList(defList, [], 1)  # symboltable of this function

		self.checkDefAssign(symboltable, func_name, return_type)
	
		self.procStmtList(stmtList, symboltable, func_name, return_type)     # use global SymbolTable and func_name to check each statement

		return symboltable


	# check assignment in definition
	def checkDefAssign(self, symboltable, func_name, return_type):
		for item in symboltable:
			if type(item[1]) == list:            # definition with assignment
				var_tp, exp = item[0], item[1][1]
				exp_tp = self.procExp(exp, symboltable, func_name, return_type)
				if exp_tp in ['INT', 'FLOAT']:
					exp_tp = exp_tp.lower()
				if var_tp != exp_tp:
					print('Error type x at Line %d: Assignment mismatch in definition.' %(exp.lineno))

	
	def procStmtList(self, stmtList, symboltable, func_name, return_type):
		# StmtList : Stmt StmtList
		#		   | empty
		if stmtList == None:
			return

		elif len(stmtList.children) == 2:              # StmtList : Stmt StmtList
			self.procStmt(stmtList.children[0], symboltable, func_name, return_type)
			self.procStmtList(stmtList.children[1], symboltable, func_name, return_type)
	
		else:
			print('Something got wrong with StmtList')


	# symboltable contains symbols defined in this function
	def procStmt(self, stmt, symboltable, func_name, return_type):
		# Stmt : Exp SEMI
		# 	   | CompSt
		# 	   | RETURN Exp SEMI
		#      | IF LP Exp RP Stmt
		# 	   | IF LP Exp RP Stmt ELSE Stmt
		# 	   | WHILE LP Exp RP Stmt

		if stmt == None:
			return	

		if len(stmt.children) == 1:    # Stmt : CompSt
			 # TODO stmt in this block can only access variables defined in this block
			self.procCompSt(stmt.children[0], symboltable, func_name, return_type)              

		elif len(stmt.children) == 2:  # Stmt : Exp SEMI
			self.procExp(stmt.children[0], symboltable, func_name, return_type)

		elif len(stmt.children) == 3:  # Stmt : RETURN Exp SEMI
			# check the function's return type
			exp_tp = self.procExp(stmt.children[1], symboltable, func_name, return_type)

			if exp_tp == None:  # it's a wrong Exp here, just return
				return

			if exp_tp in ['INT', 'FLOAT']:
				exp_tp = exp_tp.lower()

			if return_type != exp_tp:
				print('Error type 8 at Line %d: Type mismatched for return.' %(stmt.lineno))

		elif stmt.children[0] == 'IF' and len(stmt.children) == 5: # IF LP Exp RP Stmt
			self.procExp(stmt.children[2], symboltable, func_name, return_type)
			self.procStmt(stmt.children[4], symboltable, func_name, return_type)

		elif stmt.children[0] == 'IF' and len(stmt.children) == 7: # IF LP Exp RP Stmt ELSE Stmt
			self.procExp(stmt.children[2], symboltable, func_name, return_type)
			self.procStmt(stmt.children[4], symboltable, func_name, return_type)
			self.procStmt(stmt.children[6], symboltable, func_name, return_type)

		elif stmt.children[0] == 'WHILE':
			self.procExp(stmt.children[2], symboltable, func_name, return_type)
			self.procStmt(stmt.children[4], symboltable, func_name, return_type)
		

	# return type of exp, INT/FLOAT/int/float
	# symboltable contains symbols defined in this function
	def procExp(self, exp, symboltable, func_name, return_type):
		# Exp :	Exp ASSIGNOP Exp	 
		#	  |	Exp AND Exp		 
		#	  | Exp OR Exp		 
		#	  |	Exp RELOP Exp		 
		#	  |	Exp PLUS Exp		 
		#	  |	Exp MINUS Exp	 
		#	  |	Exp STAR Exp		 
		#	  |	Exp DIV Exp		 
		#	  | LP Exp RP		 
		#	  |	MINUS Exp	 
		#	  |	NOT Exp			 
		#	  |	ID LP Args RP	 
		#	  |	ID LP RP		 
		#	  |	Exp LB Exp RB		 
		#	  |	Exp DOT ID		 
		#	  |	ID		 
		#	  |	INT			 
		#     |	FLOAT

		# base case, need to return type INT, FLOAT of type of ID !!!
		if len(exp.children) == 1:  
			t, v = exp.children[0][0], exp.children[0][1]  # t:'ID'/'INT'/'FLOAT' v:name or number
		
			exp_tp = t
			v_not_define = True

			for item in symboltable:
				if type(item[1]) == str:     # no assignment
					st_t, st_v = item[0], item[1] # st_t is type(str), st_v is variable(list)
					if v == st_v:
						v_not_define = False
				elif type(item[1]) == list:  # definition which has assignment
					st_t, st_v, assign_exp = item[0], item[1][0], item[1][1]
					if v == st_v:
						v_not_define = False

			# v can also be a global variable !!
			for item in self.getSymbolTable():
				if item[0] == 'global variable' and v == item[-1]:
					v_not_define = False
					return item[1]   # type of this global variable
				
			if t == 'ID' and v_not_define:
				print('Error type 1 at Line %d: Undefined variable \"%s\"' %(exp.lineno, v))
				return None

			elif t == 'ID' and not v_not_define:         # need to look up symboltable to find out type of this exp
				for item in symboltable:
					if type(item[1]) == str and item[1] == v:
						exp_tp = item[0]
					elif type(item[1]) == list and item[1][0] == v:
						exp_tp = item[0]
		
			return exp_tp

		elif len(exp.children) == 2:                                  # MINUS Exp / NOT Exp
			exp_tp = self.procExp(exp.children[1], symboltable, func_name, return_type)

			if exp_tp == None:           # variable not defined
				return None

			if exp.children[0] == 'MINUS':
				if not exp_tp in ['int', 'float', 'INT', 'FLOAT']:
					print('Error type x at Line %d: Only Type int value or float value can do arithmetic operation.' %(exp.lineno))
					return None

			elif exp.children[0] == 'NOT':
				if not exp_tp in ['int', 'INT']:
					print('Error type x at Line %d: Only Type int can do logical operation.' %(exp.lineno))

			return exp_tp

		elif len(exp.children) == 3:
			if exp.children[1] == 'DOT':                               #	  |	Exp DOT ID
				# check if Exp is a struct variable and if ID is a variable defined in struct Exp
				# exp.children[0].children[0] can be a Node(eg: v.a.name) or a list(eg: v.name)

				# second check if ID is a variable defined in struct Exp
				id_name = exp.children[2][1]

				if type(exp.children[0].children[0]) != list:  # it's a Node, should be processed as a Exp !!
					exp_type = self.procExp(exp.children[0], symboltable, func_name, return_type)

					for item in self.getSymbolTable():
						if item[0] == 'global struct' and item[1][0] == exp_type:
							for val_definition in item[1][1]:
								if val_definition[1] == id_name:
									return val_definition[0]

					if exp_type in ['int', 'float', 'INT', 'FLOAT']:
						print('Error type 13 at Line %d: Illegal use of \".\"' %(exp.lineno))
						return None
					elif type(exp_type) == tuple and 'struct' in exp_type[0]:  
						# it's a global struct variable without type name                     
  						# should return type of Exp.ID !!!
						has_field = False
						for item in exp_type[1]:
							if item[1] == id_name:
								return item[0]
								has_field = True
						if not has_field:
							print('Error type 14 at Line %d: Non-existent field \"%s\"' %(exp.lineno, id_name))
					else:
						print('Error type 14 at Line %d: Non-existent field \"%s\"' %(exp.lineno, id_name))

				elif type(exp.children[0].children[0]) == list:
			
					exp_name = exp.children[0].children[0][1]
					exp_type = None   # 'struct xxxx'

					if_defined = self.checkIfDefined(exp_name, symboltable)     # check if defined in this function
					if_structVar, exp_type = self.checkIfStructVar(exp_name)    # check if it's a global struct variable

					# first check if Exp is a struct variable
					if if_defined == 0 and if_structVar == 0:
						print('Error type 1 at Line %d: Undefined variable \"%s\"' %(exp.lineno, exp_name))
						return None

					elif if_defined == 1 and if_structVar == 0:
						exp_type = self.procExp(exp.children[0], symboltable, func_name, return_type)

						if type(exp_type) == tuple and 'struct' in exp_type[0]:  # a struct defined in a function
							for item in exp_type[1]:
								if type(item[1]) == list and item[1][0] == id_name:    # it's an assignment !! WRONG !
									return item[0]

							# can not find this field !
							print('Error type 14 at Line %d: Non-existent field \"%s\"' %(exp.lineno, id_name))	
							
						if not 'struct' in exp_type:
							print('Error type 13 at Line %d: Illegal use of \".\".'%(exp.lineno))
							return None
			
					has_area = False
					ele_type = None

					 # a struct variable can be defined in one function or can be a global struct variable
					var_type = 'global struct' if if_structVar == 0 else 'global variable'

					for item in self.SymbolTable:
						if item[0] == var_type and item[1][0] == exp_type:
							var_list = item[1][1]
							for var in var_list:
								if type(var[1]) == str and var[1] == id_name:
									has_area = True
									ele_type = var[0]
								elif type(var[1]) == list and var[1][0] == id_name:  # it a field with assignment !!
									has_area = True
									ele_type = var[0]
		
					if not has_area:
						print('Error type 14 at Line %d: Non-existent field \"%s\".' %(exp.lineno, id_name))
						return None
					elif has_area:
						return ele_type            # type of this Exp
			
			elif exp.children[1] == 'LP' and exp.children[2] == 'RP':  #	  |	ID LP RP
				function_name = exp.children[0][1]
			
				func_not_define = True
				args_wrong = True
				match_func_name = None
				return_tp = None

				for item in self.SymbolTable:
					if item[0] == 'func':  # item for function
						func_name = item[2][0]
						param_list = item[2][1]
					
						if func_name == function_name:
							func_not_define = False
							match_func_name = func_name
							return_tp = item[1]

						if len(param_list) == 0:
							args_wrong = False

				if_defined = self.checkIfDefined(function_name, symboltable)

				if if_defined == 1:
					print('Error type 11 at Line %d: \"%s\" is not a function.' %(exp.lineno, function_name))				

				elif if_defined == 0 and func_not_define and func_name != function_name:
					print('Error type 2 at Line %d: Undefined function \"%s\"' %(exp.lineno, function_name))		

				if (args_wrong and match_func_name != None) or(func_name == function_name and len(symboltable) != 0):
					print('Error type 9 at Line %d: Function %s want param_list, while given no parameters' %(exp.lineno, match_func_name))

				if func_name == function_name:
					return return_type
				else:
					return return_tp

			elif exp.children[0] == 'LP' and exp.children[2] == 'RP':  #	  | LP Exp RP
				return self.procExp(exp.children[1], symboltable, func_name, return_type)

			else:
				exp1, exp2 = exp.children[0], exp.children[2] # type: Node

				exp1_tp = self.procExp(exp1, symboltable, func_name, return_type)         # check two components
				exp2_tp = self.procExp(exp2, symboltable, func_name, return_type)

				if exp1_tp == None or exp2_tp == None:        # variable not defined
					return None

				if exp.children[1] == 'ASSIGNOP':			  # check assignment mismatch !!

					if 'LP' in exp1.children and 'RP' in exp1.children:   # it's a function
						print('Error type 6 at Line %d: The left-hand side of an assignment must be a variable.' %(exp.lineno))

					if exp1_tp in ['int', 'float'] and exp2_tp in ['INT', 'FLOAT', 'int', 'float']:   # both sides are basic type
						if exp1_tp != exp2_tp.lower():
							print('Error type 5 at Line %d: Type mismatched for assignment.' %(exp.lineno))

					# only one side is basic type
					elif ('struct' in exp1_tp and not 'struct' in exp2_tp) or ('struct' in exp2_tp and not 'struct' in exp1_tp):
						print('Error type 5 at Line %d: Type mismatched for assignment.' %(exp.lineno))

					# both sides are struct type, struct should be defined, or it will cause error in def
					elif 'struct' in exp1_tp and 'struct' in exp2_tp:
						s1_tp = self.getStructType(exp1_tp)	
						s2_tp = self.getStructType(exp2_tp)
					
						if s1_tp != s2_tp:
							print('Error type 5 at Line %d: Type mismatched for assignment.' %(exp.lineno))

					elif not exp1_tp in ['int', 'float']: 
						print('Error type 6 at Line %d: The left-hand side of an assignment must be a variable.' %(exp.lineno))
			
				if exp.children[1] in ['PLUS', 'MINUS', 'STAR', 'DIV']:

					if exp1_tp in ['int', 'float', 'INT', 'FLOAT'] and exp2_tp in ['int', 'float', 'INT', 'FLOAT']:
						if exp1_tp.lower() != exp2_tp.lower():
							print('Error type 7 at Line %d: Type mismatched for operands.' %(exp.lineno))
						else:
							return exp1_tp.lower()
					else:
						print('Error type 7 at Line %d: Operands type mismatched.' %(exp.lineno))

					return None

				if exp.children[1] in ['AND', 'OR'] or (type(exp.children[1]) == list and exp.children[1][0] == 'RELOP'):
					if not exp1_tp in ['int', 'INT'] or not exp2_tp in ['int', 'INT']:
						print('Error type x at Line %d: Only Type int can do logical operation.' %(exp.lineno))

		elif len(exp.children) == 4:
			if exp.children[1] == 'LP' and exp.children[3] == 'RP':   # Exp : ID LP Args RP

				function_name = exp.children[0][1]
				args_list = []
				for s in self.procArgs(exp.children[2], [], symboltable, func_name, return_type):
					if s in ['INT', 'FLOAT']:
						args_list.append(s.lower())
					elif type(s) == tuple and 'struct' in s[0]:   # it's a global struct variable
						args_list.append(s[0])
					else:
						args_list.append(s)

				if_defined = self.checkIfDefined(function_name, symboltable)

				if if_defined == 1:   # it's a variable defined in this function
					print('Error type 11 at Line %d: \"%s\" is not a function.' %(exp.lineno, function_name))				
					return None				
								
				elif if_defined == 0:
					# try to get param_list and return_type of this 'function'
					return_tp, func_var_list = self.getFuncArgsList(function_name) 

					if func_var_list == None and func_name != function_name:
						print('Error type 2 at Line %d: Undefined function \"%s\"' %(exp.lineno, function_name))
						return None

					if func_name == function_name:   # it's a recursive function
						func_var_list = []
						for item in symboltable:
							func_var_list.append(item[0])

					if args_list != func_var_list:
						s1, s2 = '', ''
						for s in func_var_list:
							if s != None:
								s1 += s + ','
							else:
								s1 += 'NotDefinedVar' + ',' 
						for s in args_list:
							if s != None:
								s2 += s + ','
							else:
								s2 += 'NotDefinedVar' + ',' 

						print('Error type 9 at Line %d: Function \"func_name(%s)\" is not applicable for arguments \"(%s)\"'%(exp.lineno, s1, s2))

				if func_name == function_name:    # it's a recursive function
					return return_type 
				else:
					return return_tp

			elif exp.children[1] == 'LB' and exp.children[3] == 'RB':   # Exp : Exp LB Exp RB, check this array

				exp1, exp2 = exp.children[0], exp.children[2]

				# first check if type of exp2 is int !!
				# type of exp2 must be INT ! check this !!
				exp2_tp = self.procExp(exp2, symboltable, func_name, return_type)

				if not exp2_tp in ['INT', 'int']:
					print('Error type 12 at Line %d: \"%s\" is not an integer.' %(exp.lineno, exp2.children[0][1]))

				if type(exp1.children[0]) == list:  # it's a ID ! need to check if the variable has been defined
					exp1_id = exp1.children[0][1]

					if_defined = self.checkIfDefined(exp1_id, symboltable)
					if_array = self.checkIfArrayVariable(exp1_id, symboltable)

					# check if exp1_id is a global array
					for item in self.getSymbolTable():
						if item[0] == 'global variable' and item[-1] == exp1_id:
							return item[1]  # type of the exp

					if if_defined == 0:
						print('Error type 1 at Line %d: Undefined variable \"%s\"' %(exp.lineno, exp1_id))
					elif if_array == 0:
						print('Error type 10 at Line %d: \"%s\" is not an array.' %(exp.lineno, exp1_id))

					if if_defined == 1 and if_array == 1:   # should return type of 'ID LB Exp RB'
						for item in symboltable:
							if item[1] == exp1_id:
								exp1_tp = item[0]
								exp1_tp = exp1_tp[::-1]
								exp1_tp = exp1_tp[exp1_tp.index('-')+1:]
								exp1_tp = exp1_tp[::-1]
								return exp1_tp

				else:                               # exp1.children[0] is still a Exp
					exp1_tp = self.procExp(exp1, symboltable, func_name, return_type)
					
					if exp1_tp == None:  # Exp1 is not a legal expression !!
						return None
					
					if not '-' in exp1_tp:      # it's just a basic type, illegal use of '[]'
						print('Error type 10 at Line %d: Illegal use of \"[]\".' %(exp.lineno))		
						return None	

					exp1_tp = exp1_tp[::-1]
					exp1_tp = exp1_tp[exp1_tp.index('-')+1:]
					exp1_tp = exp1_tp[::-1]

					return exp1_tp

	
	# check if a variable is a global struct variable
	# return (True/false, exp_type), exp_type: 'struct xxxx'
	def checkIfStructVar(self, exp_name):
		if_structVar = False
		exp_type = None

		for item in self.SymbolTable:
			if item[0] == 'global variable' and 'struct' in item[1][0]:
				if item[2] == exp_name:
					if_structVar = True
					exp_type = item[1][0]

		return if_structVar, exp_type


	# get struct type: type of members defined in the struct
	def getStructType(self, struct_name):
		type_list = []	
		for item in self.SymbolTable:
			if item[0] == 'global struct' and item[1][0] == struct_name:
				for tp in item[1][1]:
					type_list.append(tp[0])

		return type_list


	# first check if the exp has been defined in this function.
	# return 0: not defined; 1: defined
	def checkIfDefined(self, exp_id, symboltable):
		exp_not_define = True

		for item in symboltable:
			tp = item[0]
			if type(item[1]) == str:
				if exp_id == item[1]:
					exp_not_define = False
			elif type(item[1]) == list:
				if exp_id == item[1][0]:
					exp_not_define = False

		if exp_not_define:
			return 0
		return 1


	# check if exp_id is a array variable, return 0 -- not array variable, 1 -- array variable
	def checkIfArrayVariable(self, exp_id, symboltable):
		for item in symboltable:
			tp = item[0]
			if type(item[1]) == str:
				if exp_id == item[1] and not '-' in tp:
					return 0
			elif type(item[1]) == list:
				if exp_id == item[1][0] and not '-' in tp:
					return 0
		return 1


	# get args list of some function
	def getFuncArgsList(self, func_name):
		args_type_list = []
		args_list = None
		return_type = None

		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == func_name:
				args_list = item[2][1]
				return_type = item[1]

		if args_list == None:	# the fucntion has not been defined
			return None, None

		for var in args_list:
			args_type_list.append(var[0])
	
		return return_type, args_type_list


	# return a list of args, each item is a type
	def procArgs(self, args, al, symboltable, func_name, return_type):
		# Args : Exp COMMA Args
		# 	   | Exp
		if len(args.children) == 1:
			al.append(self.procExp(args.children[0], symboltable, func_name, return_type))

		elif len(args.children) == 3:
			al.append(self.procExp(args.children[0], symboltable, func_name, return_type))
			al = self.procArgs(args.children[2], al, symboltable, func_name, return_type)

		else:
			print('Something got wrong with Args.')

		return al
	

	def procSpecifier(self, Specifier, caller = None):
		# Specifier : TYPE
		# 			| StructSpecifier
		# StructSpecifier : STRUCT OptTag LC DefList RC
		# 				  | STRUCT Tag

		if type(Specifier.children[0]) == list:           # Specifier : TYPE
			return Specifier.children[0][1]               # return 'int'/'float'

		else:                                             # Specifier : StructSpecifier
			structSpecifier = Specifier.children[0]       # structSpecifier is a Node

			if len(structSpecifier.children) == 5:        # StructSpecifier : STRUCT OptTag LC DefList RC
				optTag = structSpecifier.children[1]      # optTag is a Node
				deflist = self.procDefList(structSpecifier.children[3], [], 0)  # type is list

				if optTag != None:                        # WATCH OUT! OptTag here can be empty !!
					return 'struct '+optTag.children[0][1], deflist
				else:
					return 'struct UNknownType', deflist

			elif len(structSpecifier.children) == 2:      # StructSpecifier : STRUCT Tag
				tag = structSpecifier.children[1]         # is a Node
				
				if caller == 'func': 
					# the specifier is a return_type, so check if this struct has been defined
					struct_defined = False
					for item in self.getSymbolTable():
						if item[0] == 'global struct' and item[1][0] == 'struct ' + tag.children[0][1]:
							struct_defined = True
					if not struct_defined:
						print('Error type 17 at Line %d: Undefined structure \"%s\"'%(Specifier.lineno, tag.children[0][1]))
				return 'struct '+tag.children[0][1]       # return 'struct id'

			else:
				print('Something got wrong in StructSpecifier!!')
	
	
	# return a list of items, dl is []
	def procDecList(self, DecList, dl, specifier):
		# DecList : Dec
		#         | Dec COMMA DecList

		if len(DecList.children) == 1:      # DecList : Dec
			dec = DecList.children[0]
			dl.append(self.procDec(dec, specifier))

		elif len(DecList.children) == 3:    # DecList : Dec COMMA DecList
			dec = DecList.children[0]
			dl.append(self.procDec(dec, specifier))
			dl = self.procDecList(DecList.children[2], dl, specifier)

		else:
			print('Something got wrong in DecList')

		return dl


	# return an item
	def procDec(self, dec, specifier):
		# Dec : VarDec
		#     | VarDec ASSIGNOP Exp

		if len(dec.children) == 1:      # Dec : VarDec
			varDec = dec.children[0]
			symbol = self.procVarDec(varDec, '')
			return symbol

		elif len(dec.children) == 3:    # Dec : VarDec ASSIGNOP Exp
			varDec = dec.children[0]
			symbol = [self.procVarDec(varDec, ''), dec.children[2]]  # return the Exp Node !!

			# check assignment mismatch in procCompSt() !!

			return symbol

		else:
			print('Something got wrong in Dec')


	# return an item
	def procVarDec(self, varDec, symbol):
		# VarDec : ID
		#        | VarDec LB INT RB
		if len(varDec.children) ==1:    # VarDec : ID
			# set global variable
			symbol += varDec.children[0][1]

		elif len(varDec.children) == 4: # VarDec : VarDec LB INT RB
			symbol = self.procVarDec(varDec.children[0], symbol)
			symbol += '['+str(varDec.children[2][1])+']'

		else:
			print('Something got wrong in VarDec')

		return symbol


	# return a list, dl is []
	# pos==0: in Struct ; pos==1: in CompSt
	def procDefList(self, defList, dl, pos):
		# DefList : Def DefList
		# 		  | empty
		if defList == None:
			return dl

		elif len(defList.children) == 2:   # DefList : Def DefList
			new_item = self.procDef(defList.children[0], 'global')

			self.checkRedefine(defList, new_item, dl, pos)

			# if it's a definition of a struct, then check if this struct has been defined
			for item in new_item:
				if 'struct' in item[0] and not self.checkStructDef(item):
					print('Error type 17 at Line %d: Undefined structure \"%s\".' %(defList.lineno, item[0].split(' ')[1]))

			for def_var in new_item:
				if pos == 0 and type(def_var[1]) == list and not def_var[1][0] in self.wrongVarInStruct:
					print('Error type 15 at Line %d: Initialized struct field.' %(defList.children[0].lineno))
					self.wrongVarInStruct.append(def_var[1][0])

				dl.append(def_var)

			dl = self.procDefList(defList.children[1], dl, pos)

		return dl


	# return True if has defined, otherwise return False
	def checkStructDef(self, struct_def):
		if '-' in struct_def[0]:          # it's a struct array
			struct_def = struct_def[0].split('-')[0]
		else:
			struct_def = struct_def[0]
		for item in self.SymbolTable:
			if item[0] == 'global struct' and item[1][0] == struct_def:
				return True
		return False


	# check redefine, return True if not redefine
	# pos: 0 -- in struct;  1 -- in function
	def checkRedefine(self, defList, new_item, dl, pos):
		# new var name in this definition
		new_var_list = []

		error_type = 3 if pos == 1 else 15  # redefine in function--3; redefine in struct--15

		for new_var in new_item:
			if type(new_var[1]) == str:
				new_var_list.append(new_var[1])		
			elif type(new_var[1]) == list:
				new_var_list.append(new_var[1][0])

		not_redefined = True

		# first check if there has redefined variable in a def
		for idx, var in enumerate(new_var_list, 0):
			if var in new_var_list[:idx]:
				not_redefined = False
				print('Error type %d at Line %d: Redefined variable \"%s\"' %(error_type, defList.children[0].lineno, var))

		# second check if there has redefined variable above
		old_var_list = []
		for old_defin in dl:
			if type(old_defin[1]) == str:
				old_var_list.append(old_defin[1])
			elif type(old_defin[1]) == list:
				old_var_list.append(old_defin[1][0])

		for new_var in new_var_list:
			if new_var in old_var_list:
				not_redefined = False
				print('Error type %d at Line %d: Redefined variable \"%s\"' %(error_type, defList.children[0].lineno, new_var))

		# third check if some struct name the same as variable name
		# struct name is also a variable name, should not be redefine !!
		structNames = self.getStructName()
		for new_var in new_var_list:
			if new_var in structNames:
				not_redefined = False
				print('Error type %d at Line %d: Redefined variable \"%s\"' %(error_type, defList.children[0].lineno, new_var))

		return not_redefined


	# return all struct names
	def getStructName(self):
		struct_name_list = []
		for item in self.SymbolTable:
			if item[0] == 'global struct':
				struct_name_list.append(item[1][0].split(' ')[1])

		return struct_name_list


	# return all fucntion names
	def getFuncName(self):
		func_name_list = []
		for item in self.SymbolTable:
			if item[0] == 'func':
				func_name_list.append(item[2][0])

		return func_name_list


	# return a list
	def procExtDecList(self, extdeclist, dl):
		# ExtDecList : VarDec
		#            | VarDec COMMA ExtDecList

		if len(extdeclist.children) == 1:      # ExtDecList : VarDec
			vardec = extdeclist.children[0]
			dl.append(self.procVarDec(vardec, ''))

		elif len(extdeclist.children) == 3:    # ExtDecList : VarDec COMMA ExtDecList
			vardec = extdeclist.children[0]
			dl.append(self.procVarDec(vardec, ''))
			dl = self.procExtDecList(extdeclist.children[2], dl)

		else:
			print('Something got wrong in ExtDecList')
		return dl


	# return a list
	def procFunDec(self, fundec):
		# FunDec : ID LP VarList RP
		# 		 | ID LP RP

		if len(fundec.children) == 3:   # FunDec : ID LP RP
			return [fundec.children[0][1], []]

		elif len(fundec.children) == 4: # FunDec : ID LP VarList RP
			return [fundec.children[0][1], self.procVarList(fundec.children[2], [])]
	
		else:
			print('Something got wrong in FunDec')


	# return a list
	def procVarList(self, varlist, vl):
		# VarList : ParamDec COMMA VarList
		#		  | ParamDec

		if len(varlist.children) == 1:    # VarList : ParamDec
			paramdec = varlist.children[0]
			specifier = paramdec.children[0]
			vardec = paramdec.children[1]

			specifier = self.procSpecifier(specifier)
			vardec = self.procVarDec(vardec, '')

			if '[' in vardec:  # it's an array !! change ['int', 'a[10]'] into ['int-10', 'a'] !!
				vardec = vardec.replace(']', '')
				vardec = vardec.split('[')
				for item in vardec[1:]:
					specifier += '-' + item
				vardec = vardec[0]

			vl.append([specifier, vardec])

		elif len(varlist.children) == 3:  # VarList : ParamDec COMMA VarList
			paramdec = varlist.children[0]
			specifier = paramdec.children[0]
			vardec = paramdec.children[1]

			specifier = self.procSpecifier(specifier)
			vardec = self.procVarDec(vardec, '')

			if '[' in vardec:  # it's an array !! change ['int', 'a[10]'] into ['int-10', 'a'] !!
				vardec = vardec.replace(']', '')
				vardec = vardec.split('[')


				for item in vardec[1:]:
					specifier += '-' + item
				vardec = vardec[0]

			vl.append([specifier, vardec])

			vl = self.procVarList(varlist.children[2], vl)

		else:
			print('Something got wrong with VarList')		

		return vl


	# check if there has undefined function
	def checkUndefFunc(self):
		defined_func = []

		func_dec_dict = {}
		for item in self.SymbolTable:
			if item[0] == 'func-dec':
				func_dec_dict[item[2][0]] = [item[1], item[2][1], item[3]] # [return-type, param_list, line_num] 
			elif item [0] == 'func':
				for key, val in func_dec_dict.items():
					if key == item[2][0] and val[0] == item[1] and val[1] == item[2][1]:
						defined_func.append(key)

		for func in defined_func:
			func_dec_dict.pop(func)

		if len(func_dec_dict) > 0:
			for key, val in func_dec_dict.items():
				print('Error type 18 at Line %d: Undefined function \"%s\".' %(val[2], key))
