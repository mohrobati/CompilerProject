class SymbolTable:

    def __init__(self, name, address, size, outerScopeAddress):
        self.name = name
        self.address = address
        self.size = size
        self.outerScopeAddress = outerScopeAddress
        self.entities = []
