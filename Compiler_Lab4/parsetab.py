
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightASSIGNOPleftORleftANDleftRELOPleftPLUSMINUSleftSTARDIVrightNOTleftDOTLBRBLPRPnonassocif_thennonassocELSEnonassocSTRUCTRETURNWHILEINT FLOAT ID SEMI COMMA ASSIGNOP RELOP PLUS MINUS STAR DIV AND OR DOT NOT LP RP LB RB LC RC WHILE IF RETURN ELSE TYPE STRUCTProgram : ExtDefListExtDefList\t: ExtDef ExtDefList\n\t           \t\t| emptyExtDef\t:\tSpecifier SEMIExtDef :\tSpecifier FunDec CompStExtDef : Specifier FunDec SEMIExtDef\t:\tSpecifier ExtDecList SEMIExtDecList : VarDecExtDecList : VarDec COMMA ExtDecList\t Specifier : TYPESpecifier : StructSpecifierStructSpecifier : STRUCT OptTag LC DefList RCStructSpecifier : STRUCT TagOptTag : IDOptTag : emptyTag :\tIDVarDec : IDVarDec : VarDec LB INT RBFunDec : ID LP VarList RPFunDec : ID LP RPVarList : ParamDec COMMA VarListVarList : ParamDecParamDec\t:\tSpecifier VarDecCompSt\t: LC DefList StmtList RCStmtList\t: Stmt StmtList\n\t            | emptyStmt :\tExp SEMIStmt : CompStStmt : IF LP Exp RP Stmt %prec if_thenStmt : WHILE LP Exp RP StmtStmt : IF LP Exp RP Stmt ELSE StmtStmt : RETURN Exp SEMIDefList\t: Def DefList \n\t            | emptyDef : Specifier DecList SEMIDecList\t:\tDecDecList\t: Dec COMMA DecListDec\t:\tVarDecDec\t: VarDec ASSIGNOP Exp Exp : Exp ASSIGNOP ExpExp : Exp AND ExpExp : Exp OR ExpExp : Exp RELOP ExpExp : Exp PLUS ExpExp : Exp MINUS ExpExp : Exp STAR ExpExp : Exp DIV ExpExp : LP Exp RPExp : MINUS ExpExp : NOT ExpExp : ID LP Args RPExp : ID LP RPExp : Exp LB Exp RBExp : Exp DOT IDExp : IDExp : INTExp : FLOATArgs : Exp COMMA ArgsArgs : Expempty :ExtDef : error SEMIFunDec : error RPCompSt : error RCStmt : error SEMIDef : Specifier error SEMI'
    
