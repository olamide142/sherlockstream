from ast import *

import astor
import astpretty

from sherlock_monkey.rewrite import RewriteFunctionDef


subscript = """
from sherlock_monkey.sauce_code import *
"""

functionDef = """
def insert(self, val):
    functionVisit('sep', name=name, file=file)
    return 1
"""
tree = parse(open('sample.py','r').read())
# tree = parse(subscript)
# astpretty.pprint(tree, show_offsets=0)
new_tree = fix_missing_locations(RewriteFunctionDef(__file__).visit(tree))
# astpretty.pprint(tree, show_offsets=0)
with open('sample_result.py', 'w') as f:
    f.write(astor.code_gen.to_source(new_tree))


# import os
# breakpoint()
# for base, directory, files in os.walk('/home/victor'):
#     print(i)