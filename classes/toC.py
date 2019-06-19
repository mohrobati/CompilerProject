import subprocess

class ToC:

    def __init__(self, tmp_ctr, generated_code, symbolTable):
        self.tmp_ctr = tmp_ctr
        self.generated_code = generated_code
        self.symbolTable = symbolTable

    def make_c_code(self):
        code = ""
        code += "#include <stdio.h>\n#include <stdbool.h>\n\n"
        code += "double r1esult ,gotoTemp;\n"
        code += "double "
        for i in range(0, self.tmp_ctr+1):
            code += "TT" + str(i)
            if i != self.tmp_ctr:
                code += ", "
        code += ";\n"
        variables = []
        for table in self.symbolTable:
            for entity in table.entities:
                variables.append(entity.name)
        code += "double "
        i = 0
        for variable in variables:
            code += variable
            if i != len(variables)-1:
                code += ", "
            i = i + 1
        code += ";\n"

        code += "double stack[19000];\ndouble *Top ;\ndouble  returnValue ;\n\nint main() { \n\n"
        code += "Top = stack+18000;\n\n"
        code += self.generated_code
        code += "return 0;\n\n}\n"

        return code

    def write_to_file(self):
        filew= open("output.c","w")
        filew.write(self.make_c_code())
        filew.close()

    def run(self):
        self.write_to_file()
        print('=======================================')
        print('Compiling...')
        cmd = "output.c"
        subprocess.call(["gcc", cmd])
        print("\nOutput:\n")
        subprocess.call("./a.out")
        print("")

