'''Transform/Modiify a python ast node'''
import ast

from sherlock.sherlock_data.persistence import Log2DB, DBFormatter
from sherlock.utils import generateUuid

class Transformer:

    def __init__(self, file, dbSourceCodeId):
        self._starterFile = file
        self.dbSourceCodeId = dbSourceCodeId
        self.db = Log2DB.instance()
        self.sessionId = self.db.getSession()[0]
        super().__init__()

    def traverse(self, node):
        """traverse through the AST"""
        for i in ast.walk(node):

            if isinstance(i, ast.FunctionDef):
                hashId = self.saveNode(DBFormatter.FUNCTION_LOCATION, i)
                i = self._visitFunctionDef(i, hashId)
            
            if isinstance(i, ast.Module):
                i = self._visitModule(i)

        return node

    def saveNode(self, func, node):
        """save a node info to db"""
        if func == DBFormatter.FUNCTION_LOCATION:
            hashId = generateUuid()
            sql = func(node.name, self.dbSourceCodeId, node.lineno,  
            node.col_offset, self.db.getSession()[0], hashId)
            self.db.insertQuery(sql)

            return hashId

    def _visitFunctionDef(self, node, hashId):
        """ include at the start of a function exec  """
        val = ast.fix_missing_locations(ast.Expr(
                value=ast.Call(
                    func=ast.Name(id="functionCalled", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(arg='sessionId',value=ast.Constant(value=self.sessionId, ctx=ast.Load(), kind=None)),
                        ast.keyword(arg='hashId',value=ast.Constant(value=hashId, ctx=ast.Load(), kind=None)),
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
    