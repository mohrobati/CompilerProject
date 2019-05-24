import xmltodict
import json
import ast


class CodeGen:

    def arithmetic_tac_generator(self, flag, dic, p):
        if flag:
            pass
        else:
            word = ''
            word += dic['exp']['place'] + ' = '
            if 'VALUE' in dic['exp']['exp'][0].keys():
                word += dic['exp']['exp'][0]['VALUE']
            elif 'lvalue' in dic['exp']['exp'][0].keys():
                word += p[1].place #dic['exp']['exp'][0]['lvalue']['ID']
            elif 'place' in dic['exp']['exp'][0].keys():
                word += dic['exp']['exp'][0]['place']
            else:
                word += p[1].place

            word += ' ' + dic['exp']['OP'] + ' '
            if 'VALUE' in dic['exp']['exp'][1].keys():
                word += dic['exp']['exp'][1]['VALUE']
            elif 'lvalue' in dic['exp']['exp'][1].keys():
                word += p[3].place #dic['exp']['exp'][1]['lvalue']['ID']
            elif 'place' in dic['exp']['exp'][1].keys():
                word += dic['exp']['exp'][1]['place']
            else:
                word += p[3].place

            p[0].code=p[1].code+p[3].code+ word + ";\n"

    def assignment_tac_generator(self,flag, dic , p):
        if flag:
            pass
        else:
            word = '*'
            if 'assignstmt' in dic.keys():
                word += dic['assignstmt']['lvalue']['ID'] + ' = '
                if 'place' in dic['assignstmt']['exp'].keys():
                    word += dic['assignstmt']['exp']['place']
                elif 'lvalue' in dic['assignstmt']['exp'].keys():
                    word += dic['assignstmt']['exp']['lvalue']['ID']
                else:
                    word += dic['assignstmt']['exp']['VALUE']

            elif 'iddec' in dic.keys():
                word += dic['iddec']['ID'] + ' = '
                if 'place' in dic['iddec']['exp'].keys():
                    word += dic['iddec']['exp']['place']
                elif 'lvalue' in dic['iddec']['exp'].keys():
                    word += dic['iddec']['exp']['lvalue']['ID']
                else:
                    word += dic['iddec']['exp']['VALUE']
            return p[3].code+word + ";"

    def relop_tac_generator(self, flag, p):
        if flag:
            pass
        else:
            word = ''
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if 'place' in dic['exp'].keys():
                word += dic['exp']['place']
            elif 'lvalue' in dic['exp'].keys():
                word += dic['exp']['lvalue']['ID']
            elif 'VALUE' in dic['exp'].keys():
                word += dic['exp']['VALUE']
            else:
                word += p[1].place
            if p[2] == '.NE.':
                word += ' != '
            elif p[2] == '.EQ.':
                word += ' == '
            elif p[2] == '.LT.':
                word += ' < '
            elif p[2] == '.GT.':
                word += ' > '
            elif p[2] == '.LE.':
                word += ' <= '
            elif p[2] == '.GE.':
                word += ' >= '
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[3]))))
            if 'place' in dic['exp'].keys():
                word += dic['exp']['place']
            elif 'lvalue' in dic['exp'].keys():
                word += dic['exp']['lvalue']['ID']
            elif 'VALUE' in dic['exp'].keys():
                word += dic['exp']['VALUE']
            else:
                word += p[3].place
            p[0].exp = word

    def boolean_tac_generator(self, flag, p, l_true, l_false, l_next):
        if flag:
            pass
        else:
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if len(p[3].quad) != 0:
                arg1 = p[3].quad[0]
                op   = p[3].quad[1]
                arg2 = p[3].quad[2]
                self.patch(arg1, arg2, l_true, l_false, op)
                self.pprint(arg1, arg2)
                word = ""
                word += l_true + " : " + dic['lvalue']['ID'] + " = true;\n"
                word += "goto " + l_next + ";\n"
                word += l_false + " : " + dic['lvalue']['ID'] + " = false;\n"
                word += l_next + " : "
                return word
            else:
                word = "if (" + p[3].exp + ") goto " + l_true + ";"
                word += "\ngoto " + l_false + ";\n"
                word += l_true + " : " + dic['lvalue']['ID'] + " = true;\n"
                word += "goto " + l_next + ";\n"
                word += l_false + " : " + dic['lvalue']['ID'] + " = false;\n"
                word += l_next + " : "
                return word

    def if_tac_generator(self, flag, p, l_true, l_false):
        if flag:
            pass
        else:
            p[1].true = l_true
            p[1].false = l_false
            if len(p[1].quad) != 0:
                arg1 = p[1].quad[0]
                op   = p[1].quad[1]
                arg2 = p[1].quad[2]
                self.patch(arg1, arg2, l_true, l_false, op)
                self.pprint(arg1, arg2)
                print(l_true + " : ")
            else:
                dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
                if p[1].exp is "":
                    p[1].exp = dic['exp']['lvalue']['ID']
                word = "if (" + p[1].exp + ") goto " + l_true + ";"
                word += "\ngoto " + l_false + ";\n"
                word += l_true + " : "
                print(word)

    def while_tac_generator(self, flag, p, l_true, l_false, l_begin):
        if flag:
            pass
        else:
            p[1].begin = l_begin
            print(l_begin + " : ")
            p[1].true = l_true
            p[1].false = l_false
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if p[1].exp is "":
                p[1].exp = dic['exp']['lvalue']['ID']

            word = "if (" + p[1].exp + ") goto " + l_true + ";"
            word += "\ngoto " + l_false + ";\n"
            word += l_true + " : "
            print(word)

    def for_tac_generator(self, flag, p, id, l_true, l_false, l_begin, up):
        if flag:
            pass
        else:
            p[1].begin = l_begin
            print(l_begin + " : ")
            p[1].true = l_true
            p[1].false = l_false
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if up:
                if 'place' in dic['exp'].keys():
                    word = "if (" + id + " < " + dic['exp']['place'] + ") goto " + l_true + ";"
                elif 'lvalue' in dic['exp'].keys():
                    word = "if (" + id + " < " + dic['exp']['lvalue']['ID'] + ") goto " + l_true + ";"
                else:
                    word = "if (" + id + " < " + dic['exp']['VALUE'] + ") goto " + l_true + ";"
            else:
                if 'place' in dic['exp'].keys():
                    word = "if (" + id + " > " + dic['exp']['place'] + ") goto " + l_true + ";"
                elif 'lvalue' in dic['exp'].keys():
                    word = "if (" + id + " > " + dic['exp']['lvalue']['ID'] + ") goto " + l_true + ";"
                else:
                    word = "if (" + id + " > " + dic['exp']['VALUE'] + ") goto " + l_true + ";"

            word += "\ngoto " + l_false + ";\n"
            word += l_true + " : "
            print(word)

    def switch_case_tac_generator(self, flag, p, id, value, l_true, l_false):
        if flag:
            pass
        else:
            p[0].true = l_true
            p[0].false = l_false
            word = 'if (' + id + " == " + str(value) + ") goto " + l_true + ";\n"
            word += "goto " + l_false + ";\n"
            word += l_true + " : "
            print(word)

    def patch(self, arg1, arg2, l_true, l_false, op):
        arg1_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg1))))
        arg2_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg2))))
        print(arg1_dic)
        if 'exp' in arg1_dic['exp']['exp'][0].keys():
            if arg1.true != "":
                arg1.quad[2].true = arg1.true
            if arg1.false != "":
                arg1.quad[2].false = arg1.false

            if arg1.quad[1] == "Or Else":
                if arg1.true != "":
                    arg1.quad[0].true = arg1.true

            if arg1.quad[1] == "And Then":
                if arg1.false != "":
                    arg1.quad[0].false = arg1.false

            if arg1.label != "":
                arg1.quad[0].label = arg1.label

            self.patch(arg1.quad[0], arg1.quad[2], l_true, l_false, arg1.quad[1])
        else:
            if op == 'And Then':
                if arg1.false == "":
                   arg1.false = l_false
            elif op == 'Or Else':
                if arg1.true == "":
                   arg1.true = l_true

        if 'exp' in arg2_dic['exp']['exp'][0].keys():

            if arg2.false != "":
                arg2.quad[2].false = arg2.false
            if arg2.true != "":
                arg2.quad[2].true = arg2.true

            if arg2.quad[1] == "Or Else":
                if arg2.true != "":
                    arg2.quad[0].true = arg2.true
            if arg2.quad[1] == "And Then":
                if arg2.false != "":
                    arg2.quad[0].false = arg2.false

            if arg2.label != "":
                arg2.quad[0].label = arg2.label

            self.patch(arg2.quad[0], arg2.quad[2], l_true, l_false, arg2.quad[1])
        else:
            if arg2.true == "":
               arg2.true = l_true
            if arg2.false == "":
               arg2.false = l_false

    def pprint(self, arg1, arg2):
        arg1_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg1))))
        arg2_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg2))))
        if 'exp' in arg1_dic['exp']['exp'][0].keys():
            self.pprint(arg1.quad[0], arg1.quad[2])
        else:
            print(arg1.generate_code())

        if 'exp' in arg2_dic['exp']['exp'][0].keys():
            self.pprint(arg2.quad[0], arg2.quad[2])
        else:
            print(arg2.generate_code())







