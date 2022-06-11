import ast

import astpretty

class CodeToAst:

    def __init__(self, filePath) -> None:
        self.filePath = filePath
        self.sourceCode = None
        self.sourceAst = None

    def reader(self):
        with open(self.filePath, 'r') as fileReader:
            self.sourceCode = fileReader.read()

    def convert(self):
        if not self.sourceCode:
            self.reader()
        self.sourceAst = ast.parse(self.sourceCode)
            
    
if __name__ == '__main__':
    code2ast = CodeToAst('/home/victor/workspace/sherlockstream/sherlock/code2ast.py')
    code2ast.convert()
    print(code2ast.sourceCode)
    astpretty.pprint(code2ast.sourceAst)
    import astor
    astor.code_gen.to_source(code2ast.sourceAst)