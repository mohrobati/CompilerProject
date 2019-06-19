from ply import lex


class Lexer():
    tokens = [
        'END', 'DO', 'LE', 'GT', 'SEPARATOR', 'PROCEDURE', 'INT',
        'PROGRAM', 'FOR', 'SUM', 'TO', 'COLON', 'REAL',
        'IF', 'WHILE', 'OPEN_PAREN', 'OR', 'TRUE', 'AND', 'MUL',
        'SUB', 'THEN', 'FUNCTION', 'CLOSE_PAREN', 'DIV', 'ELSE',
        'EQ', 'FALSE', 'SEMI_COLON', 'RETURN', 'BOOL', 'LT',
        'BEGIN', 'ID', 'CASE', 'DOWNTO', 'GE', 'NE', 'INTEGER', 'REALNUMBER',
        'ASSIGN', 'PRINT'  # 'ERROR'
    ]
    reserved = {
        # Conditional
        'If': 'IF',
        'Then': 'THEN',
        'Else': 'ELSE',
        # Loops
        'For': 'FOR',
        'While': 'WHILE',
        # Types
        'Int': 'INT',
        'Bool': 'BOOL',
        'Real': 'REAL',
        # Other Keywords
        'Program': 'PROGRAM',
        'Print': 'PRINT',
        'To': 'TO',
        'True': 'TRUE',
        'False': 'FALSE',
        'Downto': 'DOWNTO',
        'Do': 'DO',
        'Return': 'RETURN',
        'Case': 'CASE',
        'Function': 'FUNCTION',
        'Procedure': 'PROCEDURE',
        'Begin': 'BEGIN',
        'End': 'END',
    }
    # Assign
    t_ASSIGN = r':='
    # Colons
    t_SEMI_COLON = r'\;'
    t_COLON = r'\:'
    t_SEPARATOR = r'\,'
    # Parenthesis
    t_OPEN_PAREN = r'\('
    t_CLOSE_PAREN = r'\)'
    # Operators
    t_SUM = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_EQ = r'\.EQ\.'
    t_LT = r'\.LT\.'
    t_GT = r'\.GT\.'
    t_GE = r'\.GE\.'
    t_LE = r'\.LE\.'
    t_NE = r'\.NE\.'

    def t_AND(self, t):
        r'And\sThen\b'
        return t

    def t_OR(self, t):
        r'Or\sElse\b'
        return t

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        if t.type == 'ID' and (t.value.__len__() < 2 or not t.value[1] in {'0', '1', '2', '3'
                                                                           , '4', '5', '6', '7'
                                                                           , '8', '9'}):
            raise Exception('SyntaxError: invalid syntax at ', t.value[0])
        return t

    def t_TRUE(self, t):
        r'True'
        t.value = True
        return t

    def t_FALSE(self, t):
        r'False'
        t.value = False
        return t

    def t_ERROR(self, t):
        r"""(\#[a-zA-Z0-9_\?\#]*[a-df-zA-Df-z\#]+[0-9a-zA-Z_\?\#]*)
        | ([a-zA-Z0-9_\?\#]*\#[a-zA-Z0-9_\?\#]*[a-df-zA-Df-z\#]+[0-9a-zA-Z_\?\#]*)
        | ([a-zA-Z0-9_\?\#]+\#[a-zA-Z0-9_\?\#]*[a-df-zA-Df-z\#]*[0-9a-zA-Z_\?\#]*)
        | (\#[0-9\.]*[\#]+[0-9\.\#]*)
        | (\#[- \+]?0([1-9]\d*|0))
        | (\#[- \+]?0([1-9]\d*|0)\.(\d*[1-9]|0)((E|e)[- \+]?([1-9]\d*|0))?[\s\n]+)
        | (\#[- \+]?0([1-9]\d*|0)(E|e)[- \+]?([1-9]\d*|0)[\s\n]+)
        | (\#[- \+]?([1-9]\d*|0)\.(\d*[1-9]|0)((E|e)[- \+]?([1-9]\d*|0))?0[\s\n]+)
        | (\#[- \+]?([1-9]\d*|0)(E|e)[- \+]?([1-9]\d*|0)0[\s\n]+)
        """
        raise Exception('SyntaxError: invalid syntax at ', t.value[0])

    def t_REALNUMBER(self, t):
        r"""\#[- \+]?([1-9]\d*|0)\.(\d*[1-9]|0)((E|e)[- \+]?([1-9]\d*|0))?'
           | \#[- \+]?([1-9]\d*|0)(E|e)[- \+]?([1-9]\d*|0)
           | \#[- \+]?([1-9]\d*|0)\.(\d*[1-9]|0)((E|e)[- \+]?([1-9]\d*|0))?
           | \#[- \+]?([1-9]\d*)\.(\d*[1-9]|0)((E|e)[- \+]?([1-9]\d*|0))
           | \#[- \+]?([1-9]\d*|0)\.(\d*[1-9])((E|e)[- \+]?([1-9]\d*|0))
           | \#[- \+]?([1-9]\d*|0)(E|e)[- \+]?([1-9]\d*|0)"""
        t.value = float(t.value[1:])
        return t

    def t_INTEGER(self, t):
        r'\#[- \+]?([1-9]\d*|0)'
        t.value = int(t.value[1:])
        return t

    def t_error(self, t):
        raise Exception('SyntaxError: invalid syntax at ', t.value[0])

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = '\n \t\r\f\v'

    def build(self, **kwargs):
        '''
        build the lexer
        '''
        self.lexer = lex.lex(module=self, **kwargs)

        return self.lexer
