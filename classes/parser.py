from ply import yacc
from classes.lexer import Lexer
from classes.tools.xmlGenerator import XMLGenerator
from classes.tools.dictTraversal import DictTraversal
from classes.tools.codeGen import CodeGen
import xmltodict
import ast
import json


class Parser:
    lineNumber: int
    tokens = Lexer().tokens

    def __init__(self):
        self.parser = None
        self.p = 0
        self.xmlGenerator = XMLGenerator()
        self.codeGen = CodeGen()
        self.symbolTables = []
        self.packets = []
        self.t_ctr = 0
        self.b_ctr = 0
        self.l_ctr = 0
        self.quad = 0
        self.else_tmp = ""
        self.id_tmp = ""
        self.case_id_tmp = []
        self.case_int_tmp = ""
        self.case_true_tmp = []
        self.case_false_tmp = ""
        self.flag = False

    def p_prog_declist(self, p):
        """program : PROGRAM ID SEMI_COLON declist block SEMI_COLON"""
        self.xmlGenerator.gen_p_prog_declist(p)
        self.mktables()

    def p_prog_block(self, p):
        """program : PROGRAM ID SEMI_COLON block SEMI_COLON"""
        self.xmlGenerator.gen_p_prog_block(p)
        self.mktables()

    def p_declist(self, p):
        """declist : dec"""
        self.xmlGenerator.gen_p_declist(p)

    def p_declist_ext(self, p):
        """declist : declist dec"""
        self.xmlGenerator.gen_p_declist_ext(p)

    def p_dec_vardec(self, p):
        """dec : vardec"""
        self.xmlGenerator.gen_p_dec_vardec(p)

    def p_dec_procdec(self, p):
        """dec : procdec"""
        self.xmlGenerator.gen_p_dec_procdec(p)

    def p_dec_funcdec(self, p):
        """dec : funcdec"""
        self.xmlGenerator.gen_p_dec_funcdec(p)

    def p_type_int(self, p):
        """type : INT"""
        self.xmlGenerator.gen_p_type_int(p)

    def p_type_real(self, p):
        """type : REAL"""
        self.xmlGenerator.gen_p_type_real(p)

    def p_type_bool(self, p):
        """type : BOOL"""
        self.xmlGenerator.gen_p_type_bool(p)

    def p_iddec_id(self, p):
        """iddec : ID"""
        self.xmlGenerator.gen_p_iddec_id(p)

    def p_iddec_exp(self, p):
        """iddec : ID ASSIGN exp"""
        self.xmlGenerator.gen_p_iddec_exp(p)
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        if p[3].type != "bool":
            print(self.codeGen.assignment_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0]))))))
        else:
            print(self.codeGen.boolean_tac_generator(self.flag, p, self.new_label(), self.new_label(), self.new_label()))
    def p_idlist_iddec(self, p):
        """idlist : iddec"""
        self.xmlGenerator.gen_p_idlist_iddec(p)

    def p_idlist_ext(self, p):
        """idlist : idlist SEPARATOR iddec"""
        self.xmlGenerator.gen_p_idlist_ext(p)

    def p_vardec(self, p):
        """vardec : type idlist SEMI_COLON"""
        self.xmlGenerator.gen_p_vardec(p)

    def p_procdec_declist(self, p):
        """procdec : PROCEDURE ID OPEN_PAREN paramdecs CLOSE_PAREN declist block SEMI_COLON"""
        self.xmlGenerator.gen_p_procdec_declist(p)

    def p_procdec_block(self, p):
        """procdec : PROCEDURE ID OPEN_PAREN paramdecs CLOSE_PAREN block SEMI_COLON"""
        self.xmlGenerator.gen_p_procdec_block(p)

    def p_funcdec_declist(self, p):
        """funcdec : FUNCTION ID OPEN_PAREN paramdecs CLOSE_PAREN COLON type declist block SEMI_COLON"""
        self.xmlGenerator.gen_p_funcdec_declist(p)

    def p_funcdec_block(self, p):
        """funcdec : FUNCTION ID OPEN_PAREN paramdecs CLOSE_PAREN COLON type block SEMI_COLON"""
        self.xmlGenerator.gen_p_funcdec_block(p)

    def p_paramdecs(self, p):
        """paramdecs : paramdec"""
        self.xmlGenerator.gen_p_paramdecs(p)

    def p_paramdecs_ext(self, p):
        """paramdecs : paramdecs SEMI_COLON paramdec"""
        self.xmlGenerator.gen_p_paramdecs_ext(p)

    def p_paramdec(self, p):
        """paramdec : type paramlist"""
        self.xmlGenerator.gen_p_paramdec(p)

    def p_paramlist(self, p):
        """paramlist : ID"""
        self.xmlGenerator.gen_p_paramlist(p)

    def p_paramlist_ext(self, p):
        """paramlist : paramlist SEPARATOR ID"""
        self.xmlGenerator.gen_p_paramlist_ext(p)

    def p_block_stmtlist(self, p):
        """block : BEGIN stmtlist END"""
        self.xmlGenerator.gen_p_block_stmtlist(p)

    def p_block_stmt(self, p):
        """block : stmt"""
        self.xmlGenerator.gen_p_block_stmt(p)

    def p_stmtlist(self, p):
        """stmtlist : stmt"""
        self.xmlGenerator.gen_p_stmtlist(p)

    def p_stmtlist_ext(self, p):
        """stmtlist : stmtlist SEMI_COLON stmt"""
        self.xmlGenerator.gen_p_stmtlist_ext(p)

    def p_lvalue(self, p):
        """lvalue : ID"""
        self.xmlGenerator.gen_p_lvalue(p)
        self.id_tmp = p[1]
        p[0].place = p[1]


    def p_stmt_assign(self, p):
        """assignstmt : lvalue ASSIGN exp"""
        self.xmlGenerator.gen_p_assign_stmt_assign(p)
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        if p[3].type != "bool":
            print(self.codeGen.assignment_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))),p))
        else:
            print(self.codeGen.boolean_tac_generator(self.flag, p, self.new_label(), self.new_label(), self.new_label()))

    def p_assign_stmt_assign(self, p):
        """stmt : assignstmt"""
        self.xmlGenerator.gen_p_stmt_assign(p)

    def p_stmt_if(self, p):
        """stmt : IF controlifexp THEN block"""
        self.xmlGenerator.gen_p_stmt_if(p)
        print(p[2].false + " : ")

    def p_stmt_if_else(self, p):
        """stmt : IF controlifexp THEN block ELSE controlelse block"""
        self.xmlGenerator.gen_p_stmt_if_else(p)

    def p_control_if_exp(self, p):
        """controlifexp : exp"""
        self.xmlGenerator.gen_p_control_if_exp(p)
        self.codeGen.if_tac_generator(self.flag, p, self.new_label(), self.new_label())
        self.else_tmp = p[1].false
        p[0] = p[1]

    def p_controlelse(self, p):
        """controlelse : """
        print(self.else_tmp + " : ")

    def p_stmt_while(self, p):
        """stmt : WHILE controlwhileexp DO block"""
        self.xmlGenerator.gen_p_stmt_while(p)
        print("goto " + p[2].begin + ";")
        print(p[2].false + " : ")

    def p_control_while_exp(self, p):
        """controlwhileexp : exp"""
        self.xmlGenerator.gen_p_control_while_exp(p)
        self.codeGen.while_tac_generator(self.flag, p, self.new_label(), self.new_label(), self.new_label())
        self.else_tmp = p[1].false
        p[0] = p[1]

    def p_stmt_for_up(self, p):
        """stmt : FOR assignstmt TO controlforupexp DO block"""
        self.xmlGenerator.gen_p_stmt_for_up(p)
        dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[2]))))
        id = dic['assignstmt']['lvalue']['ID']
        tmp = self.new_temp()
        print(tmp + " = " + id + " + 1;")
        print(id + " = " + tmp)
        print("goto " + p[4].begin + ";")
        print(p[4].false + " : ")

    def p_stmt_for_down(self, p):
        """stmt : FOR assignstmt DOWNTO controlfordownexp DO block"""
        self.xmlGenerator.gen_p_stmt_for_down(p)
        dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[2]))))
        id = dic['assignstmt']['lvalue']['ID']
        tmp = self.new_temp()
        print(tmp + " = " + id + " - 1;")
        print(id + " = " + tmp)
        print("goto " + p[4].begin + ";")
        print(p[4].false + " : ")

    def p_control_for_up_exp(self, p):
        """controlforupexp : exp"""
        self.xmlGenerator.gen_p_control_for_exp(p)
        self.codeGen.for_tac_generator(self.flag, p, self.id_tmp, self.new_label(), self.new_label(), self.new_label(), True)
        p[0] = p[1]

    def p_control_for_down_exp(self, p):
        """controlfordownexp : exp"""
        self.xmlGenerator.gen_p_control_for_exp(p)
        self.codeGen.for_tac_generator(self.flag, p, self.id_tmp, self.new_label(), self.new_label(), self.new_label(), False)
        p[0] = p[1]

    def p_stmt_case(self, p):
        """stmt : CASE controlcaseexp caseelement END"""
        self.xmlGenerator.gen_p_stmt_case(p)
        print(self.case_true_tmp.pop() + " : ")
        self.case_id_tmp.pop()

    def p_control_case_exp(self, p):
        """controlcaseexp : exp"""
        self.xmlGenerator.gen_p_control_case_exp(p)
        dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
        if 'place' in dic['exp'].keys():
            self.case_id_tmp.append(dic['exp']['place'])
        elif 'lvalue' in dic['exp'].keys():
            self.case_id_tmp.append(dic['exp']['lvalue']['ID'])
        else:
            self.case_id_tmp.append(dic['exp']['VALUE'])
        self.case_true_tmp.append(self.new_label())

    def p_caseelement(self, p):
        """ caseelement : case COLON caseelementcontrol block SEMI_COLON"""
        self.xmlGenerator.gen_p_caseelement(p)
        print("goto " + self.case_true_tmp[len(self.case_true_tmp)-1] + ";")
        print(p[3].false + " : ")

    def p_caseelement_ext(self, p):
        """ caseelement : caseelement case COLON caseelementcontrol block SEMI_COLON"""
        self.xmlGenerator.gen_p_caseelement_ext(p)
        print("goto " + self.case_true_tmp[len(self.case_true_tmp)-1] + ";")
        print(p[4].false + " : ")


    def p_case_element_control(self, p):
        """caseelementcontrol : """
        self.xmlGenerator.gen_p_caseelement_control(p)
        t_label = self.new_label()
        f_label = self.new_label()
        self.case_false_tmp = f_label
        self.codeGen.switch_case_tac_generator(self.flag, p, self.case_id_tmp[len(self.case_id_tmp)-1], self.case_int_tmp, t_label, f_label)

    def p_case_integer(self, p):
        """case : INTEGER"""
        self.xmlGenerator.gen_p_case_integer(p)
        self.case_int_tmp = p[1]

    def p_stmt_return(self, p):
        """stmt : RETURN exp"""
        self.xmlGenerator.gen_p_stmt_return(p)

    def p_stmt_exp(self, p):
        """stmt : exp"""
        self.xmlGenerator.gen_p_stmt_exp(p)

    def p_exp_sum(self, p):
        """exp : exp SUM exp"""
        self.xmlGenerator.gen_p_exp_sum(p, self.new_temp())
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        self.codeGen.arithmetic_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))),p)

    def p_exp_sub(self, p):
        """exp : exp SUB exp"""
        self.xmlGenerator.gen_p_exp_sub(p, self.new_temp())
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        self.codeGen.arithmetic_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))),p)

    def p_exp_mul(self, p):
        """exp : exp MUL exp"""
        self.xmlGenerator.gen_p_exp_mul(p, self.new_temp())
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        self.codeGen.arithmetic_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))),p)

    def p_exp_div(self, p):
        """exp : exp DIV exp"""
        self.xmlGenerator.gen_p_exp_div(p, self.new_temp())
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        self.codeGen.arithmetic_tac_generator(self.flag, ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))),p)

    def p_exp_and(self, p):
        """exp : exp AND exp"""
        self.xmlGenerator.gen_p_exp_and(p)
        label = self.new_label()
        p[1].true = label
        p[3].label = label
        p[0].type = "bool"
        p[0].quad.append(p[1])
        p[0].quad.append(p[2])
        p[0].quad.append(p[3])

    def p_exp_or(self, p):
        """exp : exp OR exp"""
        self.xmlGenerator.gen_p_exp_or(p)
        label = self.new_label()
        p[1].false = label
        p[3].label = label
        p[0].type = "bool"
        p[0].quad.append(p[1])
        p[0].quad.append(p[2])
        p[0].quad.append(p[3])

    def p_exp_ne(self, p):
        """exp : exp NE exp"""
        self.xmlGenerator.gen_p_exp_ne(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_eq(self, p):
        """exp : exp EQ exp"""
        self.xmlGenerator.gen_p_exp_eq(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_lt(self, p):
        """exp : exp LT exp"""
        self.xmlGenerator.gen_p_exp_lt(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_gt(self, p):
        """exp : exp GT exp"""
        self.xmlGenerator.gen_p_exp_gt(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_le(self, p):
        """exp : exp LE exp"""
        self.xmlGenerator.gen_p_exp_le(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_ge(self, p):
        """exp : exp GE exp"""
        self.xmlGenerator.gen_p_exp_ge(p)
        self.codeGen.relop_tac_generator(self.flag, p)
        p[0].type = "bool"

    def p_exp_paren(self, p):
        """exp : OPEN_PAREN exp CLOSE_PAREN"""
        self.xmlGenerator.gen_p_exp_paren(p)
        self.packets.append(ast.literal_eval(json.dumps(xmltodict.parse(str(p[0])))))
        p[0] = p[2]

    def p_exp_real(self, p):
        """exp : REALNUMBER"""
        self.xmlGenerator.gen_p_exp_real(p)
        p[0].type = 'Real'

    def p_exp_integer(self, p):
        """exp : INTEGER"""
        self.xmlGenerator.gen_p_exp_integer(p)

    def p_exp_true(self, p):
        """exp : TRUE"""
        self.xmlGenerator.gen_p_exp_true(p)
        p[0].exp = "true"
        p[0].place = "true"

    def p_exp_false(self, p):
        """exp : FALSE"""
        self.xmlGenerator.gen_p_exp_false(p)
        p[0].exp = "false"
        p[0].place = "false"

    def p_exp_lvalue(self, p):
        """exp : lvalue"""
        self.xmlGenerator.gen_p_exp_lvalue(p)
        #pointer assignment for every ID
        p[0].place = self.new_temp()
        p[0].code = p[0].place + " = *" + p[1].place + " ;\n"
        # print(p[0].code)

    def p_exp_func(self, p):
        """exp : ID OPEN_PAREN explist CLOSE_PAREN"""
        self.xmlGenerator.gen_p_exp_func(p)

    def p_explist(self, p):
        """explist : exp"""
        self.xmlGenerator.gen_p_explist(p)

    def p_explist_ext(self, p):
        """explist : explist SEPARATOR exp"""
        self.xmlGenerator.gen_p_explist_ext(p)


    def p_error(self, p):
        raise Exception('ParsingError: invalid grammar at ', p)

    precedence = (
        ('left', 'THEN'),
        ('left', 'ELSE'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'LT'),
        ('left', 'GT'),
        ('left', 'GE'),
        ('left', 'NE'),
        ('left', 'EQ'),
        ('left', 'LE'),
        ('left', 'SUM', 'SUB'),
        ('left', 'MUL', 'DIV')
    )

    def new_temp(self):
        string = 'TT' + str(self.t_ctr)
        self.t_ctr += 1
        return string

    def new_bool(self):
        string = 'BB' + str(self.b_ctr)
        self.b_ctr += 1
        return string

    def new_label(self):
        string = 'LL' + str(self.l_ctr)
        self.l_ctr += 1
        return string

    def mktables(self):
        doc = xmltodict.parse(self.xmlGenerator.w)
        # print(ast.literal_eval(json.dumps(doc,indent=10)))
        # filew= open("doc.dict","w")
        # filew.write(str(ast.literal_eval(json.dumps(doc,indent=10))))
        # filew.close()
        dictTraversal = DictTraversal(ast.literal_eval(json.dumps(doc)))
        #
        # output = open("parsed.xml", 'w')
        # output.write(self.xmlGenerator.w)
        # output.close()
        dictTraversal.maketables()
        self.symbolTables = dictTraversal.tables

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
