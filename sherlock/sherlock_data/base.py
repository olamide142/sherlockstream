from collections import deque
from base import File, Id, Line


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