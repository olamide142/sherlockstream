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
        if "ExceptionPexpect" in self.last_output.lower():
            return u"\r\nn"
        else:
            return u"\r\nn"

    def get_recent_io(self):
        temp = str(self.last_output).splitlines()#+self.last_input.strip()
        temp[-1] = temp[-1] + str(self.last_input.strip())

        return {'last_output': "\r\n".join(temp), 'last_input': self.last_input}

