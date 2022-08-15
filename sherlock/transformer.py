'''Transform/Modiify a python ast node'''
import ast
import inspect
import functools

from sherlock.sherlock_data.persistence import Log2DB, DBFormatter
from sherlock.utils import generateUuid
from sherlock.net.dispatcher import Dispatcher


def convert_file_to_ast(file_path):
    return ast.parse(open(file_path, 'r').read())


def sherlock_yellow(func):
    """yellow markers at crime scenes
    https://static01.nyt.com/images/2010/08/12/nyregion/20100812marker-cityroom/20100812marker-cityroom-blogSpan.jpg
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dispatcher = Dispatcher.instance()
        _ = dispatcher.write(func.__name__)
        # TODO:Get all the info needed and pass 
        # info to sherlock server here
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

