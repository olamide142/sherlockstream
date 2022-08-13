'''Transform/Modiify a python ast node'''
import ast
import inspect
import functools

from sherlock.sherlock_data.persistence import Log2DB, DBFormatter
from sherlock.utils import generateUuid
# from sherlock.server.dispatcher import main

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


def convert_file_to_ast(file_path):
    return ast.parse(open(file_path, 'r').read())


def sherlock_yellow(func):
    """yellow markers at crime scenes
    https://static01.nyt.com/images/2010/08/12/nyregion/20100812marker-cityroom/20100812marker-cityroom-blogSpan.jpg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # TODO:Get all the info needed and pass 
        # info to sherlock server here
        # main(str(func))
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

def get_indent_length(line):
    indent_size = 0
    for character in line:
        if character == ' ':
            indent_size += 1
        else: break
    return indent_size

def file_has_function(lines):
    for line in lines:
        if 'def ' in line:
            return True
    return False


def indent_and_add(line):
    return f"{' '*get_indent_length(line)}@sherlock_yellow\n"


def function_decorator(source_file):
    """Include the sherlock function decorator
    all functions in source_file"""

    decorated = 0
    ccode = []

    with open(source_file, 'r') as f:
        ccode = f.readlines()

    with open(source_file, 'w') as f:
        
        if file_has_function(ccode):
            f.write("from sherlock.transformer import sherlock_yellow\n")

        for line in ccode:

            # if line.strip().startswith('@') and not seen:
            #     seen = True
            #     f.write(indent_and_add(line))
            if line.strip().startswith(('def ', 'async def ')):
                f.write(indent_and_add(line))

            decorated += 1
            f.write(line)
    
    return decorated

