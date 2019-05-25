from classes.lexer import Lexer
from classes.parser import Parser
# i2 = −23
# T0 = 2 − 1
# T1 = 3 / T0
# T2 = 0−T1
# i3 = T2
# T3 = 23.003 + i1
# r1var = T3
# i1 = i2
# i2 = i3
# T4 = i1/i2
# i1 = T4
# i2 = i3
# i1 = i3
text_input = """
    Program p1Main;
        Begin
            	i2:=f1e(#11,i8,o9+#0,Q1,#10 - #2);
            	Return i1*#9 - y6
        End;
"""
lexer = Lexer().build()
parser = Parser()
parser.build().parse(text_input, lexer, False)

# for table in parser.symbolTables:
#     print(table.name, ':')
#     for entity in table.entities:
#         print(entity.name, entity.entityType, entity.varType, entity.size, entity.address, entity.returnType)
#     print('-------')
#
# for table in parser.symbolTables:
#     print(table.name, table.address, table.size, table.outerScopeAddress)

# if (a1 < b1) goto LL4;
# goto LL0;
# LL0 : if (c1 < d1) goto LL3;
# goto LL5;
# LL3 : if (e1 < f1) goto LL4;
# goto LL2;
# LL2 : if (g1 < h1) goto LL1;
# goto LL5;
# LL1 : if (i1 < j1) goto LL4;
# goto LL5;
# LL4 : t1 = true;
# goto LL6;
# LL5 : t1 = false;
# LL6 :
