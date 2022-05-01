from sherlock_monkey.sauce_code import *


class Tree:

    def __init__(self, val=None):
        functionCalled(name='__init__', line=
            'sherlock/prototype.py::2::4::8::25')
        if val != None:
            self.val = val
        else:
            self.val = None
        self.left = None
        self.right = None

    def insert(self, val):
        functionCalled(name='insert', line=
            'sherlock/prototype.py::10::4::23::26')
        if self.val:
            if val < self.val:
                if self.left is None:
                    self.left = Tree(val)
                else:
                    self.left.insert(val)
            elif val > self.val:
                if self.right is None:
                    self.right = Tree(val)
                else:
                    self.right.insert(val)
        else:
            self.val = val

    def printValues(self):
        functionCalled(name='printValues', line=
            'sherlock/prototype.py::25::4::30::36')
        if self.left:
            self.left.printValues()
        print(self.val)
        if self.right:
            self.right.printValues()


tree = Tree(20)
tree.left = Tree(18)
tree.right = Tree(22)
tree.insert(19)
tree.insert(24)
tree.insert(5)
tree.insert(21)
tree.printValues()
