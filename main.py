from classes.lexer import Lexer
from classes.parser import Parser
from classes.toC import ToC

text_input = """
    Program p1Main;
        Int i2 := #34;
        Int i3 := #0;
        Begin
            While i2 .GT. #30 Do
                Begin
                    i3 := i3 + #1;
                    i2 := i2 - #1   
                End;
            Print(i3)
        End;

"""
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
