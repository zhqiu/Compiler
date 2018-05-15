
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightASSIGNOPleftORleftANDleftRELOPleftPLUSMINUSleftSTARDIVrightNOTleftDOTLBRBLPRPnonassocif_thennonassocELSEnonassocSTRUCTRETURNWHILEINT FLOAT ID SEMI COMMA ASSIGNOP RELOP PLUS MINUS STAR DIV AND OR DOT NOT LP RP LB RB LC RC IF WHILE STRUCT TYPE ELSE RETURNProgram : ExtDefListExtDefList\t: ExtDef ExtDefList\n\t           \t\t| emptyExtDef\t:\tSpecifier SEMIExtDef :\tSpecifier FunDec CompStExtDef\t:\tSpecifier ExtDecList SEMIExtDecList : VarDecExtDecList : VarDec COMMA ExtDecList\t Specifier : TYPESpecifier : StructSpecifierStructSpecifier : STRUCT OptTag LC DefList RCStructSpecifier : STRUCT TagOptTag : IDOptTag : emptyTag :\tIDVarDec : IDVarDec : VarDec LB INT RBFunDec : ID LP VarList RPFunDec : ID LP RPVarList : ParamDec COMMA VarListVarList : ParamDecParamDec\t:\tSpecifier VarDecCompSt\t: LC DefList StmtList RCStmtList\t: Stmt StmtList\n\t            | emptyStmt :\tExp SEMIStmt : CompStStmt : IF LP Exp RP Stmt %prec if_thenStmt : WHILE LP Exp RP StmtStmt : IF LP Exp RP Stmt ELSE StmtStmt : RETURN Exp SEMIDefList\t: Def DefList \n\t            | emptyDef : Specifier DecList SEMIDecList\t:\tDecDecList\t: Dec COMMA DecListDec\t:\tVarDecDec\t: VarDec ASSIGNOP Exp Exp : Exp ASSIGNOP ExpExp : Exp AND ExpExp : Exp OR ExpExp : Exp RELOP ExpExp : Exp PLUS ExpExp : Exp MINUS ExpExp : Exp STAR ExpExp : Exp DIV ExpExp : LP Exp RPExp : MINUS ExpExp : NOT ExpExp : ID LP Args RPExp : ID LP RPExp : Exp LB Exp RBExp : Exp DOT IDExp : IDExp : INTExp : FLOATArgs : Exp COMMA ArgsArgs : Expempty :ExtDef : error SEMIFunDec : error RPCompSt : error RCStmt : error SEMIDef : Specifier error SEMI'
    
