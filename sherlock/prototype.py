from ast import *

import astor
import astpretty

from sherlock_monkey.rewrite import Transformer


subscript = """
from sherlock_monkey.sauce_code import *
"""

functionDef = """
def insert(self, val):
    functionVisit('sep', name=name, file=file)
    return 1
"""
tree = parse(open('sherlock/sample.py','r').read())
# tree = parse(subscript)
# astpretty.pprint(tree, show_offsets=0)
new_tree = Transformer(__file__).traverse(tree)
# breakpoint()

# astpretty.pprint(tree, show_offsets=0)
with open('sherlock/sample_result.py', 'w') as f:
    f.write(astor.code_gen.to_source(new_tree))


# import os
# breakpoint()
# for base, directory, files in os.walk('/home/victor'):
#     print(i)