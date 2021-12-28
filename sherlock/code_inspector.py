import inspect
from sherlock_struct.data import Stack


class CodeInspector():

    def __init__(self):
        self.last_output = None
        self.last_input = None
        self.stack = Stack()


    def next_input(self):
        if self.last_output is None:
            self.last_input = u"\r\nn"
            return self.last_input
        else:
            return u"\r\nn"

    def get_recent_io(self):
        return {'last_output': self.last_output, 'last_input': self.last_input}

