from typing import List

def mapThenList(ll: List, func):
    """ map a function to a list and return a
    list object instead of map object"""
    return list(map(func, ll))