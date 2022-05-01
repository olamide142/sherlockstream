from sherlock_data.record import Recorder
from sherlock_data.sherlock_types import FunctionCall

""" Helper code to be injected into primary source """
def functionCalled(name, line):
    recorder = Recorder.instance()
    with open(recorder.getFile(), 'a') as f:
        f.write(
            str(FunctionCall(name, line))+
            '\n'
        )

