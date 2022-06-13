"""Manage a sherlock stream session
(not a network server)
"""
from sherlock.sherlock_data.code_data import Line

"""ALGORITHM
    1: setup data structures
    2: start tailing logs in a thread
    3: parse the logs into data structure (maybe with re)
    4: Query/Order by feature
        * get most called function
        * least called function
    5: Group a sequence of calls that are identical 
        eg: a->b->c->d->e->a->b->c->f-e->a
        groups (a->b->c), (e->a)
    6: get list of logs with a range (depending on where 
        the scrollbar is maybe list slicing)
    7: load a lines from a file based on log line #::#::#
        

"""


class SourceView:

    def __init__(self, line: str) -> None:
        self.line = self.parse(line)

    
    def 


if __name__ == '__main__':
    pass