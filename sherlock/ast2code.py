import tempfile
import ast

import astor


class AstToCode:

    @staticmethod
    def convert(astObject: ast.AST, path=None):
        file = None
        if not path:
            _ = tempfile.NamedTemporaryFile(delete=True, suffix='.py')
            path = _.name

        with open(path, 'w') as f:
            f.write(astor.code_gen.to_source(astObject))

        return path
        
if __name__ == '__main__':
    from sherlock import code2ast
    aa = code2ast.CodeToAst('/home/victor/workspace/sherlockstream/sherlock/code2ast.py')
    aa.convert()
    AstToCode.convert(aa.sourceAst)