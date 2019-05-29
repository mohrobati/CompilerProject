from classes.lexer import Lexer
from classes.parser import Parser
from classes.toC import ToC

# text_input = """
#     Program p1Main;
#         Bool a1;
#         Function f1actoriel(Int i1) : Bool
#             Begin
#                 Return True
#             End;
#         Begin
#             a1 := #3 .LT. #4 Or Else #43 .EQ. #34;
#             Print(a1)
#         End;
#++++++++++++++++++++++
# """
filer = open("test-cases/function/comb", "r")
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
