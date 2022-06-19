'''Decode python import statements to file'''
import ast
import sys
import os

def getImportNodes(nodes):
    for node in ast.walk(nodes):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            yield node

def isPython(file):
    return file and file.endswith('.py')


def filterImports(path):

    return path and all([
        isPython(path),
        '/usr/lib/python3.8' not in path,
        '/sherlockstream/sherlock' not in path,
        # '/venv/' not in path
    ])

def getPaths(nodes, setToReturn=set()):

    for node in getImportNodes(nodes):

        module = vars(node).get('module', None)
        
        if module:
            modulePath = findModule(module)
            if not modulePath: continue

            setToReturn.add(modulePath)
            setToReturn = loadModule(node, modulePath, setToReturn)
        
            for name in node.names:
                modulePath = findModule(name.name)

                setToReturn.add(modulePath)
                modulePath = findModule(module)
                if not modulePath: continue
                setToReturn = loadModule(node, modulePath, setToReturn)

        else:
            for name in node.names:
                setToReturn.add(findModule(name.name))
    return set(filter(filterImports, setToReturn))

def loadModule(node, modulePath, setToReturn):

    for name in node.names:
        name = name.name + '.py'
        joinedName = os.path.join(modulePath, name)

        if os.path.isfile(joinedName):
            setToReturn.add(joinedName)
        if os.path.isfile(modulePath+'/__init__.py'):
            setToReturn.add(modulePath+'/__init__.py')

    return setToReturn

def findModule(module):
    module = module.replace('.', '/')
    for path in reversed(sys.path):
        joinedPath = os.path.join(path, module)

        if os.path.isdir(joinedPath) or os.path.isfile(joinedPath+'.py'):
            return joinedPath+'.py' \
                if os.path.isfile(joinedPath+'.py') else joinedPath
    return None

if __name__ == '__main__':
        
    from sherlock.code2ast import CodeToAst
    decoder = getPaths(CodeToAst('/home/victor/workspace/sherlockstream/sherlock/__init__.py').convert())
    # ast.parse('from sherlock import ast'),set())
    import pprint
    pprint.pprint(decoder)