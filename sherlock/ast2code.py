import tempfile
import astor


class AstToCode:

    def __init__(self, astObject):
        self.astObject = astObject

    def convert(self, path=None):
        file = None
        if not path:
            _ = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
            path = _.name

        with open(path, 'w') as f:
            f.write(astor.code_gen.to_source(self.astObject))

        return path
        
if __name__ == '__main__':
    from sherlock import code2ast
    aa = code2ast.CodeToAst('/home/victor/workspace/sherlockstream/sherlock/code2ast.py')
    aa.convert()
    AstToCode.convert(aa.sourceAst)