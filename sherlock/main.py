'''Main entry to sherlock stream'''
import os
import sys
from sherlock import transformer

from sherlock.code2ast import CodeToAst
from sherlock.transformer import Transformer
from sherlock.import_decoder import getPaths

"""ALGORITHM
    1: halt the users process
    2: once in control get the entry file name
    3: parse file to currentAst
    4: transform/modify currentAst
    5: convert currentAst back to python code
    6: update the file with the new modified code 
    7: get imports from currentAst
    8: decode the file path of code to be imported
    9: if done traversing all the required source code for 
        the run jump to step 8 else jump back to step 3
    10: make sure entry file for the execution no longer 
        halt else we are going to be stucked in a loop
    11: create a subprocess to run users modified code
    12: start SherlockServer to inspect a sherlock run session
    
    export PYTHONPATH="${PYTHONPATH}:/home/victor/workspace/sherlockstream"
"""
class _SherlockStream:
    '''Calling Sherlock Stream from source code'''
    def __init__(self, entryFile):
        self.entryFile = entryFile
        main(self.entryFile)

def getFullpath(entryFile):
    currentDirectory = os.getcwd()

    if not entryFile.startswith(currentDirectory):
        entryFile = os.path.join(currentDirectory, entryFile)
    return entryFile


def main(entryFile):
    entryFile = getFullpath(entryFile)
    parsedFiles = set()
    unparsedFiles = set() 
    unparsedFiles.add(entryFile)

    while len(unparsedFiles):
        
        currentFile = unparsedFiles.pop()

        if currentFile not in parsedFiles:
            converter = CodeToAst(currentFile)
            currentAst = converter.convert()
            transformer = Transformer(currentFile)
            transformedAst = transformer.traverse(currentAst)
            
            parsedFiles = getPaths(currentAst, entryFile, parsedFiles)
            parsedFiles.add(currentFile)
    return 0


if __name__ == '__main__':
    import pprint
    pprint.pprint(sys.modules)
    raise SystemExit(main(sys.argv[0]))