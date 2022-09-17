import os
import uuid
import time
import shutil
import ast

from .import_decoder import is_python

def generateUuid():
    return "".join(str(uuid.uuid4()).split('-'))


def function_finder(code_string):
    """get function line number and colum offsets"""
    results = []
    code_ast = ast.parse(code_string)

    for node in ast.walk(code_ast):
        if isinstance(node, ast.FunctionDef):
            results.append({'name':node.name,
                  'column_offset': node.col_offset,
                  'line_number': node.lineno
                })
            
    return results


def backup_original(original):
    shutil.copyfile(original, original+'.ssb') #ssb: sherlock stream backup


def get_full_path(entryFile):
    currentDirectory = os.getcwd()

    if not entryFile.startswith(currentDirectory):
        entryFile = os.path.join(currentDirectory, entryFile)
    
    return entryFile


def sherlock_unhalt(entryFile):
    """ remove Sherlock(__file__) from entryFile """
    # FIXME: this should be done via ast, not this way
    with open(entryFile, 'r') as f:
        sourceCode = f.read()
        sourceCode = sourceCode.replace('Sherlock(__file__)', '')

    with open(entryFile, 'w') as f:
        print(sourceCode, file=f) 


def recover_original(files):
    for file in files:
        if os.path.isfile(file+'.ssb'):
            os.rename(file+'.ssb', file)
    print('[+] Done Recovering Original Files')


def hard_recover(directory):
    """Give me a path and i will rename all files 
    with .sbb extension to just .py"""
    for i in os.listdir(directory):
        full_path = os.path.join(directory, i)

        if os.path.isdir(full_path):
            hard_recover(full_path)
        elif full_path.endswith('.py.ssb'):
            if not "/home/lams/workspace/flask/venv/lib/python3.10/site-packages/markupsafe/__init__.py" in full_path:
                os.rename(full_path, full_path[0:-4])
                print(f"Recovered {full_path}")
    __import__('sys').exit(0)


def add_neighbours(current_file, unparsed_files, parsed_files):
    """Get all python files in the current level of a directory"""
    base_dir = os.path.dirname(current_file)

    for file in os.listdir(base_dir):
        path  = os.path.join(base_dir, file)

        if is_python(file) and path not in parsed_files:
            unparsed_files.add(path)
    
    return unparsed_files


def tailLog(file, sleep_sec=0.1):
    """ https://stackoverflow.com/questions/12523044/how-can-i-tail-a-log-file-in-python
    Yield each line from a file as they are written.
    `sleep_sec` is the time to sleep after empty reads. """
    line = ''
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ''
        elif sleep_sec:
            time.sleep(sleep_sec)


def tailLogUtil(logPath='sherlock.log'):
    with open(logPath, 'r') as file:
        for line in tailLog(file):
            print(line, end='')
