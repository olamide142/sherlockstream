'''Main entry to sherlock stream'''
import os
import sys
import subprocess

from sherlock.log4sherlock import Log4Sherlock
from sherlock.sherlock_data.persistence import Log2DB
from sherlock.code2ast import CodeToAst
from sherlock.ast2code import AstToCode
from sherlock.transformer import Transformer
from sherlock.import_decoder import getPaths
from sherlock.sherlock_exceptions import EntryFileException
from sherlock.sherlock_data.data_util import getFunctionCalls
from sherlock.utils import backupOriginal, getFullpath, recoverOriginal, \
    sherlockUnhalt, recoverOriginal

logger = Log4Sherlock().startLogger()


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
        the run jump to step 10 else jump back to step 3
    10: make sure entry file for the execution no longer 
        halt else we are going to be stucked in a loop
    11: create a subprocess to run users modified code
    12: start SherlockServer to inspect a sherlock run session
    
    export PYTHONPATH="${PYTHONPATH}:/home/victor/workspace/sherlockstream"
"""

class _SherlockStream:
    '''Calling Sherlock Stream from source code'''
    def __init__(self, entryFile=None):
        if entryFile is None:
            raise EntryFileException()
        self.entryFile = entryFile
        main(self.entryFile)


def cleanUp(db):
    db.save()
    print("[+] Done with cleanUp")
    os.posix_spawn("")

def main(entryFile):
    # database setup
    db = Log2DB.instance()
    db.setUp()
    
    entryFile = getFullpath(entryFile)
    parsedFiles = set()
    unparsedFiles = set() 
    unparsedFiles.add(entryFile)

    while len(unparsedFiles) > 0:
        currentFile = unparsedFiles.pop()
        if currentFile not in parsedFiles:
            
            codeConverter = CodeToAst(currentFile)
            currentAst = codeConverter.convert()
            dbSourceCodeId = codeConverter.saveFile()

            transformer = Transformer(currentFile, dbSourceCodeId)
            transformedAst = transformer.traverse(currentAst)

            astConvert = AstToCode(transformedAst)
            modifiedCodePath = astConvert.convert()
            # os.remove(modifiedCodePath)
            
            backupOriginal(currentFile, modifiedCodePath)

            unparsedFiles = getPaths(currentAst, unparsedFiles)
            parsedFiles.add(currentFile)
    
    sherlockUnhalt(entryFile)
    subprocess.check_call([sys.executable, *sys.argv])
    cleanUp(db)
    getFunctionCalls(db)    
    recoverOriginal(db)
    db.close()



if __name__ == '__main__':
    main(sys.argv[0])
    os.system(" ".join(['python3 '] + sys.argv))