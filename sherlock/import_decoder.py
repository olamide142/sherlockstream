'''Decode python import statements to file'''
import ast
import sys
import os

# from sherlock.config_parser import get_config

def get_import_nodes(nodes):
    for node in ast.walk(nodes):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            yield node


def is_python(file):
    return file and file.endswith('.py')


def filter_imports(path):

    return path and all([
        is_python(path),
        '/usr/lib/' not in path, #avoid debgging python stdlib modules
        '/sherlockstream/sherlock' not in path,
        # '/venv/' not in path
    ])


def load_module(node, modulePath, setToReturn):

    for name in node.names:
        name = name.name + '.py'
        joinedName = os.path.join(modulePath, name)

        if os.path.isfile(joinedName):
            setToReturn.add(joinedName)
        if os.path.isfile(modulePath+'/__init__.py'):
            setToReturn.add(modulePath+'/__init__.py')

    return setToReturn


def find_module(module):
    module = module.replace('.', '/')
    for path in reversed(sys.path):
        joinedPath = os.path.join(path, module)

        if os.path.isdir(joinedPath) or os.path.isfile(joinedPath+'.py'):
            return joinedPath+'.py' \
                if os.path.isfile(joinedPath+'.py') else joinedPath
    return None


def get_paths(nodes, setToReturn=set()):

    """Get list of related python files for the run """
    for node in get_import_nodes(nodes):

        module = vars(node).get('module', None)
        
        if module:
            modulePath = find_module(module)
            if not modulePath: continue

            setToReturn.add(modulePath)
            setToReturn = load_module(node, modulePath, setToReturn)
        
            for name in node.names:
                modulePath = find_module(name.name)

                setToReturn.add(modulePath)
                modulePath = find_module(module)
                if not modulePath: continue
                setToReturn = load_module(node, modulePath, setToReturn)

        else:
            for name in node.names:
                setToReturn.add(find_module(name.name))
    
    return set(filter(filter_imports, setToReturn))