'''Transform/Modiify a python ast node'''
import ast
from sherlock.sherlock_data.code_data import Line

class Transformer:

    def __init__(self, file):
        self._starterFile = file
        super().__init__()

    def traverse(self, node):
        for i in ast.walk(node):
            if isinstance(i, ast.FunctionDef):
                i = self._visitFunctionDef(i)
            if isinstance(i, ast.Module):
                i = self._visitModule(i)

        return node


    def _visitFunctionDef(self, node):
        """ include at the start of a function exec  """
        val = ast.fix_missing_locations(ast.Expr(
                value=ast.Call(
                    func=ast.Name(id="functionCalled", ctx=ast.Load()),
                    args=[],
                    keywords=[ast.keyword(arg='name',value=ast.Constant(value=node.name, ctx=ast.Load(), kind=None)),
                            ast.keyword(arg='line',value=ast.Constant(value=Line().parse(node, self._starterFile), 
                                ctx=ast.Load(), kind=None))
                    ],
                )
            ))
        node.body  = list([val] + node.body)
        return node


    def _visitModule(self, node):
        """ all files changed will have sauce_code visibility"""
        val = ast.fix_missing_locations(ast.ImportFrom(
            module='sherlock.sauce_code',
            names=[ast.alias(name='*', asname=None)],
            level=0)
        )
        node.body  = list([val] + node.body)

        return node