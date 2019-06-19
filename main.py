from classes.lexer import Lexer
from classes.parser import Parser
from classes.toC import ToC

# text_input = """
#     Program p1Main;
#         Bool b2;
#         Begin
#             b2 := #10 And Then #-1 And Then #0;
#             Print(b2)
#         End;
# """

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
# filer = open("test-cases/complete-programs/factoriel.txt", "r")            #3628800
# filer = open("test-cases/complete-programs/fibonacci.txt", "r")            #1,1,2,3,5,8,13,21,34,55
# filer = open("test-cases/complete-programs/comb.txt", "r")                 #184756
# filer = open("test-cases/sample/factorial.txt", "r")                       #120
# filer = open("test-cases/sample/boolean.txt", "r")                         #15,3,35,15,0,38
# filer = open("test-cases/sample/calculator.txt", "r")                      #-1,-4
# filer = open("test-cases/sample/fibonachi.txt", "r")                       #102334155
filer = open("test-cases/sample/arithmetic.txt", "r")                      #15,3,35

text_input = filer.read()
filer.close()

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
