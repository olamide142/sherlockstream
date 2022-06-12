import os
import pprint
import pickle

def backupOriginal(original, modified):
    print(original, modified)
    os.rename(original, original+'.ssb') #ssb: sherlock stream backup
    os.rename(modified, original)

def getFullpath(entryFile):
    currentDirectory = os.getcwd()

    if not entryFile.startswith(currentDirectory):
        entryFile = os.path.join(currentDirectory, entryFile)
    
    return entryFile

def sherlockUnhalt(entryFile):
    """ remove Sherlock(__file__) from entryFile """
    


def recoverOriginal(path=None, delete=False):
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