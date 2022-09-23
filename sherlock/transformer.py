from __future__ import annotations
'''Transform/Modiify a python ast node'''
import ast
import inspect
import functools
from sherlock.utils import function_finder, module_has_future
# from sherlock.net.dispatcher import Dispatcher

# dispatcher = Dispatcher()

def convert_file_to_ast(file_path):
    return ast.parse(open(file_path, 'r').read())


def sherlock_yellow(func):
    """yellow markers at crime scenes
    https://static01.nyt.com/images/2010/08/12/nyregion/20100812marker-cityroom/20100812marker-cityroom-blogSpan.jpg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(str(func.__name__))
        #breakpoint()
        # dispatcher.write(str(func.__name__))
        return func(*args, **kwargs)
    return wrapper


def file_has_function(lines):
    """See if a file has python function"""
    for line in lines:
        if 'def ' in line:
            return True
    return False


def indent_and_add(indent_length):
    return f"{' ' * indent_length}@sherlock_yellow\n"


def function_decorator(source_file):
    """Include the sherlock function decorator
    all functions in source_file"""

    decorated = 0 #number of decorated functions in a file
    code_string = ""

    with open(source_file, 'r') as f:
        code_string = f.read()

    marker_import = "from sherlock.transformer import sherlock_yellow\n"
    functions = function_finder(code_string)
    has_future = module_has_future(code_string)
    marker_imported = False
    first_import_line = 0
    if len(functions):
            
        with open(source_file, 'w') as f:

            for index, line in enumerate(code_string.split('\n'), start=1):
                # if file uses the __future__ module, 
                # import yellow_marker on the next line
                    
                if all([
                        len(functions), 
                        (not has_future), 
                        (not marker_imported)
                    ]):
                    f.write(marker_import)
                    marker_imported = True
                elif has_future and index > first_import_line:
                    f.write(marker_import)
                    marker_imported = True

                function = functions[0] if len(functions) else 0

                if function and (index == function.get('line_number')):
                    column_offset = function.get('column_offset')
                    f.write(indent_and_add(column_offset))
                    functions.pop(0)
                    decorated += 1
                    
                f.write(f"{line}\n")    
                
    return decorated

