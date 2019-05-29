import xmltodict
import json
import ast


class nonTerminal:

    def __init__(self, word):
        self.word = word
        self.place = ""
        self.true = ""
        self.false = ""
        self.begin = ""
        self.type = ""
        self.exp = ""
        self.label = ""
        self.code = ''''''
        self.quad = []
        self.parameters = []
        self.number = ""

    # self.otherAttribute=default
    def generate_code(self):
        if self.exp == "":
            return ""
        if self.label != "":
            self.code += self.label + " : "
        self.code += 'if (' + self.exp + ") goto " + self.true + ";\ngoto " + self.false
        return self.code + ";"

    def __str__(self):
        return self.word
