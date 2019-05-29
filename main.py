from classes.lexer import Lexer
from classes.parser import Parser
from classes.toC import ToC

text_input = """
    Program p1Main;
        Int a1 := #2;
        
        Function f1actoriel(Int i1) : Int 
        Begin
            If i1 .LE. #1 Then 
                Return #1;
            Return i1*f1actoriel(i1-#1) 
        End;
        
        Begin
         r1esult:=f1actoriel(#5) + a1;
            Print(r1esult)
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