_lr_action_items = {'IF':([27,39,40,41,42,52,57,67,70,72,75,76,83,102,114,115,119,120,122,123,],[-59,-33,-59,53,-62,-32,-27,53,-34,-64,-23,-63,-26,-31,53,53,-28,-29,53,-30,]),'RC':([27,29,30,39,40,41,42,43,52,54,56,57,58,67,70,72,75,76,83,94,102,119,120,123,],[-59,42,-59,-33,-59,-59,-62,68,-32,75,-25,-27,42,-59,-34,-64,-23,-63,-26,-24,-31,-28,-29,-30,]),'TYPE':([0,8,10,21,22,26,27,28,30,40,42,46,70,72,75,],[7,7,-4,-60,-6,7,7,-5,7,7,-62,7,-34,-64,-23,]),'PLUS':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,81,-49,81,-48,81,81,81,81,81,-51,-43,-45,81,81,81,81,81,-46,-53,-44,-47,-50,-52,]),'SEMI':([1,5,7,9,11,12,14,18,19,32,33,44,48,49,50,51,55,58,60,61,64,68,79,80,92,95,96,101,103,104,105,106,107,108,110,111,112,113,116,118,],[10,-10,-9,21,22,-7,-16,-15,-12,-8,-16,-17,70,-37,72,-35,-55,76,-54,-56,83,-11,-49,102,-48,-38,-36,-51,-43,-45,-42,-41,-40,-39,-46,-53,-44,-47,-50,-52,]),'MINUS':([27,39,40,41,42,52,55,57,60,61,62,63,64,65,66,67,70,71,72,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,91,92,93,95,97,98,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,122,123,],[-59,-33,-59,65,-62,-32,-55,-27,-54,-56,65,65,91,65,65,65,-34,65,-64,65,-23,-63,65,65,-49,91,65,65,-26,65,65,65,65,65,65,65,-48,91,91,91,91,91,-51,-31,-43,-45,91,91,91,91,91,-46,-53,-44,-47,65,65,-50,65,-52,-28,-29,65,-30,]),'ASSIGNOP':([33,44,49,55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-16,-17,71,-55,-54,-56,87,-49,87,-48,87,87,87,87,87,-51,-43,-45,-42,-41,-40,87,87,-46,-53,-44,-47,-50,-52,]),'error':([0,1,5,7,8,10,15,18,19,21,22,25,27,28,35,38,39,40,41,42,47,52,57,67,68,70,72,75,76,83,102,114,115,119,120,122,123,],[9,13,-10,-9,9,-4,29,-15,-12,-60,-6,-61,-59,-5,-19,50,-33,-59,58,-62,-18,-32,-27,58,-11,-34,-64,-23,-63,-26,-31,58,58,-28,-29,58,-30,]),'WHILE':([27,39,40,41,42,52,57,67,70,72,75,76,83,102,114,115,119,120,122,123,],[-59,-33,-59,59,-62,-32,-27,59,-34,-64,-23,-63,-26,-31,59,59,-28,-29,59,-30,]),'STAR':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,82,-49,82,82,82,82,82,82,82,-51,82,-45,82,82,82,82,82,-46,-53,82,-47,-50,-52,]),'ELSE':([42,57,75,76,83,102,119,120,123,],[-62,-27,-23,-63,-26,-31,122,-29,-30,]),'LP':([14,27,39,40,41,42,52,53,57,59,60,62,63,65,66,67,70,71,72,74,75,76,77,78,81,82,83,84,85,86,87,88,89,91,102,114,115,117,119,120,122,123,],[26,-59,-33,-59,66,-62,-32,74,-27,77,78,66,66,66,66,66,-34,66,-64,66,-23,-63,66,66,66,66,-26,66,66,66,66,66,66,66,-31,66,66,66,-28,-29,66,-30,]),'COMMA':([12,14,33,36,44,45,49,51,55,60,61,79,92,95,100,101,103,104,105,106,107,108,110,111,112,113,116,118,],[24,-16,-16,46,-17,-22,-37,73,-55,-54,-56,-49,-48,-38,117,-51,-43,-45,-42,-41,-40,-39,-46,-53,-44,-47,-50,-52,]),'NOT':([27,39,40,41,42,52,57,62,63,65,66,67,70,71,72,74,75,76,77,78,81,82,83,84,85,86,87,88,89,91,102,114,115,117,119,120,122,123,],[-59,-33,-59,62,-62,-32,-27,62,62,62,62,62,-34,62,-64,62,-23,-63,62,62,62,62,-26,62,62,62,62,62,62,62,-31,62,62,62,-28,-29,62,-30,]),'DIV':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,89,-49,89,89,89,89,89,89,89,-51,89,-45,89,89,89,89,89,-46,-53,89,-47,-50,-52,]),'DOT':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,90,90,90,90,90,90,90,90,90,-51,90,90,90,90,90,90,90,90,-53,90,-47,-50,-52,]),'RETURN':([27,39,40,41,42,52,57,67,70,72,75,76,83,102,114,115,119,120,122,123,],[-59,-33,-59,63,-62,-32,-27,63,-34,-64,-23,-63,-26,-31,63,63,-28,-29,63,-30,]),'LB':([12,14,33,44,45,49,55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[23,-16,-16,-17,23,23,-55,-54,-56,88,88,88,88,88,88,88,88,88,-51,88,88,88,88,88,88,88,88,-53,88,-47,-50,-52,]),'AND':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,86,-49,86,-48,86,86,86,86,86,-51,-43,-45,-42,86,-40,86,86,-46,-53,-44,-47,-50,-52,]),'RELOP':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,84,-49,84,-48,84,84,84,84,84,-51,-43,-45,-42,84,84,84,84,-46,-53,-44,-47,-50,-52,]),'LC':([3,15,16,17,18,25,27,35,39,40,41,42,47,52,57,67,70,72,75,76,83,102,114,115,119,120,122,123,],[-59,27,-14,30,-13,-61,-59,-19,-33,-59,27,-62,-18,-32,-27,27,-34,-64,-23,-63,-26,-31,27,27,-28,-29,27,-30,]),'OR':([55,60,61,64,79,80,92,93,95,97,98,100,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[-55,-54,-56,85,-49,85,-48,85,85,85,85,85,-51,-43,-45,-42,-41,-40,85,85,-46,-53,-44,-47,-50,-52,]),'INT':([23,27,39,40,41,42,52,57,62,63,65,66,67,70,71,72,74,75,76,77,78,81,82,83,84,85,86,87,88,89,91,102,114,115,117,119,120,122,123,],[31,-59,-33,-59,55,-62,-32,-27,55,55,55,55,55,-34,55,-64,55,-23,-63,55,55,55,55,-26,55,55,55,55,55,55,55,-31,55,55,55,-28,-29,55,-30,]),'$end':([0,2,4,6,8,10,20,21,22,28,42,75,],[-59,-3,0,-1,-59,-4,-2,-60,-6,-5,-62,-23,]),'STRUCT':([0,8,10,21,22,26,27,28,30,40,42,46,70,72,75,],[3,3,-4,-60,-6,3,3,-5,3,3,-62,3,-34,-64,-23,]),'RB':([31,55,60,61,79,92,101,103,104,105,106,107,108,109,110,111,112,113,116,118,],[44,-55,-54,-56,-49,-48,-51,-43,-45,-42,-41,-40,-39,118,-46,-53,-44,-47,-50,-52,]),'ID':([1,3,5,7,18,19,24,27,34,38,39,40,41,42,52,57,62,63,65,66,67,68,70,71,72,73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,102,114,115,117,119,120,122,123,],[14,18,-10,-9,-15,-12,33,-59,33,33,-33,-59,60,-62,-32,-27,60,60,60,60,60,-11,-34,60,-64,33,60,-23,-63,60,60,60,60,-26,60,60,60,60,60,60,111,60,-31,60,60,60,-28,-29,60,-30,]),'RP':([13,26,33,36,37,44,45,55,60,61,69,78,79,92,93,97,98,99,100,101,103,104,105,106,107,108,110,111,112,113,116,118,121,],[25,35,-16,-21,47,-17,-22,-55,-54,-56,-20,101,-49,-48,113,114,115,116,-58,-51,-43,-45,-42,-41,-40,-39,-46,-53,-44,-47,-50,-52,-57,]),'FLOAT':([27,39,40,41,42,52,57,62,63,65,66,67,70,71,72,74,75,76,77,78,81,82,83,84,85,86,87,88,89,91,102,114,115,117,119,120,122,123,],[-59,-33,-59,61,-62,-32,-27,61,61,61,61,61,-34,61,-64,61,-23,-63,61,61,61,61,-26,61,61,61,61,61,61,61,-31,61,61,61,-28,-29,61,-30,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'StmtList':([41,67,],[54,94,]),'empty':([0,3,8,27,30,40,41,67,],[2,16,2,39,39,39,56,56,]),'Args':([78,117,],[99,121,]),'CompSt':([15,41,67,114,115,122,],[28,57,57,57,57,57,]),'Specifier':([0,8,26,27,30,40,46,],[1,1,34,38,38,38,34,]),'FunDec':([1,],[15,]),'Tag':([3,],[19,]),'StructSpecifier':([0,8,26,27,30,40,46,],[5,5,5,5,5,5,5,]),'ExtDef':([0,8,],[8,8,]),'DefList':([27,30,40,],[41,43,52,]),'Exp':([41,62,63,65,66,67,71,74,77,78,81,82,84,85,86,87,88,89,91,114,115,117,122,],[64,79,80,92,93,64,95,97,98,100,103,104,105,106,107,108,109,110,112,64,64,100,64,]),'ParamDec':([26,46,],[36,36,]),'ExtDecList':([1,24,],[11,32,]),'VarDec':([1,24,34,38,73,],[12,12,45,49,49,]),'Program':([0,],[4,]),'ExtDefList':([0,8,],[6,20,]),'Stmt':([41,67,114,115,122,],[67,67,119,120,123,]),'DecList':([38,73,],[48,96,]),'Def':([27,30,40,],[40,40,40,]),'OptTag':([3,],[17,]),'Dec':([38,73,],[51,51,]),'VarList':([26,46,],[37,69,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Program","S'",1,None,None,None),
  ('Program -> ExtDefList','Program',1,'p_program','lab1.py',260),
  ('ExtDefList -> ExtDef ExtDefList','ExtDefList',2,'p_extdeflist','lab1.py',266),
  ('ExtDefList -> empty','ExtDefList',1,'p_extdeflist','lab1.py',267),
  ('ExtDef -> Specifier SEMI','ExtDef',2,'p_extdef_1','lab1.py',275),
  ('ExtDef -> Specifier FunDec CompSt','ExtDef',3,'p_extdef_2','lab1.py',279),
  ('ExtDef -> Specifier ExtDecList SEMI','ExtDef',3,'p_extdef_3','lab1.py',283),
  ('ExtDecList -> VarDec','ExtDecList',1,'p_extdeclist_1','lab1.py',289),
  ('ExtDecList -> VarDec COMMA ExtDecList','ExtDecList',3,'p_extdeclist_2','lab1.py',293),
  ('Specifier -> TYPE','Specifier',1,'p_specifier_TYPE','lab1.py',299),
  ('Specifier -> StructSpecifier','Specifier',1,'p_specifier_structspecifier','lab1.py',304),
  ('StructSpecifier -> STRUCT OptTag LC DefList RC','StructSpecifier',5,'p_structspecifier_1','lab1.py',310),
  ('StructSpecifier -> STRUCT Tag','StructSpecifier',2,'p_structspecifier_2','lab1.py',314),
  ('OptTag -> ID','OptTag',1,'p_opttag_ID','lab1.py',320),
  ('OptTag -> empty','OptTag',1,'p_opttag_empty','lab1.py',324),
  ('Tag -> ID','Tag',1,'p_tag','lab1.py',329),
  ('VarDec -> ID','VarDec',1,'p_vardec_ID','lab1.py',335),
  ('VarDec -> VarDec LB INT RB','VarDec',4,'p_vardec_vardeclbintrb','lab1.py',340),
  ('FunDec -> ID LP VarList RP','FunDec',4,'p_fundec_1','lab1.py',346),
  ('FunDec -> ID LP RP','FunDec',3,'p_fundec_2','lab1.py',350),
  ('VarList -> ParamDec COMMA VarList','VarList',3,'p_varlist_1','lab1.py',356),
  ('VarList -> ParamDec','VarList',1,'p_varlist_2','lab1.py',360),
  ('ParamDec -> Specifier VarDec','ParamDec',2,'p_paramdec','lab1.py',366),
  ('CompSt -> LC DefList StmtList RC','CompSt',4,'p_compst','lab1.py',372),
  ('StmtList -> Stmt StmtList','StmtList',2,'p_stmtlist','lab1.py',378),
  ('StmtList -> empty','StmtList',1,'p_stmtlist','lab1.py',379),
  ('Stmt -> Exp SEMI','Stmt',2,'p_stmt_1','lab1.py',388),
  ('Stmt -> CompSt','Stmt',1,'p_stmt_2','lab1.py',392),
  ('Stmt -> IF LP Exp RP Stmt','Stmt',5,'p_stmt_3','lab1.py',397),
  ('Stmt -> WHILE LP Exp RP Stmt','Stmt',5,'p_stmt_4','lab1.py',402),
  ('Stmt -> IF LP Exp RP Stmt ELSE Stmt','Stmt',7,'p_stmt_5','lab1.py',406),
  ('Stmt -> RETURN Exp SEMI','Stmt',3,'p_stmt_6','lab1.py',410),
  ('DefList -> Def DefList','DefList',2,'p_deflist','lab1.py',416),
  ('DefList -> empty','DefList',1,'p_deflist','lab1.py',417),
  ('Def -> Specifier DecList SEMI','Def',3,'p_def','lab1.py',426),
  ('DecList -> Dec','DecList',1,'p_declist_1','lab1.py',432),
  ('DecList -> Dec COMMA DecList','DecList',3,'p_declist_2','lab1.py',436),
  ('Dec -> VarDec','Dec',1,'p_dec_1','lab1.py',441),
  ('Dec -> VarDec ASSIGNOP Exp','Dec',3,'p_dec_2','lab1.py',445),
  ('Exp -> Exp ASSIGNOP Exp','Exp',3,'p_exp_ASSIGNOP','lab1.py',451),
  ('Exp -> Exp AND Exp','Exp',3,'p_exp_AND','lab1.py',455),
  ('Exp -> Exp OR Exp','Exp',3,'p_exp_OR','lab1.py',459),
  ('Exp -> Exp RELOP Exp','Exp',3,'p_exp_RELOP','lab1.py',463),
  ('Exp -> Exp PLUS Exp','Exp',3,'p_exp_PLUS','lab1.py',467),
  ('Exp -> Exp MINUS Exp','Exp',3,'p_exp_MINUS','lab1.py',471),
  ('Exp -> Exp STAR Exp','Exp',3,'p_exp_STAR','lab1.py',475),
  ('Exp -> Exp DIV Exp','Exp',3,'p_exp_DIV','lab1.py',479),
  ('Exp -> LP Exp RP','Exp',3,'p_exp_LPRP','lab1.py',483),
  ('Exp -> MINUS Exp','Exp',2,'p_exp_MINUS_2','lab1.py',487),
  ('Exp -> NOT Exp','Exp',2,'p_exp_NOT','lab1.py',491),
  ('Exp -> ID LP Args RP','Exp',4,'p_exp_IDLPRP','lab1.py',495),
  ('Exp -> ID LP RP','Exp',3,'p_exp_IDLPRP2','lab1.py',499),
  ('Exp -> Exp LB Exp RB','Exp',4,'p_exp_LBRB','lab1.py',503),
  ('Exp -> Exp DOT ID','Exp',3,'p_exp_DOTID','lab1.py',507),
  ('Exp -> ID','Exp',1,'p_exp_ID','lab1.py',511),
  ('Exp -> INT','Exp',1,'p_exp_INT','lab1.py',515),
  ('Exp -> FLOAT','Exp',1,'p_exp_FLOAT','lab1.py',519),
  ('Args -> Exp COMMA Args','Args',3,'p_args_1','lab1.py',525),
  ('Args -> Exp','Args',1,'p_args_2','lab1.py',529),
  ('empty -> <empty>','empty',0,'p_empty','lab1.py',535),
  ('ExtDef -> error SEMI','ExtDef',2,'p_extdef_error','lab1.py',556),
  ('FunDec -> error RP','FunDec',2,'p_fundec_error','lab1.py',560),
  ('CompSt -> error RC','CompSt',2,'p_compst_error','lab1.py',564),
  ('Stmt -> error SEMI','Stmt',2,'p_stmt_error','lab1.py',568),
  ('Def -> Specifier error SEMI','Def',3,'p_def_error','lab1.py',572),
]