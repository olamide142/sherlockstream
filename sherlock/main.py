'''Main entry to sherlock stream'''
import os
import sys
import time
import subprocess
import multiprocessing

from sherlock.server import Server
from sherlock.code2ast import CodeToAst
from sherlock.ast2code import AstToCode
from sherlock.import_decoder import getPaths
from sherlock.transformer import Transformer
from sherlock.log4sherlock import Log4Sherlock
from sherlock.sherlock_data.persistence import Log2DB
from sherlock.sherlock_exceptions import EntryFileException
from sherlock.sherlock_data.data_util import getFunctionCalls
from sherlock.utils import backupOriginal, getFullpath, sherlockUnhalt

logger = Log4Sherlock().startLogger()


"""
export PYTHONPATH="${PYTHONPATH}:/home/victor/workspace/sherlockstream"
"""

class _SherlockStream:
    '''Calling Sherlock Stream from source code'''
    def __init__(self, entryFile=None):
        if entryFile is None:
            raise EntryFileException()
        self.entryFile = entryFile
        self.server = None
        self.db = Log2DB.instance()
        self.main(self.entryFile)

        
    def main(self, entryFile):
        # database setup
        
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
                
                backupOriginal(currentFile, modifiedCodePath)

                unparsedFiles = getPaths(currentAst, unparsedFiles)
                parsedFiles.add(currentFile)
        
        #to avoid getting stuck in a recursion
        sherlockUnhalt(entryFile) 

        if os.fork():
            self.runUserCode()
            # self.startServer()
        else:
            self.runUserCode()
        # parent process
        # db.close()
        # sys.exit()

    def runUserCode(self):
        time.sleep(1)
        os.execv(sys.executable, sys.argv)

    def startServer(self):
        self.server = Server(self.db)
        cursor = self.db.getCursor()
        for sql in self.server.poll():
            cursor.execute(sql)
            print(sql)

        self.db.close()


if __name__ == '__main__':
    _SherlockStream(sys.argv[0])
    os.system(" ".join(['python3 '] + sys.argv))