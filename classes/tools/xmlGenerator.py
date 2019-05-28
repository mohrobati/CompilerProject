from classes.tools.nonTerminal import nonTerminal
import xmltodict
import ast
import json


class XMLGenerator:
    def __init__(self):
        self.w = ''

    def gen_p_prog_declist(self, p):
        w = "<program>"
        w += "<PROGRAM>" + p[1] + "</PROGRAM>"
        w += "<ID>" + p[2] + "</ID>"
        w += "<SEMI_COLON>" + p[3] + "</SEMI_COLON>"
        w += str(p[4])
        w += str(p[5])
        w += "<SEMI_COLON>" + p[6] + "</SEMI_COLON>"
        w += "</program>"
        p[0] = nonTerminal(w)
        self.w = w

    def gen_p_prog_block(self, p):
        w = "<program>"
        w += "<PROGRAM>" + p[1] + "</PROGRAM>"
        w += "<ID>" + p[2] + "</ID>"
        w += "<SEMI_COLON>" + p[3] + "</SEMI_COLON>"
        w += str(p[4])
        w += "<SEMI_COLON>" + p[5] + "</SEMI_COLON>"
        w += "</program>"
        p[0] = nonTerminal(w)
        self.w = w

    def gen_p_declist(self, p):
        w = "<declist>"
        w += str(p[1])
        w += "</declist>"
        p[0] = nonTerminal(w)

    def gen_p_declist_ext(self, p):
        w = "<declist>"
        w += str(p[1])
        w += str(p[2])
        w += "</declist>"
        p[0] = nonTerminal(w)

    def gen_p_dec_vardec(self, p):
        w = "<dec>"
        w += str(p[1])
        w += "</dec>"
        p[0] = nonTerminal(w)

    def gen_p_dec_procdec(self, p):
        w = "<dec>"
        w += str(p[1])
        w += "</dec>"
        p[0] = nonTerminal(w)

    def gen_p_dec_funcdec(self, p):
        w = "<dec>"
        w += str(p[1])
        w += "</dec>"
        p[0] = nonTerminal(w)

    def gen_p_type_int(self, p):
        w = "<type>"
        w += "<INT>"
        w += str(p[1])
        w += "</INT>"
        w += "</type>"
        p[0] = nonTerminal(w)

    def gen_p_type_real(self, p):
        w = "<type>"
        w += "<REAL>"
        w += str(p[1])
        w += "</REAL>"
        w += "</type>"
        p[0] = nonTerminal(w)

    def gen_p_type_bool(self, p):
        w = "<type>"
        w += "<BOOL>"
        w += str(p[1])
        w += "</BOOL>"
        w += "</type>"
        p[0] = nonTerminal(w)

    def gen_p_iddec_id(self, p):
        w = "<iddec>"
        w += "<ID>"
        w += str(p[1])
        w += "</ID>"
        w += "</iddec>"
        p[0] = nonTerminal(w)

    def gen_p_iddec_exp(self, p):
        w = "<iddec>"
        w += "<ID>"
        w += str(p[1])
        w += "</ID>"
        w += "<ASSIGN>"
        w += str(p[2])
        w += "</ASSIGN>"
        w += str(p[3])
        w += "</iddec>"
        p[0] = nonTerminal(w)

    def gen_p_idlist_iddec(self, p):
        w = "<idlist>"
        w += str(p[1])
        w += "</idlist>"
        p[0] = nonTerminal(w)

    def gen_p_idlist_ext(self, p):
        w = "<idlist>"
        w += str(p[1])
        w += "<SEPARATOR>" + p[2] + "</SEPARATOR>"
        w += str(p[3])
        w += "</idlist>"
        p[0] = nonTerminal(w)

    def gen_p_vardec(self, p):
        w = "<vardec>"
        w += str(p[1])
        w += str(p[2])
        w += "<SEMI_COLON>" + p[3] + "</SEMI_COLON>"
        w += "</vardec>"
        p[0] = nonTerminal(w)

    def gen_p_procdec_declist(self, p):
        w = "<procdec>"
        w += "<PROCEDURE>"
        w += str(p[1])
        w += "</PROCEDURE>"
        w += "<ID>"
        w += str(p[2])
        w += "</ID>"
        w += "<OPEN_PAREN>"
        w += str(p[3])
        w += "</OPEN_PAREN>"
        w += str(p[4])
        w += "<CLOSE_PAREN>"
        w += str(p[5])
        w += "</CLOSE_PAREN>"
        w += str(p[6])
        w += str(p[7])
        w += "<SEMI_COLON>"
        w += str(p[8])
        w += "</SEMI_COLON>"
        w += "</procdec>"
        p[0] = nonTerminal(w)

    def gen_p_procdec_block(self, p):
        w = "<procdec>"
        w += "<PROCEDURE>"
        w += str(p[1])
        w += "</PROCEDURE>"
        w += "<ID>"
        w += str(p[2])
        w += "</ID>"
        w += "<OPEN_PAREN>"
        w += str(p[3])
        w += "</OPEN_PAREN>"
        w += str(p[4])
        w += "<CLOSE_PAREN>"
        w += str(p[5])
        w += "</CLOSE_PAREN>"
        w += str(p[6])
        w += "<SEMI_COLON>"
        w += str(p[7])
        w += "</SEMI_COLON>"
        w += "</procdec>"
        p[0] = nonTerminal(w)

    def gen_p_funcdec_declist(self, p):
        w = "<funcdec>"
        w += str(p[1])
        w += "<OPEN_PAREN>"
        w += str(p[2])
        w += "</OPEN_PAREN>"
        w += str(p[3])
        w += "<CLOSE_PAREN>"
        w += str(p[4])
        w += "</CLOSE_PAREN>"
        w += "<COLON>"
        w += str(p[5])
        w += "</COLON>"
        w += str(p[6])
        w += str(p[7])
        w += str(p[8])
        w += "<SEMI_COLON>"
        w += str(p[9])
        w += "</SEMI_COLON>"
        w += "</funcdec>"
        p[0] = nonTerminal(w)

    def gen_p_funcdec_block(self, p):
        w = "<funcdec>"
        w += "<FUNCTION>"
        w += str(p[1])
        w += "</FUNCTION>"
        w += "<ID>"
        w += str(p[2])
        w += "</ID>"
        w += "<OPEN_PAREN>"
        w += str(p[3])
        w += "</OPEN_PAREN>"
        w += str(p[4])
        w += "<CLOSE_PAREN>"
        w += str(p[5])
        w += "</CLOSE_PAREN>"
        w += "<COLON>"
        w += str(p[6])
        w += "</COLON>"
        w += str(p[7])
        w += str(p[8])
        w += "<SEMI_COLON>"
        w += str(p[9])
        w += "</SEMI_COLON>"
        w += "</funcdec>"
        p[0] = nonTerminal(w)

    def gen_p_paramdecs(self, p):
        w = "<paramdecs>"
        w += str(p[1])
        w += "</paramdecs>"
        p[0] = nonTerminal(w)

    def gen_p_paramdecs_ext(self, p):
        w = "<paramdecs>"
        w += str(p[1])
        w += "<SEMI_COLON>"
        w += str(p[2])
        w += "</SEMI_COLON>"
        w += str(p[3])
        w += "</paramdecs>"
        p[0] = nonTerminal(w)

    def gen_p_paramdec(self, p):
        w = "<paramdec>"
        w += str(p[1])
        w += str(p[2])
        w += "</paramdec>"
        p[0] = nonTerminal(w)

    def gen_p_paramlist(self, p):
        w = "<paramlist>"
        w += "<ID>" + p[1] + "</ID>"
        w += "</paramlist>"
        p[0] = nonTerminal(w)

    def gen_p_paramlist_ext(self, p):
        w = "<paramlist>"
        w += str(p[1])
        w += "<SEPARATOR>" + p[2] + "</SEPARATOR>"
        w += "<ID>" + p[3] + "</ID>"
        w += "</paramlist>"
        p[0] = nonTerminal(w)

    def gen_p_block_stmtlist(self, p):
        w = "<block>"
        w += "<BEGIN>" + p[1] + "</BEGIN>"
        w += str(p[2])
        w += "<END>" + p[3] + "</END>"
        w += "</block>"
        p[0] = nonTerminal(w)

    def gen_p_block_stmt(self, p):
        w = "<block>"
        w += str(p[1])
        w += "</block>"
        p[0] = nonTerminal(w)

    def gen_p_stmtlist(self, p):
        w = "<stmtlist>"
        w += str(p[1])
        w += "</stmtlist>"
        p[0] = nonTerminal(w)

    def gen_p_stmtlist_ext(self, p):
        w = "<stmtlist>"
        w += str(p[1])
        w += "<SEMI_COLON>" + p[2] + "</SEMI_COLON>"
        w += str(p[3])
        w += "</stmtlist>"
        p[0] = nonTerminal(w)

    def gen_p_lvalue(self, p):
        w = "<lvalue>"
        w += "<ID>" + p[1] + "</ID>"
        w += "</lvalue>"
        p[0] = nonTerminal(w)

    def gen_p_caseelement(self, p):
        w = "<caseelement>"
        w += "<case>" + str(p[1]) + "</case>"
        w += "<COLON>" + p[2] + "</COLON>"
        w += str(p[4])
        w += "<SEMI_COLON>" + p[5] + "</SEMI_COLON>"
        w += "</caseelement>"
        p[0] = nonTerminal(w)

    def gen_p_caseelement_ext(self, p):
        w = "<caseelement>"
        w += str(p[1])
        w += "<case>" + str(p[2]) + "</case>"
        w += "<COLON>" + p[3] + "</COLON>"
        w += str(p[5])
        w += "<SEMI_COLON>" + p[6] + "</SEMI_COLON>"
        w += "</caseelement>"
        p[0] = nonTerminal(w)

    def gen_p_caseelement_control(self, p):
        w = ""
        p[0] = nonTerminal(w)

    def gen_p_case_integer(self, p):
        w = "<case>"
        w += "<INTEGER>" + str(p[1]) + "</INTEGER>"
        w += "</case>"
        p[0] = nonTerminal(w)

    def gen_p_assign_stmt_assign(self, p):
        w = "<assignstmt>"
        w += str(p[1])
        w += "<ASSIGN>"
        w += str(p[2])
        w += "</ASSIGN>"
        w += str(p[3])
        w += "</assignstmt>"

        p[0] = nonTerminal(w)

    def gen_p_stmt_assign(self, p):
        w = "<stmt>"
        w += str(p[1])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_if(self, p):
        w = "<stmt>"
        w += "<IF>" + p[1] + "</IF>"
        w += str(p[2])
        w += "<THEN>" + p[3] + "</THEN>"
        w += str(p[4])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_if_else(self, p):
        w = "<stmt>"
        w += "<IF>" + p[1] + "</IF>"
        w += str(p[2])
        w += "<THEN>" + p[3] + "</THEN>"
        w += str(p[4])
        w += "<ELSE>" + p[5] + "</ELSE>"
        w += str(p[7])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_control_if_exp(self, p):
        w = "<controlifexp>"
        w += str(p[1])
        w += "</controlifexp>"
        p[0] = nonTerminal(w)

    def gen_p_print(self, p):
        w = "<stmt>"
        w += "<PRINT>" + p[1] + "</PRINT>"
        w += "<OPEN_PAREN>" + p[2] + "</OPEN_PAREN>"
        w += "<ID>" + p[3] + "</ID>"
        w += "<CLOSE_PAREN>" + p[4] + "</CLOSE_PAREN>"
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_control_while_exp(self, p):
        w = "<controlwhileexp>"
        w += str(p[1])
        w += "</controlwhileexp>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_while(self, p):
        w = "<stmt>"
        w += "<WHILE>" + p[1] + "</WHILE>"
        w += str(p[2])
        w += "<DO>" + p[3] + "</DO>"
        w += str(p[4])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_for_up(self, p):
        w = "<stmt>"
        w += "<FOR>" + p[1] + "</FOR>"
        w += str(p[2])
        w += "<TO>" + p[3] + "</TO>"
        w += str(p[4])
        w += "<DO>" + p[5] + "</DO>"
        w += str(p[6])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_for_down(self, p):
        w = "<stmt>"
        w += "<FOR>" + p[1] + "</FOR>"
        w += str(p[2])
        w += "<DOWNTO>" + p[3] + "</DOWNTO>"
        w += str(p[4])
        w += "<DO>" + p[5] + "</DO>"
        w += str(p[6])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_control_for_exp(self, p):
        w = "<controlforexp>"
        w += str(p[1])
        w += "</controlforexp>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_case(self, p):
        w = "<stmt>"
        w += "<CASE>" + p[1] + "</CASE>"
        w += str(p[2])
        w += str(p[3])
        w += "<END>" + p[3].word + "</END>"
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_control_case_exp(self, p):
        w = "<controlcaseexp>"
        w += str(p[1])
        w += "</controlcaseexp>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_return(self, p):
        w = "<stmt>"
        w += "<RETURN>" + p[1] + "</RETURN>"
        w += str(p[2])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_exp_sum(self, p, place):
        w = "<exp>"
        w += str(p[1])
        w += "<OP>" + p[2] + "</OP>"
        w += "<place>" + place + "</place>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_sub(self, p, place):
        w = "<exp>"
        w += str(p[1])
        w += "<OP>" + p[2] + "</OP>"
        w += "<place>" + place + "</place>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_mul(self, p, place):
        w = "<exp>"
        w += str(p[1])
        w += "<OP>" + p[2] + "</OP>"
        w += "<place>" + place + "</place>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_div(self, p, place):
        w = "<exp>"
        w += str(p[1])
        w += "<OP>" + p[2] + "</OP>"
        w += "<place>" + place + "</place>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_stmt_exp(self, p):
        w = "<stmt>"
        w += str(p[1])
        w += "</stmt>"
        p[0] = nonTerminal(w)

    def gen_p_exp_and(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + p[2] + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_or(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + p[2] + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_ne(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_eq(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_lt(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_gt(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_le(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_ge(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "<BOOLOP>" + str(p[2]) + "</BOOLOP>"
        w += str(p[3])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_paren(self, p):
        w = ""
        w += str(p[2])
        p[0] = nonTerminal(w)

    def gen_p_exp_real(self, p):
        w = "<exp>"
        w += "<VALUE>" + str(p[1]) + "</VALUE>"
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_integer(self, p):
        w = "<exp>"
        w += "<VALUE>" + str(p[1]) + "</VALUE>"
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_true(self, p):
        w = "<exp>"
        w += "<VALUE>" 'true' + "</VALUE>"
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_false(self, p):
        w = "<exp>"
        w += "<VALUE>" + 'false' + "</VALUE>"
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_lvalue(self, p):
        w = "<exp>"
        w += str(p[1])
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_exp_func(self, p):
        w = "<exp>"
        w += "<ID>" + p[1] + "</ID>"
        w += "<OPEN_PAREN>" + p[2] + "</OPEN_PAREN>"
        w += str(p[3])
        w += "<CLOSE_PAREN>" + p[4] + "</CLOSE_PAREN>"
        w += "</exp>"
        p[0] = nonTerminal(w)

    def gen_p_explist(self, p):
        w = "<explist>"
        w += str(p[1])
        w += "</explist>"
        p[0] = nonTerminal(w)

    def gen_p_explist_ext(self, p):
        w = "<explist>"
        w += str(p[1])
        w += "<SEPARATOR>" + p[2] + "</SEPARATOR>"
        w += str(p[3])
        w += "</explist>"
        p[0] = nonTerminal(w)

    def gen_p_funcname(self, p):
        w = "<FUNCTION>"
        w += str(p[1])
        w += "</FUNCTION>"
        w += "<ID>"
        w += str(p[2])
        w += "</ID>"
        p[0] = nonTerminal(w)
