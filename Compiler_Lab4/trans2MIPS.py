"""
	use SDT to translate tree-IR into linear-IR in MIPS form

	only accept simple variable or one-dimension array variable
"""

from operator import mul
from functools import reduce

class Translate2MIPS(object):

	def __init__(self, SymbolTable, root, SemAnalysis, tokens):
		# use the SymbolTable made in semantic analysis
		# type of SymbolTable is list !!
		self.SymbolTable = SymbolTable
		self.treeRoot = root              # root of parsing tree
		self.tokens = tokens              # tokens defined in lab3.py and used to output parsing tree
		self.semAnalysis = SemAnalysis    # need to use procSpecifier() and procDecList() in class SemAnalysis
		self.base_type_len = {'int':4}
		self.current_function_name = None # name of current function
		self.var_bias = -4                # bias of variable in current function
		self.label_idx = 0                # index used in new_label()
		self.raw_code = ''
		self.var_address_dict = {}        # store the address and length of each variable
		self.function_param_reg_idx = -1
		self.empty_reg_idx = -1
		self.op_instr = {'==':'beq', '!=':'bne', '>':'bgt', '<':'blt', '>=':'bge', '<=':'ble'}
		self.add_program_head()


	def add_program_head(self):
		self.raw_code += '.data\n_prompt: .asciiz "Enter an integer:"\n_ret: .asciiz \"\\n\"\n'
		self.raw_code += '.globl main\n.text\n'
		self.raw_code += 'read:\n  li $v0, 4\n  la $a0, _prompt\n  syscall\n  li $v0, 5\n  syscall\n  jr $ra\n'
		self.raw_code += 'write:\n  li $v0, 1\n  syscall\n  li $v0, 4\n  la $a0, _ret\n  syscall\n  move $v0, $0\n  jr $ra\n'


	def new_label(self):
		self.label_idx += 1
		return 'label' + str(self.label_idx)

		
	def __call__(self):                      # do translation
		#self.printSynAnaTree(self.treeRoot, 0)	
		
		self.preOrderTraversal(self.treeRoot)
		print(self.raw_code)


	def allocFuncParamReg(self):
		self.function_param_reg_idx += 1
		if self.function_param_reg_idx >= 4:
			print('Error, cannot process more than 4 params !!')
		return '$a' + str(self.function_param_reg_idx)


	def allocEmptyReg(self):
		self.empty_reg_idx += 1
		if self.empty_reg_idx > 18:
			print('Sorry, no enough temp register!')
		reg_name = 't' if self.empty_reg_idx<=9 else 's'
		reg_idx = self.empty_reg_idx if self.empty_reg_idx<10 else self.empty_reg_idx-10
		return '$' + reg_name + str(reg_idx)


	def preOrderTraversal(self, root):
		"""
			using pre-order traversal and SDT to generate asm code
		"""
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


	def printSynAnaTree(self, root, indent):
		"""
			output Syntax Analysis Tree
		"""
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


	def length(self, tp):
		"""
			return length(int) of one type
			tp(str): 'int' or 'int-10'
			return: eg:  int -> 4, int-10 -> 40
		"""
		tp = tp + '-1'
		num_of_elm = reduce(mul, map(int, tp.split('-')[1:]))
		return num_of_elm * 4                                # only int is allowed !


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

		if func_name in ['read', 'write']:
			return ''

		self.current_function_name = func_name  # set current function here !!!
		self.var_bias = -4                     # set initial bias of this function

		# generate code for function head
		code0 = func_name + ':\n'
		
		# save $s0 - $s7
		for i in range(8):
			code0 += '  sw $s' + str(i) + ', ' + str(self.var_bias) + '($sp)\n'
			self.var_bias += -4

		code1 = ''
		# PARAMs, should read param stored in $a0 ~ $a3 into stack
		if len(var_list) > 0:
			for idx, var in enumerate(var_list):
				self.var_address_dict[var[1]] = [self.var_bias, self.length(var[0])]
				code1 += '  sw $a' + str(idx) + ', ' + str(self.var_bias) + '($sp)\n'
				self.var_bias += -4

		code2 = self.translate_CompSt(extdef.children[2])

		return code0 + code1 + code2 + '\n'


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
		for var in defin:
			var_type = var[0]
			var_len = self.length(var_type)
			if type(var[1])==list and len(var[1])==2: # it's a definition with initialization
				self.var_address_dict[var[1][0]] = [self.var_bias, var_len]
				t0 = self.allocEmptyReg()
				code_for_defin += self.translate_Exp(var[1][1], t0)  # the result of Exp is put into '$t0'
				code_for_defin += '  sw ' + t0 + ', '+ str(self.var_bias) + '($sp)\n'
				self.empty_reg_idx = -1
				self.var_bias -= var_len
			else:                                       # it's a definition without initialization
				self.var_address_dict[var[1]] = [self.var_bias, var_len]
				self.var_bias -= var_len
		return code_for_defin


	def translate_StmtList(self, stmtlist):
		# StmtList : Stmt StmtList
		#          : empty
		if stmtlist == None:
			return ''
		code1 = self.translate_Stmt(stmtlist.children[0])
		code2 = self.translate_StmtList(stmtlist.children[1])
		return code1 + code2


	def translate_Stmt(self, stmt):
		"""
			Args:  stmt(Node) -- Node of one Stmt
			Return: code of this Stmt(str)
		"""
		if len(stmt.children) == 1:    # CompSt
			rt_code = self.translate_CompSt(stmt.children[0])
			return rt_code

		elif len(stmt.children) == 2:  # Exp SEMI
			t0 = self.allocEmptyReg()
			rt_code = self.translate_Exp(stmt.children[0], t0)
			self.empty_reg_idx = -1
			return rt_code
			
		elif len(stmt.children) == 3:  # RETURN Exp SEMI
			exp = stmt.children[1]
			t0 = self.allocEmptyReg()
			code1 = self.translate_Exp(stmt.children[1], t0)
			code2 = '  move $v0, ' + t0 + '\n'

			# recover $s0 - $s7
			start_bias = -32
			code2_5 = ''
			for i in range(8)[::-1]:
				code2_5 += '  lw $s' + str(i) + ', ' + str(start_bias) + '($sp)\n'
				start_bias += 4

			code3 = '  jr $ra\n'
			self.empty_reg_idx = -1
			return code1 + code2 + code2_5 + code3

		elif len(stmt.children) == 5:  
			if stmt.children[0] == 'IF':       # IF LP Exp RP Stmt
				label1 = self.new_label()
				label2 = self.new_label()
				code1 = self.translate_Cond(stmt.children[2], label1, label2)
				code2 = self.translate_Stmt(stmt.children[4])
				return code1 + label1 + ':\n' + code2 + label2 + ':\n'

			elif stmt.children[0] == 'WHILE':  # WHILE LP Exp RP Stmt
				label1 = self.new_label()
				label2 = self.new_label()
				label3 = self.new_label()
				code1 = self.translate_Cond(stmt.children[2], label2, label3)
				code2 = self.translate_Stmt(stmt.children[4])
				return label1 + ':\n' + code1 + label2 + ':\n' + code2 + '  j ' + label1 + '\n' + label3 + ':\n'

		else:                                  # IF LP Exp RP Stmt ELSE Stmt
			label1 = self.new_label()
			label2 = self.new_label()
			label3 = self.new_label()
			code1 = self.translate_Cond(stmt.children[2], label1, label2)
			code2 = self.translate_Stmt(stmt.children[4])
			code3 = self.translate_Stmt(stmt.children[6])
			return code1 + label1 + ':\n' + code2 + '  j '+ label3 + '\n' + label2 + ':\n' + code3 + label3 + ':\n'


	def translate_Cond(self, exp, label_true, label_false):
		if len(exp.children) == 2 and exp.children[0] == 'NOT':  # NOT Exp
			return self.translate_Cond(exp, label_false, label_true)

		elif len(exp.children) == 3 and exp.children[1] == 'AND':  # Exp AND Exp
			label1 = self.new_label()
			code1 = self.translate_Cond(exp.children[0], label1, label_false)
			code2 = self.translate_Cond(exp.children[2], label_true, label_false)
			return code1 + label1 + ':\n' + code2

		elif len(exp.children) == 3 and exp.children[1] == 'OR':  # Exp OR Exp
			label1 = self.new_label()
			code1 = self.translate_Cond(exp.children[0], label_true, label1)
			code2 = self.translate_Cond(exp.children[2], label_true, label_false)
			return code1 + label1 + '\n' + code2

		elif len(exp.children) == 3 and type(exp.children[1]) == list and exp.children[1][0] == 'RELOP':  # Exp RELOP Exp
			t0 = self.allocEmptyReg()
			t1 = self.allocEmptyReg()
			code1 = self.translate_Exp(exp.children[0], t0)
			code2 = self.translate_Exp(exp.children[2], t1)
			op = self.op_instr[exp.children[1][1]]
			code3 = '  ' + op + ' '+ t0 +', '+ t1 +', ' + label_true + '\n'
			return code1 + code2 + code3 + '  j ' + label_false + '\n'

		else:
			t0 = self.allocEmptyReg()
			t1 = self.allocEmptyReg()
			code1 = self.translate_Exp(exp, t0)
			code2 = '  li '+ t1 +', 0\n'
			code3 = '  bne '+ t0 +', '+ t1 +', ' + label_true + '\n'
			return code1 + code2 + code3 + '  j ' + label_false + '\n'


	def translate_Exp(self, exp, reg):
		"""
			Args:  exp(Node) -- Node of one Exp
				   reg(str) -- put the result of exp into reg, eg: '$t0'
			Return(str): code of this Exp
		"""
		if len(exp.children) == 1:   # 'ID'/'INT'
			t, v = exp.children[0][0], exp.children[0][1]  # t:'ID'/'INT', v:name or number
			if t == 'INT':
				return '  li ' + reg + ', ' + v + '\n'
			elif t == 'ID':
				t_bias = self.var_address_dict[v][0]
				return '  lw ' + reg + ', ' + str(t_bias) + '($sp)\n'
			else:
				print('wtf-1')

		elif len(exp.children) == 2: # 'MINUS Exp'/'NOT Exp'
			if exp.children[0] == 'MINUS':
				t0 = self.allocEmptyReg()
				t1 = self.allocEmptyReg()
				code1 = self.translate_Exp(exp.children[1], t0)
				code2 = '  li '+t1+', 0\n'
				code3 = '  sub ' + reg + ', '+t1+', '+t0+'\n'
				return code1 + code2 + code3

			elif exp.children[0] == 'NOT':
				label1 = self.new_label()
				label2 = self.new_label()
				code0 = '  li ' + reg + ', 0\n'
				code1 = self.translate_Cond(exp, label1, label2)
				code2 = label1 + ':\n' + '  li' + reg + ', 1\n'
				return code0 + code1 + code2 + label2 + ':\n'
			
			else:
				print('wtf-2')
			
		elif len(exp.children) == 3: # 'Exp op Exp'/'LP Exp RP'/'ID LP RP'/'Exp DOT ID'
			if exp.children[1] in ['PLUS', 'MINUS', 'STAR', 'DIV']:
				t0 = self.allocEmptyReg()
				t1 = self.allocEmptyReg()
				code1 = self.translate_Exp(exp.children[0], t0)
				code2 = self.translate_Exp(exp.children[2], t1)
				if exp.children[1] == 'PLUS':
					code3 = '  add ' + reg + ', ' + t0 + ', '+ t1 + '\n'
				elif exp.children[1] == 'MINUS':
					code3 = '  sub ' + reg + ', ' + t0 + ', '+ t1 + '\n'
				elif exp.children[1] == 'STAR':
					code3 = '  mul ' + reg + ', ' + t0 + ', '+ t1 + '\n'
				else:
					code3 = '  div ' + t0 + ', ' + t1 + '\n'
					code3 += '  mflo ' + reg + '\n'
				return code1 + code2 + code3

			elif exp.children[1] in ['AND', 'OR'] or (type(exp.children[1]) == list and exp.children[1][0] == 'RELOP'):
				t0 = self.allocEmptyReg()
				label1 = self.new_label()
				label2 = self.new_label()
				code0 = '  li '+ t0 +', 0\n'
				code1 = self.translate_Cond(exp, label1, label2)
				code2 = label1 + ':\n' + '  li' + reg + ', 1\n'
				return code0 + code1 + code2 + label2 + ':\n'

			elif exp.children[1] == 'ASSIGNOP':
				if type(exp.children[0])!=list and len(exp.children[0].children)!=1:        
					# exp1 is a node, it should be a struct member or a array member
					if 'DOT' in exp.children[0].children:  # it's a struct member
						print('Error! struct variable cannot be processed !!')
					elif 'LB' in exp.children[0].children: # it's a array member
						t0 = self.allocEmptyReg()
						t1 = self.allocEmptyReg()
						t2 = self.allocEmptyReg()
						code0 = self.translate_Exp(exp.children[2], t0)         # calculate exp2, put result into t0
						raw_list = []
						raw_list = self.getArrayList(exp.children[0], raw_list)
						array_name = raw_list[0]
						base_addr = self.var_address_dict[array_name][0]
						array_idx = raw_list[1]  # it can be a INT, ID or Node object(Exp)
						if type(array_idx) == str:  # INT/ID
							if array_idx.isdigit():   # INT
								bias = int(array_idx) * 4
								code1 = '  sw ' + t0 + ', ' + str(base_addr-bias) + '($sp)\n'
								return code0 + code1
							elif not array_idx.isdigit(): # ID
								bias = self.var_address_dict[array_idx][0]
								code1 = '  lw '+ t1 +', ' + str(bias) + '($sp)\n'  # $t1 <= id, t1 is positive !!
								code2 = '  li '+ t2 +', -4\n'
								code3 = '  mul '+t1+', '+t1+', '+t2+'\n'
								code4 = '  addi '+t1+', '+t1+', ' + str(base_addr) + '\n'
								code5 = '  add $sp, $sp, '+t1+'\n'
								code6 = '  sw '+t0+', 0($sp)\n' 
								code7 = '  sub $sp, $sp, '+t1+'\n'
								return code0 + code1 + code2 + code3 + code4 + code5 + code6 + code7
						else:
							code1 = self.translate_Exp(array_idx, t1)  # it's a positive number
							code2 = '  lt '+t2+', -4\n'
							code3 = '  mul '+t1+', '+t1+', '+t2+'\n'
							code4 = '  addi '+t1+', '+t1+', ' + str(base_addr) + '\n' # $t1 store total bias to $sp
							code5 = '  add $sp, $sp, '+t1+'\n'
							code6 = '  sw '+t0+', 0($sp)\n' 
							code7 = '  sub $sp, $sp, '+t1+'\n'
							return code0 + code1 + code2 + code3 + code4 + code5 + code6 + code7

					else:
						print('WTF! it\'s a node but it\'s not a struct nor a array !!')
				else:                                   # exp1 is a ID
					t0 = self.allocEmptyReg()
					exp1 = exp.children[0]
					t, v = exp1.children[0][0], exp1.children[0][1]
					exp1_addr_bias = self.var_address_dict[v][0]
					code1 = self.translate_Exp(exp.children[2], t0)
					code2 = '  sw '+t0+', ' + str(exp1_addr_bias) + '($sp)\n'
					code3 = '  move ' + reg + ', '+t0+'\n'
					rt_code = code1 + code2 + code3
					return rt_code

			elif exp.children[1] == 'LP' and exp.children[2] == 'RP': # ID LP RP
				self.function_param_reg_idx = -1
				func_name = exp.children[0][1]
				code1 = '  addi $sp, $sp, ' + str(self.var_bias) + '\n'
				code1_5 = ''
				# save $t0 - $t9
				for i in range(10):
					code1_5 += '  sw $t' + str(i) + ', 0($sp)\n'
					code1_5 += '  addi $sp, $sp, -4\n'
				code2 = '  sw $ra, 0($sp)\n'
				code2 += '  jal ' + func_name + '\n'
				code3 = '  lw $ra, 0($sp)\n'
				code3_5 = ''
				# recover $t0 - $t9
				for i in range(10)[::-1]:
					code3_5 += '  addi $sp, $sp, 4\n'
					code3_5 += '  lw $t' + str(i) + ', 0($sp)\n'
				code4 = '  addi $sp, $sp, ' + str(-self.var_bias) + '\n'
				code4 += '  move ' + reg + ', $v0\n'
				return code1 + code1_5 + code2 + code3 + code3_5 + code4

			elif exp.children[0] == 'LP' and exp.children[2] == 'RP': # LP Exp RP
				return self.translate_Exp(exp.children[1], reg)

			elif exp.children[1] == 'DOT':                            # Exp DOT ID
				print('Error! struct variable cannot be processed !!')

			else:
				print('wtf-3')

		elif len(exp.children) == 4:
			if exp.children[1] == 'LP' and exp.children[3] == 'RP':   # 'ID LP Args RP'
				self.function_param_reg_idx = -1
				func_name = exp.children[0][1]
				code0 = self.translate_Args(exp.children[2])
				code1 = '  addi $sp, $sp, ' + str(self.var_bias) + '\n'
				code1_5 = ''
				# save $t0 - $t9
				for i in range(10):
					code1_5 += '  sw $t' + str(i) + ', 0($sp)\n'
					code1_5 += '  addi $sp, $sp, -4\n'
				code2 = '  sw $ra, 0($sp)\n'
				code2 += '  jal ' + func_name + '\n'
				code3 = '  lw $ra, 0($sp)\n'
				code3_5 = ''
				# recover $t0 - $t9
				for i in range(10)[::-1]:
					code3_5 += '  addi $sp, $sp, 4\n'
					code3_5 += '  lw $t' + str(i) + ', 0($sp)\n'
				code4 = '  addi $sp, $sp, ' + str(-self.var_bias) + '\n'
				code4 += '  move ' + reg + ', $v0\n'
				return code0 + code1 + code1_5 + code2 + code3 + code3_5 + code4

			elif exp.children[1] == 'LB' and exp.children[3] == 'RB': # 'Exp LB Exp RB', must be 1-dimension here !!
				t0 = self.allocEmptyReg()
				t1 = self.allocEmptyReg()
				t2 = self.allocEmptyReg()
				raw_list = []
				raw_list = self.getArrayList(exp, raw_list)
				array_name = raw_list[0]
				base_addr = self.var_address_dict[array_name][0]   # it's a negative number !!
				array_idx = raw_list[1]  # it can be a INT, ID or Node object(Exp)
				if type(array_idx) == str:  # INT/ID
					if array_idx.isdigit():   # INT
						bias = int(array_idx) * 4                  # it's a positive number !!
						code1 = '  lw ' + reg + ', ' + str(base_addr-bias) + '($sp)\n'
						return code1
					elif not array_idx.isdigit(): # ID
						bias = self.var_address_dict[array_idx][0] # it's a negative number !!
						code1 = '  lw '+t0+', ' + str(bias) + '($sp)\n'  # $t0 <= id, t0 is positive !!
						code2 = '  li '+t1+', -4\n'
						code3 = '  mul '+t0+', '+t0+', '+t1+'\n'
						code4 = '  addi '+t0+', '+t0+', ' + str(base_addr) + '\n'
						code5 = '  add $sp, $sp, '+t0+'\n'
						code6 = '  lw ' + reg + ', 0($sp)\n' 
						code7 = '  sub $sp, $sp, '+t0+'\n'
						return code1 + code2 + code3 + code4 + code5 + code6 + code7
				else:
					code1 = self.translate_Exp(array_idx, t0)     # it's a positive number
					code2 = '  li '+t1+', -4\n'
					code3 = '  mul '+t0+', '+t0+', '+t1+'\n'
					code4 = '  addi '+t0+', '+t0+', ' + str(base_addr) + '\n' # $t1 store total bias to $sp
					code5 = '  add $sp, $sp, '+t0+'\n'
					code6 = '  lw ' + reg + ', 0($sp)\n' 
					code7 = '  sub $sp, $sp, '+t0+'\n'
					return code1 + code2 + code3 + code4 + code5 + code6 + code7

			else:
				print('wtf-4')

		else:
			print('wtf-others')


	def translate_Args(self, args):
		"""
			type of args_list is list
			args can a variable or a expression

			Args : Exp COMMA Args
				 | Exp
		"""	
		if len(args.children) == 1:    # Exp
			code1 = self.translate_Exp(args.children[0], self.allocFuncParamReg())
			return code1
			
		elif len(args.children) == 3:  # Exp COMMA Args
			code1 = self.translate_Exp(args.children[0], self.allocFuncParamReg())
			code2 = self.translate_Args(args.children[2])
			return code1 + code2


	def getArrayList(self, exp, raw_list):
		"""
			get a Exp Node and return its raw_list
			eg: Exp(a[i][0][j]) => ['a', 'i', '0', 'j']
				Exp(a[i+j-1])   => ['a', Node object]

			Exp : Exp LB Exp RB

			use pre-Order traversal
		"""
		if exp == None:
			return raw_list
		elif type(exp) == str:
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
				self.getArrayList(sub_exp, raw_list)
			return raw_list
