import os
import uuid
import time
import pickle
import logging

def generateUuid():
    return "".join(str(uuid.uuid4()).split('-'))

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

def recoverOriginal(db):
    print('[+] Recovering Original Files')
    cursor = db.getCursor()
    files = cursor.execute(f"""select file_path from source_code where session_id={db.getSession()[0]}""")
    for file in files:
        file = file[0]
        if os.path.isfile(file+'.ssb'):
            os.rename(file+'.ssb', file)
    print('[+] Done Recovering Original Files')
    
    
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
