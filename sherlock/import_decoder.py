'''Decode python import statements to file'''
import ast
import sys
import os

import astpretty

import sherlock

def getImportNodes(nodes):
    for node in ast.walk(nodes):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            yield node

def getPaths(nodes, entryPath, setToReturn=set()):
    for node in getImportNodes(nodes):
        # astpretty.pprint(node)
        module = vars(node).get('module')
        if not module:
            #check the names
            ...
        elif not module.startswith('sherlock'):
            print(findModule(module))
    return setToReturn


def findModule(module):
    module = module.replace('.', '/')
    for path in reversed(sys.path):
        joinedPath = os.path.join(path, module)
        if os.path.isdir(joinedPath) or os.path.isdir(joinedPath+'.py'):
            return joinedPath
        

# decoder = getPaths(ast.parse('from sherlock import ast'))
