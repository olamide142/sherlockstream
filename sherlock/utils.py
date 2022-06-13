import os
import time
import pickle
import logging

def backupOriginal(original, modified):
    print(original)
    os.rename(original, original+'.ssb') #ssb: sherlock stream backup
    os.rename(modified, original)

def getFullpath(entryFile):
    currentDirectory = os.getcwd()

    if not entryFile.startswith(currentDirectory):
        entryFile = os.path.join(currentDirectory, entryFile)
    
    return entryFile

def sherlockUnhalt(entryFile):
    """ remove Sherlock(__file__) from entryFile """
    # FIXME: this should be done via ast, not this way
    with open(entryFile, 'r') as f:
        sourceCode = f.read()
        sourceCode = sourceCode.replace('Sherlock(__file__)', '')

    with open(entryFile, 'w') as f:
        print(sourceCode, file=f) 

def recoverOriginal(path=None, delete=False):
    logging.info('[+] Recovering Original Files')
    if not path:
        path = 'sherlock_parsed_files.sherlock'
        delete = True
    
    with open(path, 'rb') as f:
        files = pickle.load(f)
        for file in files:
            if os.path.isfile(file+'.ssb'):
                os.rename(file+'.ssb', file)
    
    if delete: os.remove(path)

def saveParsedFiles(parsedFiles):

    with open('sherlock_parsed_files.sherlock', 'wb+') as f: 
        f.write(
            pickle.dumps(parsedFiles)
        )


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
