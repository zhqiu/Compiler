"""
	use SDT to turn tree-IR to linear-IR
"""

from operator import mul
from functools import reduce

class Translate(object):
	
	def __init__(self, SymbolTable, root, SemAnalysis, tokens):
		# use the SymbolTable made in semantic analysis
		# type of SymbolTable is list !!
		self.SymbolTable = SymbolTable
		self.tokens = tokens              # tokens defined in lab3.py and used to output parsing tree
		self.treeRoot = root              # root of parsing tree
		self.semAnalysis = SemAnalysis    # need to use procSpecifier() and procDecList() in class SemAnalysis
		self.temp_idx = 0    # index used in new_item()
		self.label_idx = 0   # index used in new_label()
		self.var_base = 0    # number of variables in previous functions
		self.op_dict = {'PLUS':'+', 'MINUS':'-', 'STAR':'*', 'DIV':'/'}
		self.base_type_len = {'int':4, 'float':4}
		self.current_function_name = None # name of current function
		self.raw_code = ''

	
	def __call__(self, output_filename):        # do translation
		"""
			do translation
			write the result into 'output_filename' in local dir
		"""
		self.preOrderTraversal(self.treeRoot)
		with open(output_filename, 'w') as f:
			for line in self.raw_code:
				f.write(line)


	def printSymbolTable(self):
		for item in self.SymbolTable:
			print(item)


	def new_temp(self):
		self.temp_idx += 1
		return 't' + str(self.temp_idx)
	

	def new_label(self):
		self.label_idx += 1
		return 'label' + str(self.label_idx)

	
	def printSynAnaTree(self, root, indent):
		# root -> left child -> right child
		if root == None:
			return
		print(' '*indent, end='')
		if type(root) == list and len(root) == 2 and root[0] in ['ID', 'TYPE', 'INT', 'FLOAT', 'RELOP']:
			print(root[0]+': '+str(root[1]))          # terminal symbols(ID,TYPE,INT,FLOAT)
			return
		elif type(root) == str and root in self.tokens:
			print(root)                          # any other terminal symbols
			return                   
		else:                                    # non-terminal symbols
			print(root.node_type+' ('+str(root.lineno)+')')   # in ply, lineno start from 0
			for i in range(len(root.children)):
				self.printSynAnaTree(root.children[i], indent+2)

	
	def preOrderTraversal(self, root):
		# root -> left child -> right child
		if root == None:
			return
		if type(root) == list and len(root) == 2 and root[0] in ['ID', 'TYPE', 'INT', 'FLOAT', 'RELOP']:
			return
		elif type(root) == str and root in self.tokens:
			# any other terminal symbols
			return                   
		else:                                 # non-terminal symbols
			if root.node_type == 'ExtDef':        
				self.raw_code += self.translate_ExtDef(root)      # change here to debug
			for i in range(len(root.children)):
				self.preOrderTraversal(root.children[i])

	
	def length(self, tp):
		"""
			return length(int) of one type
			eg:  int -> 4, float -> 4, int-10 -> 40, struct_name -> xxx
			
			assume there are no struct array !
		"""
		if not '-' in tp and not 'struct' in tp:
			return self.base_type_len[tp]
		elif 'struct' in tp:   # it's a struct
			if '-' in tp:                                          # deal with struct array
				num_of_elm = reduce(mul, map(int, tp.split('-')[1:]))
				tp = tp.split('-')[0]
			else:
				num_of_elm = 1
			length = 0
			for item in self.SymbolTable:
				if item[0]=='global struct' and item[1][0]==tp:
					for defin in item[1][1]:
						length += self.length(defin[0])
			return length * num_of_elm
		elif '-' in tp:        # it's a array
			num_of_elm = reduce(mul, map(int, tp.split('-')[1:]))
			base_len = self.base_type_len[tp.split('-')[0]]
			return num_of_elm * base_len

	
	def lookup(self, Id):
		"""
			look up one id in symboltable
			arg: Id(str)
			return: v_i(str)
		"""
		has_id = False
		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == self.current_function_name:
				id_list = item[3]
				for idx, def_id in enumerate(id_list, 1):
					if def_id[1] == Id or (len(def_id[1])==2 and def_id[1][0]==Id):
						has_id = True
						return 'v' + str(idx + self.var_base)
		if not has_id:
			print('Error! doesn\'t has id: %s' %(Id))
	

	def translate_Exp(self, exp, place):
		"""
			Args:  exp(Node) -- Node of one Exp
				   place -- temp variable
			Return: code of this Exp
		"""
		if len(exp.children) == 1:   # 'ID'/'INT'/'FLOAT'
			t, v = exp.children[0][0], exp.children[0][1]  # t:'ID'/'INT'/'FLOAT' v:name or number
			if t in ['INT', 'FLOAT']:
					return place + ' := ' + '#' + v + '\n' if place != None else '#' + v
			elif t == 'ID':
				var = self.lookup(v)
				return place + ' := ' + var + '\n' if place != None else var

		elif len(exp.children) == 2: # 'MINUS Exp'/'NOT Exp'
			if exp.children[0] == 'MINUS':
				t1 = self.new_temp()
				code1 = self.translate_Exp(exp.children[1], t1)
				code2 = place + ' := #0 - ' + t1 + '\n' if place != None else ''
				return code1 + code2

			elif exp.children[0] == 'NOT':
				label1 = self.new_label()
				label2 = self.new_label()
				code0 = place + ' := #0\n' if place != None else ''
				code1 = self.translate_Cond(exp, label1, label2)
				code2 = 'LABEL ' + label1 + ' :\n' + place + ' := #1\n' if place != None else ''
				return code0 + code1 + code2 + 'LABEL ' + label2 + ' :\n'
			
		elif len(exp.children) == 3: # 'Exp op Exp'/'LP Exp RP'/'ID LP RP'/'Exp DOT ID'
			if exp.children[1] in ['PLUS', 'MINUS', 'STAR', 'DIV']:
				if type(exp.children[0].children[0])==list and exp.children[0].children[0][0] in ['ID', 'INT', 'FLOAT'] \
															and len(exp.children[0].children)==1:  # can be optimized!
					t1 = self.translate_Exp(exp.children[0], None)
					code1 = ''
				else:
					t1 = self.new_temp()
					code1 = self.translate_Exp(exp.children[0], t1)
				if type(exp.children[2].children[0])==list and exp.children[2].children[0][0] in ['ID', 'INT', 'FLOAT'] \
															and len(exp.children[2].children)==1:  # can be optimized!
					t2 = self.translate_Exp(exp.children[2], None)
					code2 = ''
				else:
					t2 = self.new_temp()
					code2 = self.translate_Exp(exp.children[2], t2)
				
				code3 = place + ' := ' + t1 + ' ' + self.op_dict[exp.children[1]] + ' ' + t2 + '\n' if place != None else ''
				return code1 + code2 + code3

			elif exp.children[1] in ['AND', 'OR'] or (type(exp.children[1]) == list and exp.children[1][0] == 'RELOP'):
				label1 = self.new_label()
				label2 = self.new_label()
				code0 = place + ' := #0\n' if place != None else ''
				code1 = self.translate_Cond(exp, label1, label2)
				code2 = 'LABEL ' + label1 + ' :\n' + place + ' := #1\n' if place != None else ''
				return code0 + code1 + code2 + 'LABEL ' + label2 + ' :\n'

			elif exp.children[1] == 'ASSIGNOP':
				if type(exp.children[0])!=list and len(exp.children[0].children)!=1:        
					# exp1 is a node, it should be a struct member or a array member
					if 'DOT' in exp.children[0].children:  # it's a struct member
						code1 = self.translate_Exp(exp.children[0], None) # address_variable store the address of Exp.ID
						code1 = code1.split('\n')
						address_variable = code1[1]
						code1 = code1[0] + '\n'
						t1 = self.new_temp()
						code2 = self.translate_Exp(exp.children[2], t1)
						code3 = '*' + address_variable + ' := ' + t1 + '\n'
						return code1 + code2 + code3
					elif 'LB' in exp.children[0].children: # it's a array member
						t1 = self.new_temp()
						code2 = self.translate_Exp(exp.children[2], t1)
						code1 = self.translate_Exp(exp.children[0], None)
						code1 = code1.split('$')
						address_variable = code1[1]
						code1 = code1[0]
						code3 = '*' + address_variable + ' := ' + t1 + '\n'
						return code1 + code2 + code3
					else:
						print('WTF! it\'s a node but it\'s not a struct nor a array !!')
				else:                                   # exp1 is a ID
					exp1 = exp.children[0]
					t, v = exp1.children[0][0], exp1.children[0][1]
					var = self.lookup(v)
					# exp2 can be in [ID, INT, FLOAT], then can be optimized !
					if len(exp.children[2].children)==1 and exp.children[2].children[0][0] in ['ID', 'INT', 'FLOAT']:
						code1 = self.translate_Exp(exp.children[2], None)
						rt_code = var + ' := ' + code1 + '\n'
					else:
						t1 = self.new_temp()
						code1 = self.translate_Exp(exp.children[2], t1)
						code2 = var + ' := ' + t1 + '\n'
						code3 = place + ' := ' + var + '\n' if place != None else ''
						rt_code = code1 + code2 + code3
					return rt_code

			elif exp.children[1] == 'LP' and exp.children[2] == 'RP': # ID LP RP     
				func_name = exp.children[0][1]
				if func_name == 'read':
					return 'READ ' + place +'\n' if place != None else ''
				return place + ' := CALL ' + func_name + '\n' if place != None else ''

			elif exp.children[0] == 'LP' and exp.children[2] == 'RP': # LP Exp RP    
				return self.translate_Exp(exp.children[1], place)

			elif exp.children[1] == 'DOT':                            # Exp DOT ID
				raw_list = []
				raw_list = self.getExpList(exp, raw_list)

				struct_name = raw_list[0]

				exp_type, exp_struct_type, var_idx = self.getStructInfo(struct_name)
				#self.genStructBiasCode(raw_list, exp_type, exp_struct_type, var_idx)

				# find bias of ID
				id_name = exp.children[2][1]
				bias = 0
				for item in self.SymbolTable:
					if item[0] == 'global struct' and item[1][0] == exp_struct_type:
						def_list = item[1][1]
						for defin in def_list:
							if defin[1] == id_name:
								break
							else:
								bias += self.length(defin[0])
				t1 = self.new_temp()
				if exp_type == 'var':
					code1 = t1 + ' := &' + var_idx + ' + #' + str(bias) + '\n' # calculate the address
					code2 = place + ' := *' + t1 + '\n' if place != None else t1  # t1 is the address, just return it !!
				elif exp_type == 'add':
					code1 = t1 + ' := ' + var_idx + ' + #' + str(bias) + '\n'  # calculate the address
					code2 = place + ' := *' + t1 + '\n' if place != None else t1  # ti is the address, just return it !!
				return code1 + code2

		elif len(exp.children) == 4:
			if exp.children[1] == 'LP' and exp.children[3] == 'RP':   # 'ID LP Args RP'
				func_name = exp.children[0][1]
				arg_list = []
				code1 = self.translate_Args(exp.children[2], arg_list)
				if func_name == 'write':
					return code1 + 'WRITE ' + arg_list[0] + '\n'
				code2 = ''
				for arg in arg_list:
					# if arg is a struct variable or a array variable, then it's address should be passed in !!
					# arg should be v_i, temp variable cannot be struct or array !!
					if arg[0] == 'v':
						arg_type = None
						for item in self.SymbolTable:
							if item[0] == 'func' and item[2][0] == self.current_function_name:
								arg_type = item[3][int(arg[1:])-self.var_base-1][0]
						if arg_type != None and ('struct' in arg_type or '-' in arg_type):
							arg = '&' + arg
					code2 = code2 + 'ARG ' + arg + '\n'
				code3 = place + ' := CALL ' + func_name + '\n'
				return code1 + code2 + code3

			elif exp.children[1] == 'LB' and exp.children[3] == 'RB': # 'Exp LB Exp RB'
				raw_list = []
				raw_list = self.getExpList(exp, raw_list)

				array_name = raw_list[0]
				var_type, dim_type, var_idx = self.getArrayVarInfo(array_name)
				bias_var, bias_code = self.genArrayBiasCode(raw_list, dim_type)
				var_idx = self.lookup(array_name)
				if var_type == 'add':
					t1 = self.new_temp()
					code1 = bias_code
					code2 = t1 + ' := ' + var_idx + ' + ' + bias_var + '\n'   # t1 is the address
					code3 = place + ' := *' + t1 + '\n' if place != None else '$' + t1
				elif var_type == 'var':
					t1 = self.new_temp()
					code1 = bias_code
					code2 = t1 + ' := &' + var_idx + ' + ' + bias_var + '\n'  # t1 is the address
					code3 = place + ' := *' + t1 + '\n' if place != None else '$' + t1
				return code1 + code2 + code3
				
	
	def getExpList(self, exp, raw_list):
		"""
			get a Exp Node and return its raw_list
			eg: Exp(a[i][0][j]) => ['a', 'i', '0', 'j']
				Exp(a[i+j-1])   => ['a', Node object]

			Exp : Exp LB Exp RB / Exp DOT ID

			use pre-Order traversal
		"""
		if exp == None:
			return raw_list
		elif type(exp) == str:
			return raw_list
		elif type(exp) == list and exp[0] == 'ID':       # it's a struct array
			raw_list.append(exp[1])
			return raw_list
		elif not 'LB' in exp.children and not 'DOT' in exp.children:   # it's a Exp, between [] ; or ahead []
			if len(exp.children) == 1 and exp.children[0][0] in ['ID', 'INT']:
				raw_list.append(exp.children[0][1])
				return raw_list
			else:
				raw_list.append(exp)
				return raw_list
		else:
			for sub_exp in exp.children:
				self.getExpList(sub_exp, raw_list)
			return raw_list


	def getStructInfo(self, struct_var_name):
		"""
			input: struct_var_name
			return: exp_type (add/var)
				    exp_struct_type (struct xxx)
					var_idx (v1)
		"""
		# need to find out if the name is a variable or an address
		exp_type = None               # str: 'var' / 'add'
		exp_struct_type = None        # str: 'struct xxxx'
		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == self.current_function_name:
				param_list = item[2][1]
				var_list = item[3]
				for param in param_list:
					if param[1] == struct_var_name:
						exp_type, exp_struct_type = 'add', param[0]
				if exp_type != None and exp_struct_type != None:
					break
				for var in var_list:
					if var[1] == struct_var_name:
						exp_type, exp_struct_type = 'var', var[0]
		# then look up this variable, find its v_i
		var_idx = self.lookup(struct_var_name)
		return exp_type, exp_struct_type, var_idx


	def getArrayVarInfo(self, array_name):
		"""
			get some info of one array
			eg: var_type('var'/'add'), dim_type(str, eg:'int-2-2'), var_idx(v_i)
		"""
		var_type, dim_type = None, None
		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == self.current_function_name:
				param_list = item[2][1]
				var_list = item[3]
				for param in param_list:
					if param[1] == array_name:
						var_type, dim_type = 'add', param[0]
				if var_type != None and dim_type != None:
					break
				for var in var_list:
					if var[1] == array_name:
						var_type, dim_type = 'var', var[0]
		# then look up this variable, find its v_i
		var_idx = self.lookup(array_name)
		return var_type, dim_type, var_idx


	def genArrayBiasCode(self, raw_list, dim_type):
		"""
			generate the code of calculate the bias of one array element
			return 1.variable which store the bias
				   2.code to calculate the bias
		"""
		num_of_dim = dim_type.count('-')  # number of dimension
		if num_of_dim == 1:
			idx_str = raw_list[1]
			ele_len = self.length(dim_type.split('-')[0])
			if type(idx_str)==str and idx_str.isdigit():
				bias = int(idx_str)*ele_len
				return '#' + str(bias), ''
			elif type(idx_str)==str and not idx_str.isdigit():
				idx_v = self.lookup(idx_str)
				t1 = self.new_temp()
				rt_code = t1 + ' := ' + idx_v + ' * #' + str(ele_len) + '\n'
				return t1, rt_code
			else:                         # it's a Exp
				t1 = self.new_temp()
				t2 = self.new_temp()
				rt_code = self.translate_Exp(raw_list[1], t1)
				rt_code += t2 + ' := ' + t1 + ' * #' + str(ele_len) + '\n'
				return t2, rt_code
		elif num_of_dim >= 2:
			ele_len = self.length(dim_type.split('-')[0])      
			dim_list = list(map(int, dim_type.split('-')[1:])) # eg: int[1][3][2] => [1,3,2]
			dim_list.append(1)                                 # [1,3,2] => [1,3,2,1]
			dim_len = []  # eg: int[1][3][2]=> [24,8,4]
			for idx in range(num_of_dim):
				dim_len.insert(0, ele_len * reduce(mul, dim_list[num_of_dim-idx:]))
			param_list = raw_list[1:]                          # eg: ['0', 'j'] for op[0][j]
			rt_code = ''
			for idx, param_str in enumerate(param_list):
				if type(param_str)==str and not param_str.isdigit():
					param_list[idx] = self.lookup(param_str)
				if type(param_str)==str and param_str.isdigit():
					param_list[idx] = '#' + param_str			
			t1 = self.new_temp()
			t2 = self.new_temp()
			t3 = self.new_temp()
			# calculate t1 and t2 first
			if type(param_list[-1])==str and param_list[-1] != '#0':
				rt_code += t1 + ' := ' + param_list[-1] + ' * #' + str(dim_len[-1]) + '\n'
			elif param_list[-1] == '#0':
				rt_code += t1 + ' := #0\n'
			else:             # must be a Exp
				tx = self.new_temp()
				rt_code += self.translate_Exp(param_list[-1], tx)
				rt_code += t1 + ' := ' + tx + ' * #' + str(dim_len[-1]) + '\n'

			if type(param_list[-2])==str and param_list[-2] != '#0':
				rt_code += t2 + ' := ' + param_list[-2] + ' * #' + str(dim_len[-2]) + '\n'
			elif param_list[-2] == '#0':
				rt_code += t2 + ' := #0\n'
			else:             # must be a Exp
				tx = self.new_temp()
				rt_code += self.translate_Exp(param_list[-2], tx)
				rt_code += t2 + ' := ' + tx + ' * #' + str(dim_len[-2]) + '\n'

			rt_code += t3 + ' := ' + t1 + ' + ' + t2 + '\n'
			t_sum = t3
			for i in range(num_of_dim-2):
				t1 = self.new_temp()
				if type(param_list[-(3+i)])==str and param_list[-(3+i)] != '#0':
					rt_code += t1 + ' := ' + param_list[-(3+i)] + ' * #' + str(dim_len[-(3+i)]) + '\n'
				elif param_list[-(3+i)] == '#0':
					rt_code += t1 + ' := #0\n'
				else:           # must be a Exp
					tx = self.new_temp()
					rt_code += self.translate_Exp(param_list[-(3+i)], tx)
					rt_code += t1 + ' := ' + tx + ' * #' + str(dim_len[-(3+i)]) + '\n'
				t2 = self.new_temp()
				rt_code += t2 + ' := ' + t1 + ' + ' + t_sum + '\n'
				t_sum = t2
			return t_sum, rt_code


	"""
	def genStructBiasCode(self, raw_list, exp_type, exp_struct_type, var_idx):
		
			#generate the code of calculate the bias of one struct element
			#return 1.variable which store the bias
			#	   2.code to calculate the bias
		
		print('raw_list:', raw_list)
		print('exp_type:', exp_type)
		print('exp_struct_type:', exp_struct_type)
		print('var_idx:', var_idx)
		print(self.SymbolTable)
		for item in raw_list:
			if not item.isdigit():
				print(self.getVarType(item))
	"""


	def getVarType(self, var_name):
		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == self.current_function_name:
				for var in item[3]:
					if var[1] == var_name:
						return var[0]


	def getStructMemberBias(self, struct_type, member_name):
		bias = 0
		for item in self.SymbolTable:
			if item[0] == 'global struct' and item[1][0] == struct_type:
				def_list = item[1][1]
				for defin in def_list:
					if defin[1] == member_name:
						break
					else:
						bias += self.length(defin[0])
		return bias
		

	def translate_Stmt(self, stmt):
		"""
			Args:  stmt(Node) -- Node of one Stmt
			Return: code of this Stmt(str), return_flag: 1--Stmt contains return, 0--ow
		"""
		if len(stmt.children) == 1:    # CompSt
			return 0, self.translate_CompSt(stmt.children[0])

		elif len(stmt.children) == 2:  # Exp SEMI
			t1 = self.new_temp()
			return 0, self.translate_Exp(stmt.children[0], t1)
			
		elif len(stmt.children) == 3:  # RETURN Exp SEMI
			exp = stmt.children[1]
			if type(exp.children[0])==list and len(exp.children)==1 and exp.children[0][0] in ['ID', 'INT', 'FLOAT']:
				t1 = self.translate_Exp(stmt.children[1], None)
				code1 = ''
			else:
				t1 = self.new_temp()
				code1 = self.translate_Exp(stmt.children[1], t1)
			code2 = 'RETURN ' + t1 + '\n'
			return 1, code1 + code2

		elif len(stmt.children) == 5:  
			if stmt.children[0] == 'IF':       # IF LP Exp RP Stmt
				label1 = self.new_label()
				label2 = self.new_label()
				code1 = self.translate_Cond(stmt.children[2], label1, label2)
				_, code2 = self.translate_Stmt(stmt.children[4])
				return 0, code1 + 'LABEL ' + label1 + ' :\n' + code2 + 'LABEL ' + label2 + ' :\n' 

			elif stmt.children[0] == 'WHILE':  # WHILE LP Exp RP Stmt
				label1 = self.new_label()
				label2 = self.new_label()
				label3 = self.new_label()
				code1 = self.translate_Cond(stmt.children[2], label2, label3)
				rt_flag, code2 = self.translate_Stmt(stmt.children[4])
				if rt_flag == 1:
					return 0, 'LABEL '+label1+' :\n'+code1+'LABEL '+label2+' :\n'+code2+'\n'+'LABEL '+label3+' :\n'
				else:
					return 0, 'LABEL '+label1+' :\n'+code1+'LABEL '+label2+' :\n'+code2+'GOTO '+label1+'\n'+'LABEL '+label3+' :\n'

		else:                                  # IF LP Exp RP Stmt ELSE Stmt
			label1 = self.new_label()
			label2 = self.new_label()
			label3 = self.new_label()
			code1 = self.translate_Cond(stmt.children[2], label1, label2)
			rt_flag, code2 = self.translate_Stmt(stmt.children[4])
			_, code3 = self.translate_Stmt(stmt.children[6])
			if rt_flag == 1:
				return 0, code1+'LABEL '+label1+' :\n'+code2+'LABEL '+label2+' :\n'+code3
			else:
				return 0, code1+'LABEL '+label1+' :\n'+code2+'GOTO '+label3+'\n'+'LABEL '+label2+' :\n'+code3+'LABEL '+label3+' :\n'



	def translate_Cond(self, exp, label_true, label_false):
		if len(exp.children) == 2 and exp.children[0] == 'NOT':  # NOT Exp
			return self.translate_Cond(exp, label_false, label_true)

		elif len(exp.children) == 3 and exp.children[1] == 'AND':  # Exp AND Exp
			label1 = self.new_label()
			code1 = self.translate_Cond(exp.children[0], label1, label_false)
			code2 = self.translate_Cond(exp.children[2], label_true, label_false)
			return code1 + 'LABEL ' + label1 + ' :\n' + code2

		elif len(exp.children) == 3 and exp.children[1] == 'OR':  # Exp OR Exp
			label1 = self.new_label()
			code1 = self.translate_Cond(exp.children[0], label_true, label1)
			code2 = self.translate_Cond(exp.children[2], label_true, label_false)
			return code1 + 'LABEL ' + label1 + ' :\n' + code2

		elif len(exp.children) == 3 and type(exp.children[1]) == list and exp.children[1][0] == 'RELOP':  # Exp RELOP Exp
			if len(exp.children[0].children)==1 and exp.children[0].children[0][0] in ['ID', 'INT', 'FLOAT']:  # can be optimized!
				t1 = self.translate_Exp(exp.children[0], None)
				code1 = ''
			else:
				t1 = self.new_temp()
				code1 = self.translate_Exp(exp.children[0], t1)

			if len(exp.children[2].children)==1 and exp.children[2].children[0][0] in ['ID', 'INT', 'FLOAT']:  # can be optimized!
				t2 = self.translate_Exp(exp.children[2], None)
				code2 = ''
			else:
				t2 = self.new_temp()
				code2 = self.translate_Exp(exp.children[2], t2)

			op = exp.children[1][1]
			code3 = 'IF ' + t1 + ' ' + op + ' ' + t2 + ' GOTO ' + label_true + '\n'
			return code1 + code2 + code3 + 'GOTO ' + label_false + '\n'

		else:
			t1 = self.new_temp()
			code1 = self.translate_Exp(exp, t1)
			code2 = 'IF ' + t1 + ' != #0 GOTO ' + label_true + '\n'
			return code1 + code2 + 'GOTO ' + label_false + '\n'



	def translate_Args(self, args, arg_list):
		"""
			type of args_list is list
			args can a variable or a expression
		"""	
		if len(args.children) == 1:    # Exp
			if type(args.children[0].children[0])==list and args.children[0].children[0][0] in ['ID', 'INT', 'FLOAT'] \
														and len(args.children[0].children)==1:
				t1 = self.translate_Exp(args.children[0], None)
				code1 = ''
			else:
				t1 = self.new_temp()
				code1 = self.translate_Exp(args.children[0], t1)
			arg_list.insert(0, t1)
			return code1
			
		elif len(args.children) == 3:  # Exp COMMA Args
			t1 = self.new_temp()
			code1 = self.translate_Exp(args.children[0], t1)
			arg_list.insert(0, t1)
			code2 = self.translate_Args(args.children[2], arg_list)
			return code1 + code2


	def translate_CompSt(self, compst):
		# CompSt : LC DefList StmtList RC
		code1 = self.translate_DefList(compst.children[1])
		code2 = self.translate_StmtList(compst.children[2])
		return code1 + code2


	def translate_DefList(self, deflist):
		# DefList : Def DefList
		#         : empty
		if deflist == None:
			return ''
		else:
			code1 = self.translate_Def(deflist.children[0])
			code2 = self.translate_DefList(deflist.children[1])
			return code1 + code2


	def translate_Def(self, defin):
		# Def : Specifier DecList SEMI
		specifier = self.semAnalysis.procSpecifier(defin.children[0])
		declist = self.semAnalysis.procDecList(defin.children[1], [], specifier)
		defin = self.semAnalysis.procArrayType(specifier, declist)
		code_for_defin = ''
		for item in defin:
			if 'struct' in item[0]:
				code_for_defin += 'DEC ' + self.lookup(item[1]) + ' ' + str(self.length(item[0])) + '\n'
			if '-' in item[0]:    # it's an array
				base_type = item[0].split('-')[0]
				base_type_len = self.base_type_len[base_type]
				num_of_elm = reduce(mul, map(int, item[0].split('-')[1:]))
				code_for_defin += 'DEC ' + self.lookup(item[1]) + ' ' + str(base_type_len*num_of_elm) + '\n'
			if type(item[1])== list and len(item[1])==2: # it's a definition with initialization
				var_idx = self.lookup(item[1][0])
				code_for_defin += self.translate_Exp(item[1][1], var_idx)

		return code_for_defin

	def translate_StmtList(self, stmtlist):
		# StmtList : Stmt StmtList
		#          : empty
		if stmtlist == None:
			return ''
		_, code1 = self.translate_Stmt(stmtlist.children[0])
		code2 = self.translate_StmtList(stmtlist.children[1])
		return code1 + code2


	def translate_ExtDef(self, extdef):
		# ExtDef : Specifier FunDec CompSt
		# only translate function !
		# return code(str)

		# don't process struct and global variable
		if len(extdef.children)==2 or (len(extdef.children)==3 and extdef.children[2]=='SEMI'):
			return ''

		# first get function name
		fundec = self.semAnalysis.procFunDec(extdef.children[1])
		func_name, var_list = fundec[0], fundec[1]

		self.current_function_name = func_name  # set current function here !!!

		# generate code for function head
		code1 = 'FUNCTION ' + func_name + ' :\n'
		
		# PARAMs
		for param in var_list:
			code1 += 'PARAM ' + self.lookup(param[1]) + '\n'

		# generate code for function body
		code2 = self.translate_CompSt(extdef.children[2])

		# modify var_base
		for item in self.SymbolTable:
			if item[0] == 'func' and item[2][0] == func_name:
				self.var_base += len(item[3])

		return code1 + code2 + '\n'
