from uuid import uuid4
from collections import deque


class SherlockStreamBase(object):

    def __init__(self):
        self.id  = uuid4()
    
    def __repr__(self):
        return f"{str(self.id)}"


class SherlockStreamDataType(SherlockStreamBase):
    
    def __init__(self, object_name, object_type=None):
        self.object_name = object_name
        self.object_type = object_type
        super().__init__()


class SherlockStreamVariable(SherlockStreamDataType):

    def __init__(self, object_name, val, object_type):
        self.val = val
        super().__init__(object_name,object_type)

class SherlockStreamFrame(object):

    def __init__(self, filename, line_number):
        self.filename = filename
        self.line_number = line_number
        self.ast_dump = None


class Stack(object):

    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def size(self):
        return len(self.stack)

    def pop(self):
        if len(self.stack()) > 0:
            self.stack.pop(-1)
        else:
            raise IndexError("Stack is empty")

    def peek(self):
        if len(self.stack()) > 0:
            return self.stack[-1]
        else:
            raise IndexError("Stack is empty")
