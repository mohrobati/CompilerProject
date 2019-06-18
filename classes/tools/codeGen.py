import xmltodict
import json
import ast
from ply import yacc


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
                word += dic['exp']['exp'][0]['lvalue']['ID']
            elif 'place' in dic['exp']['exp'][0].keys():
                word += dic['exp']['exp'][0]['place']
            else:
                word += p[1].place

            word += ' ' + dic['exp']['OP'] + ' '
            if 'VALUE' in dic['exp']['exp'][1].keys():
                word += dic['exp']['exp'][1]['VALUE']
            elif 'lvalue' in dic['exp']['exp'][1].keys():
                word += dic['exp']['exp'][1]['lvalue']['ID']
            elif 'place' in dic['exp']['exp'][1].keys():
                word += dic['exp']['exp'][1]['place']
            else:
                word += p[3].place

            p[0].code=p[1].code+p[3].code+ word + ";\n"

    def assignment_tac_generator(self,flag, dic , p):
        if flag:
            pass
        else:
            word = ""
            if 'assignstmt' in dic.keys():
                word += dic['assignstmt']['lvalue']['ID'] + ' = '
                if 'place' in dic['assignstmt']['exp'].keys():
                    word += dic['assignstmt']['exp']['place']
                elif 'lvalue' in dic['assignstmt']['exp'].keys():
                    word += dic['assignstmt']['exp']['lvalue']['ID']
                elif 'VALUE' in dic['assignstmt']['exp'].keys():
                    word += dic['assignstmt']['exp']['VALUE']
                else:
                    word+=p[3].place


            elif 'iddec' in dic.keys():
                word += dic['iddec']['ID'] + ' = '
                if 'place' in dic['iddec']['exp'].keys():
                    word += dic['iddec']['exp']['place']
                elif 'lvalue' in dic['iddec']['exp'].keys():
                    word += dic['iddec']['exp']['lvalue']['ID']
                elif 'VALUE' in dic['iddec']['exp'].keys():
                    word += dic['iddec']['exp']['VALUE']
                else:
                    word+=p[3].place
            return p[3].code+word + ";\n"

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
            p[0].code = p[1].code+p[3].code

    def boolean_tac_generator(self, flag, p, l_true, l_false, l_next):
        if flag:
            pass
        else:
            if type(p[1]) == str:
                id = p[1]
            else:
                dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
                id = dic['lvalue']['ID']
            if len(p[3].quad) != 0:
                arg1 = p[3].quad[0]
                op   = p[3].quad[1]
                arg2 = p[3].quad[2]
                container = []
                word = ""
                word += arg1.code
                word += arg2.code
                arg1.code = ""
                arg2.code = ""
                self.patch(arg1, arg2, l_true, l_false, op, container)
                for line in container:
                    word += line + "\n"
                word += l_true + " : " + id + " = true;\n"
                word += "goto " + l_next + ";\n"
                word += l_false + " : " + id + " = false;\n"
                word += l_next + " : \n"
                return p[3].code+word
            else:
                word = "if (" + p[3].exp + ") goto " + l_true + ";"
                word += "\ngoto " + l_false + ";\n"
                word += l_true + " : " + id + " = true;\n"
                word += "goto " + l_next + ";\n"
                word += l_false + " : " + id + " = false;\n"
                word += l_next + " : \n"
                return p[3].code+word

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
                container = []
                self.patch(arg1, arg2, l_true, l_false, op, container)
                for line in container:
                    p[1].code += line + "\n"
                p[1].code += (l_true + " : ")
            else:
                dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
                if p[1].exp is "":
                    if 'lvalue' in dic['exp'].keys():
                        p[1].exp = dic['exp']['lvalue']['ID']
                    elif 'VALUE' in dic['exp'].keys():
                        p[1].exp = dic['exp']['VALUE']
                    elif 'place' in dic['exp'].keys():
                        p[1].exp = dic['exp']['place']

                word = "if (" + p[1].exp + ") goto " + l_true + ";"
                word += "\ngoto " + l_false + ";\n"
                word += l_true + " : "

                p[1].code += (word)

    def while_tac_generator(self, flag, p, l_true, l_false, l_begin):
        if flag:
            pass
        else:
            p[1].begin = l_begin
            p[1].code += (l_begin + " : ")
            p[1].true = l_true
            p[1].false = l_false
            if len(p[1].quad) != 0:
                arg1 = p[1].quad[0]
                op = p[1].quad[1]
                arg2 = p[1].quad[2]
                container = []
                self.patch(arg1, arg2, l_true, l_false, op, container)
                for line in container:
                    p[1].code += line + "\n"
                p[1].code += (l_true + " : ")
            else:
                dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
                if p[1].exp is "":
                    if 'lvalue' in dic['exp'].keys():
                        p[1].exp = dic['exp']['lvalue']['ID']
                    elif 'VALUE' in dic['exp'].keys():
                        p[1].exp = dic['exp']['VALUE']
                    elif 'place' in dic['exp'].keys():
                        p[1].exp = dic['exp']['place']
                word = "if (" + p[1].exp + ") goto " + l_true + ";"
                word += "\ngoto " + l_false + ";\n"
                word += l_true + " : "
                p[1].code += (word)

    def for_tac_generator(self, flag, p, id, l_true, l_false, l_begin, up):
        if flag:
            pass
        else:
            p[1].begin = l_begin
            p[1].code += (l_begin + " : \n")
            p[1].true = l_true
            p[1].false = l_false
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if up:
                if 'place' in dic['exp'].keys():
                    word = "if (" + id + " < " + dic['exp']['place'] + ") goto " + l_true + ";\n"
                elif 'lvalue' in dic['exp'].keys():
                    word = "if (" + id + " < " + dic['exp']['lvalue']['ID'] + ") goto " + l_true + ";\n"
                else:
                    word = "if (" + id + " < " + dic['exp']['VALUE'] + ") goto " + l_true + ";\n"
            else:
                if 'place' in dic['exp'].keys():
                    word = "if (" + id + " > " + dic['exp']['place'] + ") goto " + l_true + ";\n"
                elif 'lvalue' in dic['exp'].keys():
                    word = "if (" + id + " > " + dic['exp']['lvalue']['ID'] + ") goto " + l_true + ";\n"
                else:
                    word = "if (" + id + " > " + dic['exp']['VALUE'] + ") goto " + l_true + ";\n"
            word += "\ngoto " + l_false + ";\n"
            word += l_true + " : \n"
            p[1].code += (word)

    def switch_case_tac_generator(self, flag, p, id, value, l_true, l_false):
        if flag:
            pass
        else:
            p[0].true = l_true
            p[0].false = l_false
            word = 'if (' + id + " == " + str(value) + ") goto " + l_true + ";\n"
            word += "goto " + l_false + ";\n"
            word += l_true + " : \n"
            p[0].code+=(word)

    def patch(self, arg1, arg2, l_true, l_false, op, container):
        arg1_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg1))))
        arg2_dic = ast.literal_eval(json.dumps(xmltodict.parse(str(arg2))))
        if 'exp' in arg1_dic['exp'].keys():
            if len(arg1.quad) != 0:
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
                self.patch(arg1.quad[0], arg1.quad[2], l_true, l_false, arg1.quad[1], container)
            else:
                if op == 'And Then':
                    if arg1.false == "":
                        arg1.false = l_false
                elif op == 'Or Else':
                    if arg1.true == "":
                        arg1.true = l_true
                container.append(arg1.generate_code())

        elif 'lvalue' in arg1_dic['exp'].keys():
            if arg1.true == "":
                arg1.true = l_true
            if arg1.false == "":
                arg1.false = l_false
            arg1.exp = arg1_dic['exp']['lvalue']['ID']
            container.append(arg1.generate_code())

        elif 'VALUE' in arg1_dic['exp'].keys():
            if arg1.true == "":
                arg1.true = l_true
            if arg1.false == "":
                arg1.false = l_false
            arg1.exp = arg1_dic['exp']['VALUE']
            container.append(arg1.generate_code())

        elif 'ID' in arg1_dic['exp'].keys():
            if arg1.true == "":
                arg1.true = l_true
            if arg1.false == "":
                arg1.false = l_false
            container.append(arg1.generate_code())

        if 'exp' in arg2_dic['exp'].keys():
            if len(arg2.quad) != 0:
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
                self.patch(arg2.quad[0], arg2.quad[2], l_true, l_false, arg2.quad[1], container)
            else:
                if arg2.true == "":
                    arg2.true = l_true
                if arg2.false == "":
                    arg2.false = l_false
                container.append(arg2.generate_code())

        elif 'lvalue' in arg2_dic['exp'].keys():
            if arg2.true == "":
                arg2.true = l_true
            if arg2.false == "":
                arg2.false = l_false
            arg2.exp = arg2_dic['exp']['lvalue']['ID']
            container.append(arg2.generate_code())

        elif 'VALUE' in arg2_dic['exp'].keys():
            if arg2.true == "":
                arg2.true = l_true
            if arg2.false == "":
                arg2.false = l_false
            arg2.exp = arg2_dic['exp']['VALUE']
            container.append(arg2.generate_code())

        elif 'ID' in arg2_dic['exp'].keys():
            if arg2.true == "":
                arg2.true = l_true
            if arg2.false == "":
                arg2.false = l_false
            container.append(arg2.generate_code())

    def explist_tac_generator(self, flag, p, new_temp, l_true, l_false, l_next):
        if flag:
            pass
        word = "Top = Top - 1 ;\n*Top = "
        if p[0].number == 1:
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[1]))))
            if 'place' in dic['exp'].keys():
                word += dic['exp']['place']
            elif 'lvalue' in dic['exp'].keys():
                word += dic['exp']['lvalue']['ID']
            elif 'VALUE' in dic['exp'].keys():
                word += dic['exp']['VALUE']
            else:
                if p[1].type == 'bool':
                    p[0].code += self.return_bool_generator(p, new_temp, l_true, l_false, l_next, 1)
                    p[1].place = new_temp
                word += p[1].place

        else:

            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[3]))))
            if 'place' in dic['exp'].keys():
                word += dic['exp']['place']
            elif 'lvalue' in dic['exp'].keys():
                word += dic['exp']['lvalue']['ID']
            elif 'VALUE' in dic['exp'].keys():
                word += dic['exp']['VALUE']
            else:
                if p[3].type == 'bool':
                    p[0].code += self.return_bool_generator(p, new_temp, l_true, l_false, l_next, 3)
                    p[3].place = new_temp
                word += p[3].place

        word += ";\n"
        if p[0].number == 1:
            p[0].code += p[1].code+ word
        else:
            p[0].code += p[1].code +p[3].code + word

    def expfunc_tac_generator(self, flag, p, next_label, return_temp,val):
        if flag:
            pass
        p[0].code+="Top = Top - 1 ;\n*Top = "
        p[0].code+=str(val)+" ;\n"
        p[0].code += p[3].code
        word =""
        word += "goto FF" + p[1] + " ;\n"
        word += next_label + ":\n"
        word += return_temp + " =returnValue;\n"
        p[0].code += word
        p[0].exp = return_temp
        p[0].place = return_temp

    def return_tac_generator(self, flag, p, funcId, new_temp, l_true, l_false, l_next):
        if flag:
            pass
        else:
            word = "returnValue="
            dic = ast.literal_eval(json.dumps(xmltodict.parse(str(p[2]))))
            if 'place' in dic['exp'].keys():
                word += dic['exp']['place']
            elif 'lvalue' in dic['exp'].keys():
                word += dic['exp']['lvalue']['ID']
            elif 'VALUE' in dic['exp'].keys():
                word += dic['exp']['VALUE']
            else:
                if p[2].type == 'bool':
                    p[0].code += self.return_bool_generator(p, new_temp, l_true, l_false, l_next, 2)
                    p[2].place = new_temp
                word += p[2].place

            word+=";\n"
            word+="goto EN"+funcId+";\n"
            p[0].code+=p[2].code+word

    def return_bool_generator(self, p, new_temp, l_true, l_false, l_next, i):
        if len(p[i].quad) != 0:
            arg1 = p[i].quad[0]
            op   = p[i].quad[1]
            arg2 = p[i].quad[2]
            container = []
            word = ""
            word += arg1.code
            word += arg2.code
            arg1.code = ""
            arg2.code = ""
            self.patch(arg1, arg2, l_true, l_false, op, container)
            for line in container:
                word += line + "\n"
            word += l_true + " : " + new_temp + " = true;\n"
            word += "goto " + l_next + ";\n"
            word += l_false + " : " + new_temp + " = false;\n"
            word += l_next + " : \n"
            return p[i].code+word
        else:
            word = "if (" + p[i].exp + ") goto " + l_true + ";"
            word += "\ngoto " + l_false + ";\n"
            word += l_true + " : " + new_temp + " = true;\n"
            word += "goto " + l_next + ";\n"
            word += l_false + " : " + new_temp + " = false;\n"
            word += l_next + " : \n"
            return p[i].code+word

    def paramdec_append_tac_generator(self, flag, parameters,p, tmp_list):
        if flag:
            pass
        parameters.reverse()
        i = 0
        for param in parameters:
            p[0].code += tmp_list[i] + " = "+param+";\n"
            p[0].code += param+" = *Top ; \n"
            p[0].code += "Top = Top + 1;\n"
            i = i + 1
        i = 0
        for param in parameters:
            p[0].code += "Top = Top - 1;\n"
            p[0].code += "*Top = " + tmp_list[i] +";\n"
            i = i + 1

    def declist_back_tac_generator(self, flag, parameters, p):
        if flag:
            pass
        parameters.reverse()
        for param in parameters:
            p[0].code+=param+"=*Top "+";\n"
            p[0].code+="Top = Top + 1 ;\n"

    def paramdec_back_tac_generator(self, flag, parameters, p):
        if flag:
            pass
        parameters.reverse()
        for param in parameters:
            p[0].code+=param+"=*Top "+";\n"
            p[0].code+="Top = Top + 1 ;\n"

    def backjmp_tac_generator(self, flag, returnLine,p):
        if flag:
            pass
        p[0].code+="return 0;\n"
        p[0].code+="longjump :\n"
        p[0].code+="gotoTemp = *Top ;\n"
        p[0].code+="Top = Top + 1 ;\n"
        for i in range(returnLine.__len__()):
            p[0].code+="if (gotoTemp == "+str(i)+") goto "+returnLine[i]+";\n"

    def Temp_append_tac_generator(self, flag, parameters, p):
        if flag:
            pass
        for param in parameters:
             p[0].code+="Top = Top - 1 ;\n"
             p[0].code+="*Top = "+param+";\n"






