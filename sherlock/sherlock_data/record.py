from sherlock_data.data import Id

class Recorder(object):
    _instance = None
    _file = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, file=None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._file = cls.getFile(file)
        return cls._instance

    @classmethod
    def getFile(cls, file=None):
        
        if not cls._file:
            retVal = Id()
        else:
            retVal = file or cls._file

        return str(retVal)        

if __name__ == '__main__':
    l = Recorder.instance()
    ll = Recorder.instance()
    print(l.getFile())
    print(ll.getFile())