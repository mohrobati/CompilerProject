from classes.tools.symbolTable import SymbolTable
from classes.tools.entity import Entity


class DictTraversal:
    # {'program':
    #  {'PROGRAM':
    #  'Program', 'ID':
    #  'p1Main', 'SEMI_COLON':
    #  [';', ';'], 'block':
    #  {'BEGIN':
    #  'Begin', 'stmtlist':
    #  {'stmt':
    #  {'exp':
    #  {'VALUE':
    #  '2'}}}, 'END':
    #  'End'}}}
    def __init__(self, main_dic):
        self.dic = main_dic
        self.scopeStack = []
        self.tables = []
        self.tmpType = ''
        self.isAuthorized = True
        self.tmpAddress = 0

    def search_for_vars(self, dic, symbolTable):
        for key, value in dic.items():
            if key == "procdec":
                self.hit_another_table(value, 'Procedure')
            elif key == 'funcdec':
                self.hit_another_table(value, 'Function')
            elif key == 'type':
                for val in value.values():
                    self.tmpType = val
            elif key == 'FUNCTION' or key == 'PROCEDURE':
                self.isAuthorized = False
            elif key == 'ID':
                if self.isAuthorized:
                    varSize = 4
                    if self.tmpType == 'Real':
                        varSize = 8
                    elif self.tmpType == 'Bool':
                        varSize = 1
                    self.scopeStack[len(self.scopeStack) - 1].entities.append(
                        Entity(value, 'Var', self.tmpType, varSize, self.tmpAddress, None))
                    self.tmpAddress += varSize
                    symbolTable.size += varSize
                else:
                    self.isAuthorized = True
            elif type(value) == dict and key != 'block':
                self.search_for_vars(value, symbolTable)

    def hit_another_table(self, value, entityType):
        returnType = None
        if entityType == 'Function':
            for val in value['type'].values():
                returnType = val
        self.scopeStack[len(self.scopeStack) - 1].entities.append(Entity(value['ID'], entityType, None, None, self.tmpAddress, returnType))
        newSymbolTable = SymbolTable(value['ID'], 0, 0, None)
        self.scopeStack.append(newSymbolTable)
        self.search_for_vars(value, newSymbolTable)
        newSymbolTable.outerScopeAddress = self.scopeStack[len(self.scopeStack) - 2].entities[0].address
        self.scopeStack[len(self.scopeStack) - 1].address = self.scopeStack[len(self.scopeStack) - 1].entities[0].address
        self.tables.append(newSymbolTable)
        self.scopeStack.pop()

    def maketables(self):
        programSymbolTable = SymbolTable(self.dic["program"]["ID"], 0, 0, None)
        self.scopeStack.append(programSymbolTable)
        if 'declist' in self.dic["program"].keys():
            self.search_for_vars(self.dic["program"]["declist"], programSymbolTable)
        else:
            self.search_for_vars(self.dic["program"]["block"], programSymbolTable)
        self.tables.append(programSymbolTable)
        self.scopeStack.pop()
