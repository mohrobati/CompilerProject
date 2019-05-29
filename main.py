from classes.lexer import Lexer
from classes.parser import Parser
from classes.toC import ToC

text_input = """
    Program p1Main;
        Bool b2;
        Begin
            b2 := #10 And Then #-1 And Then #0;
            Print(b2)
        End;
"""

# filer = open("test-cases/arithmetic/arith_1.txt", "r")                     #3.454545
# filer = open("test-cases/arithmetic/arith_2.txt", "r")                     #16
# filer = open("test-cases/arithmetic/arith_3.txt", "r")                     #655
# filer = open("test-cases/boolean/bool_all_simple.txt", "r")                #1,0,35,100,37,90
# filer = open("test-cases/boolean/bool_all_advance.txt", "r")               #12,0,0
# filer = open("test-cases/function/func_simple.txt", "r")                   #400,10
# filer = open("test-cases/function/func_advanced.txt", "r")                 #32
# filer = open("test-cases/function/func_super_advanced.txt", "r")           #3628800,512
# filer = open("test-cases/complete-programs/mean.txt", "r")                 #5
# filer = open("test-cases/complete-programs/even-or-odd.txt", "r")          #1
# filer = open("test-cases/complete-programs/bit_op.txt", "r")               #0
# filer = open("test-cases/complete-programs/factoriel.txt", "r")
# filer = open("test-cases/complete-programs/fibonacci.txt", "r")
# filer = open("test-cases/complete-programs/comb.txt", "r")
# text_input = filer.read()
# filer.close()

lexer = Lexer().build()
parser = Parser()
parser.build().parse(text_input, lexer, False)
to_c = ToC(parser.t_ctr, parser.generatedCode, parser.symbolTables)
to_c.run()


# for table in parser.symbolTables:
#     print(table.name, ':')
#     for entity in table.entities:
#         print(entity.name, entity.entityType, entity.varType, entity.size, entity.address, entity.returnType)
#     print('-------')
#
# for table in parser.symbolTables:
#     print(table.name, table.address, table.size, table.outerScopeAddress)