_lr_action_items = {'INT':([25,27,36,37,38,39,53,54,55,59,61,62,65,70,72,73,74,75,78,79,80,81,82,83,84,86,87,88,89,90,92,114,115,116,118,120,122,123,124,],[34,-60,50,-60,-34,-63,50,50,-28,50,50,50,-33,-65,-35,50,50,-24,50,50,50,50,50,50,50,-27,50,50,50,50,-64,-32,50,50,50,-29,-30,50,-31,]),'IF':([27,36,37,38,39,55,61,65,70,72,75,86,92,114,115,118,120,122,123,124,],[-60,51,-60,-34,-63,-28,51,-33,-65,-35,-24,-27,-64,-32,51,51,-29,-30,51,-31,]),'ELSE':([39,55,75,86,92,114,120,122,124,],[-63,-28,-24,-27,-64,-32,123,-30,-31,]),'LC':([7,14,17,19,20,22,27,36,37,38,39,40,55,61,65,68,70,72,75,86,92,114,115,118,120,122,123,124,],[-60,27,-14,31,-15,-62,-60,27,-60,-34,-63,-20,-28,27,-33,-19,-65,-35,-24,-27,-64,-32,27,27,-29,-30,27,-31,]),'LP':([15,27,36,37,38,39,51,53,54,55,56,57,59,61,62,65,70,72,73,74,75,78,79,80,81,82,83,84,86,87,88,89,90,92,114,115,116,118,120,122,123,124,],[30,-60,53,-60,-34,-63,74,53,53,-28,78,79,53,53,53,-33,-65,-35,53,53,-24,53,53,53,53,53,53,53,-27,53,53,53,53,-64,-32,53,53,53,-29,-30,53,-31,]),'TYPE':([0,9,12,16,23,26,27,28,30,31,37,39,67,70,72,75,],[5,5,-4,-61,-7,-5,5,-6,5,5,5,-63,5,-65,-35,-24,]),'DOT':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,85,-57,85,85,85,85,85,85,-48,-52,85,85,85,85,85,85,85,-54,85,85,85,85,-51,-53,]),'OR':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,88,-57,88,-50,88,-49,88,88,-48,-52,88,88,88,88,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,]),'RC':([27,29,31,36,37,38,39,44,52,55,60,61,63,65,70,72,75,86,92,93,114,120,122,124,],[-60,39,-60,-60,-60,-34,-63,69,75,-28,39,-60,-26,-33,-65,-35,-24,-27,-64,-25,-32,-29,-30,-31,]),'RB':([34,50,56,64,77,94,99,100,104,105,106,107,108,109,110,111,112,113,117,119,],[45,-56,-55,-57,-50,-49,-48,-52,-40,119,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,]),'ID':([1,3,5,7,17,18,24,27,35,36,37,38,39,41,53,54,55,59,61,62,65,69,70,71,72,73,74,75,78,79,80,81,82,83,84,85,86,87,88,89,90,92,114,115,116,118,120,122,123,124,],[15,-11,-10,17,-16,-13,32,-60,32,56,-60,-34,-63,32,56,56,-28,56,56,56,-33,-12,-65,32,-35,56,56,-24,56,56,56,56,56,56,56,109,-27,56,56,56,56,-64,-32,56,56,56,-29,-30,56,-31,]),'RETURN':([27,36,37,38,39,55,61,65,70,72,75,86,92,114,115,118,120,122,123,124,],[-60,59,-60,-34,-63,-28,59,-33,-65,-35,-24,-27,-64,-32,59,59,-29,-30,59,-31,]),'DIV':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,89,-57,89,-50,89,89,89,89,-48,-52,89,89,89,89,89,89,89,-54,89,89,-47,-46,-51,-53,]),'ASSIGNOP':([32,45,49,50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-17,-18,73,-56,-55,80,-57,80,-50,80,-49,80,80,-48,-52,80,80,80,80,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,]),'RP':([10,30,32,42,43,45,50,56,64,66,76,77,78,94,95,98,99,100,101,102,103,104,106,107,108,109,110,111,112,113,117,119,121,],[22,40,-17,-22,68,-18,-56,-55,-57,-23,99,-50,100,-49,-21,115,-48,-52,-59,117,118,-40,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,-58,]),'WHILE':([27,36,37,38,39,55,61,65,70,72,75,86,92,114,115,118,120,122,123,124,],[-60,57,-60,-34,-63,-28,57,-33,-65,-35,-24,-27,-64,-32,57,57,-29,-30,57,-31,]),'error':([0,1,3,5,9,12,14,16,17,18,22,23,26,27,28,35,36,37,38,39,40,55,61,65,68,69,70,72,75,86,92,114,115,118,120,122,123,124,],[2,10,-11,-10,2,-4,29,-61,-16,-13,-62,-7,-5,-60,-6,46,60,-60,-34,-63,-20,-28,60,-33,-19,-12,-65,-35,-24,-27,-64,-32,60,60,-29,-30,60,-31,]),'LB':([13,15,32,45,49,50,56,58,64,66,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[25,-17,-17,-18,25,-56,-55,81,-57,25,81,81,81,81,81,81,-48,-52,81,81,81,81,81,81,81,-54,81,81,81,81,-51,-53,]),'PLUS':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,82,-57,82,-50,82,-49,82,82,-48,-52,82,82,82,82,-44,-45,82,-54,82,82,-47,-46,-51,-53,]),'SEMI':([1,2,3,5,11,13,14,15,17,18,22,32,33,40,45,46,47,48,49,50,56,58,60,64,68,69,77,91,94,96,97,99,100,104,106,107,108,109,110,111,112,113,117,119,],[12,16,-11,-10,23,-8,28,-17,-16,-13,-62,-17,-9,-20,-18,70,-36,72,-38,-56,-55,86,92,-57,-19,-12,-50,114,-49,-37,-39,-48,-52,-40,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,]),'AND':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,84,-57,84,-50,84,-49,84,84,-48,-52,84,84,84,84,-44,-45,-41,-54,-43,84,-47,-46,-51,-53,]),'$end':([0,4,6,8,9,12,16,21,23,26,28,39,75,],[-60,-1,0,-3,-60,-4,-61,-2,-7,-5,-6,-63,-24,]),'COMMA':([13,15,32,42,45,47,49,50,56,64,66,77,94,97,99,100,101,104,106,107,108,109,110,111,112,113,117,119,],[24,-17,-17,67,-18,71,-38,-56,-55,-57,-23,-50,-49,-39,-48,-52,116,-40,-44,-45,-41,-54,-43,-42,-47,-46,-51,-53,]),'NOT':([27,36,37,38,39,53,54,55,59,61,62,65,70,72,73,74,75,78,79,80,81,82,83,84,86,87,88,89,90,92,114,115,116,118,120,122,123,124,],[-60,54,-60,-34,-63,54,54,-28,54,54,54,-33,-65,-35,54,54,-24,54,54,54,54,54,54,54,-27,54,54,54,54,-64,-32,54,54,54,-29,-30,54,-31,]),'MINUS':([27,36,37,38,39,50,53,54,55,56,58,59,61,62,64,65,70,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,123,124,],[-60,62,-60,-34,-63,-56,62,62,-28,-55,83,62,62,62,-57,-33,-65,-35,62,62,-24,83,-50,62,62,62,62,62,62,62,-27,62,62,62,62,83,-64,-49,83,83,-48,-52,83,83,83,83,-44,-45,83,-54,83,83,-47,-46,-32,62,62,-51,62,-53,-29,-30,62,-31,]),'STRUCT':([0,9,12,16,23,26,27,28,30,31,37,39,67,70,72,75,],[7,7,-4,-61,-7,-5,7,-6,7,7,7,-63,7,-65,-35,-24,]),'STAR':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,90,-57,90,-50,90,90,90,90,-48,-52,90,90,90,90,90,90,90,-54,90,90,-47,-46,-51,-53,]),'FLOAT':([27,36,37,38,39,53,54,55,59,61,62,65,70,72,73,74,75,78,79,80,81,82,83,84,86,87,88,89,90,92,114,115,116,118,120,122,123,124,],[-60,64,-60,-34,-63,64,64,-28,64,64,64,-33,-65,-35,64,64,-24,64,64,64,64,64,64,64,-27,64,64,64,64,-64,-32,64,64,64,-29,-30,64,-31,]),'RELOP':([50,56,58,64,76,77,91,94,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,117,119,],[-56,-55,87,-57,87,-50,87,-49,87,87,-48,-52,87,87,87,87,-44,-45,87,-54,-43,87,-47,-46,-51,-53,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'StmtList':([36,61,],[52,93,]),'ParamDec':([30,67,],[42,42,]),'ExtDecList':([1,24,],[11,33,]),'Dec':([35,71,],[47,47,]),'CompSt':([14,36,61,115,118,123,],[26,55,55,55,55,55,]),'FunDec':([1,],[14,]),'Args':([78,116,],[102,121,]),'DefList':([27,31,37,],[36,44,65,]),'Exp':([36,53,54,59,61,62,73,74,78,79,80,81,82,83,84,87,88,89,90,115,116,118,123,],[58,76,77,91,58,94,97,98,101,103,104,105,106,107,108,110,111,112,113,58,101,58,58,]),'Specifier':([0,9,27,30,31,37,67,],[1,1,35,41,35,35,41,]),'DecList':([35,71,],[48,96,]),'Stmt':([36,61,115,118,123,],[61,61,120,122,124,]),'VarDec':([1,24,35,41,71,],[13,13,49,66,49,]),'Def':([27,31,37,],[37,37,37,]),'StructSpecifier':([0,9,27,30,31,37,67,],[3,3,3,3,3,3,3,]),'ExtDefList':([0,9,],[4,21,]),'OptTag':([7,],[19,]),'Program':([0,],[6,]),'Tag':([7,],[18,]),'VarList':([30,67,],[43,95,]),'empty':([0,7,9,27,31,36,37,61,],[8,20,8,38,38,63,38,63,]),'ExtDef':([0,9,],[9,9,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> ExtDefList','Program',1,'p_program','lab4.py',267),
  ('ExtDefList -> ExtDef ExtDefList','ExtDefList',2,'p_extdeflist','lab4.py',273),
  ('ExtDefList -> empty','ExtDefList',1,'p_extdeflist','lab4.py',274),
  ('ExtDef -> Specifier SEMI','ExtDef',2,'p_extdef_1','lab4.py',282),
  ('ExtDef -> Specifier FunDec CompSt','ExtDef',3,'p_extdef_2','lab4.py',300),
  ('ExtDef -> Specifier FunDec SEMI','ExtDef',3,'p_extdef_funcDec','lab4.py',321),
  ('ExtDef -> Specifier ExtDecList SEMI','ExtDef',3,'p_extdef_3','lab4.py',332),
  ('ExtDecList -> VarDec','ExtDecList',1,'p_extdeclist_1','lab4.py',373),
  ('ExtDecList -> VarDec COMMA ExtDecList','ExtDecList',3,'p_extdeclist_2','lab4.py',377),
  ('Specifier -> TYPE','Specifier',1,'p_specifier_TYPE','lab4.py',383),
  ('Specifier -> StructSpecifier','Specifier',1,'p_specifier_structspecifier','lab4.py',388),
  ('StructSpecifier -> STRUCT OptTag LC DefList RC','StructSpecifier',5,'p_structspecifier_1','lab4.py',394),
  ('StructSpecifier -> STRUCT Tag','StructSpecifier',2,'p_structspecifier_2','lab4.py',398),
  ('OptTag -> ID','OptTag',1,'p_opttag_ID','lab4.py',404),
  ('OptTag -> empty','OptTag',1,'p_opttag_empty','lab4.py',408),
  ('Tag -> ID','Tag',1,'p_tag','lab4.py',413),
  ('VarDec -> ID','VarDec',1,'p_vardec_ID','lab4.py',419),
  ('VarDec -> VarDec LB INT RB','VarDec',4,'p_vardec_vardeclbintrb','lab4.py',424),
  ('FunDec -> ID LP VarList RP','FunDec',4,'p_fundec_1','lab4.py',430),
  ('FunDec -> ID LP RP','FunDec',3,'p_fundec_2','lab4.py',434),
  ('VarList -> ParamDec COMMA VarList','VarList',3,'p_varlist_1','lab4.py',440),
  ('VarList -> ParamDec','VarList',1,'p_varlist_2','lab4.py',444),
  ('ParamDec -> Specifier VarDec','ParamDec',2,'p_paramdec','lab4.py',450),
  ('CompSt -> LC DefList StmtList RC','CompSt',4,'p_compst','lab4.py',456),
  ('StmtList -> Stmt StmtList','StmtList',2,'p_stmtlist','lab4.py',462),
  ('StmtList -> empty','StmtList',1,'p_stmtlist','lab4.py',463),
  ('Stmt -> Exp SEMI','Stmt',2,'p_stmt_1','lab4.py',472),
  ('Stmt -> CompSt','Stmt',1,'p_stmt_2','lab4.py',476),
  ('Stmt -> IF LP Exp RP Stmt','Stmt',5,'p_stmt_3','lab4.py',480),
  ('Stmt -> WHILE LP Exp RP Stmt','Stmt',5,'p_stmt_4','lab4.py',484),
  ('Stmt -> IF LP Exp RP Stmt ELSE Stmt','Stmt',7,'p_stmt_5','lab4.py',488),
  ('Stmt -> RETURN Exp SEMI','Stmt',3,'p_stmt_6','lab4.py',492),
  ('DefList -> Def DefList','DefList',2,'p_deflist','lab4.py',498),
  ('DefList -> empty','DefList',1,'p_deflist','lab4.py',499),
  ('Def -> Specifier DecList SEMI','Def',3,'p_def','lab4.py',508),
  ('DecList -> Dec','DecList',1,'p_declist_1','lab4.py',518),
  ('DecList -> Dec COMMA DecList','DecList',3,'p_declist_2','lab4.py',522),
  ('Dec -> VarDec','Dec',1,'p_dec_1','lab4.py',527),
  ('Dec -> VarDec ASSIGNOP Exp','Dec',3,'p_dec_2','lab4.py',531),
  ('Exp -> Exp ASSIGNOP Exp','Exp',3,'p_exp_ASSIGNOP','lab4.py',537),
  ('Exp -> Exp AND Exp','Exp',3,'p_exp_AND','lab4.py',541),
  ('Exp -> Exp OR Exp','Exp',3,'p_exp_OR','lab4.py',545),
  ('Exp -> Exp RELOP Exp','Exp',3,'p_exp_RELOP','lab4.py',549),
  ('Exp -> Exp PLUS Exp','Exp',3,'p_exp_PLUS','lab4.py',553),
  ('Exp -> Exp MINUS Exp','Exp',3,'p_exp_MINUS','lab4.py',557),
  ('Exp -> Exp STAR Exp','Exp',3,'p_exp_STAR','lab4.py',561),
  ('Exp -> Exp DIV Exp','Exp',3,'p_exp_DIV','lab4.py',565),
  ('Exp -> LP Exp RP','Exp',3,'p_exp_LPRP','lab4.py',569),
  ('Exp -> MINUS Exp','Exp',2,'p_exp_MINUS_2','lab4.py',573),
  ('Exp -> NOT Exp','Exp',2,'p_exp_NOT','lab4.py',577),
  ('Exp -> ID LP Args RP','Exp',4,'p_exp_IDLPRP','lab4.py',581),
  ('Exp -> ID LP RP','Exp',3,'p_exp_IDLPRP2','lab4.py',585),
  ('Exp -> Exp LB Exp RB','Exp',4,'p_exp_LBRB','lab4.py',589),
  ('Exp -> Exp DOT ID','Exp',3,'p_exp_DOTID','lab4.py',593),
  ('Exp -> ID','Exp',1,'p_exp_ID','lab4.py',597),
  ('Exp -> INT','Exp',1,'p_exp_INT','lab4.py',601),
  ('Exp -> FLOAT','Exp',1,'p_exp_FLOAT','lab4.py',605),
  ('Args -> Exp COMMA Args','Args',3,'p_args_1','lab4.py',611),
  ('Args -> Exp','Args',1,'p_args_2','lab4.py',615),
  ('empty -> <empty>','empty',0,'p_empty','lab4.py',621),
  ('ExtDef -> error SEMI','ExtDef',2,'p_extdef_error','lab4.py',643),
  ('FunDec -> error RP','FunDec',2,'p_fundec_error','lab4.py',647),
  ('CompSt -> error RC','CompSt',2,'p_compst_error','lab4.py',651),
  ('Stmt -> error SEMI','Stmt',2,'p_stmt_error','lab4.py',655),
  ('Def -> Specifier error SEMI','Def',3,'p_def_error','lab4.py',659),
]