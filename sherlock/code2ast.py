'''Convert python source code to python's Abstract Syntax Tree'''
import ast

import astpretty

class CodeToAst:

    def __init__(self, filePath):
        self.filePath = filePath
        self.sourceCode = None

    def reader(self):
        with open(self.filePath, 'r') as fileReader:
            self.sourceCode = fileReader.read()

    def convert(self):
        if not self.sourceCode:
            self.reader()
        return ast.parse(self.sourceCode)