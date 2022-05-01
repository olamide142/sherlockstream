from ast import *

from sherlock_data.data import Line

class RewriteBase(NodeTransformer):

    def __init__(self) -> None:
        super().__init__()

    def generic_visit(self, node):
        """ all files changed will have sauce_code visibility"""
        # breakpoint()
        if not isinstance(node, Module):
            return node
        print('+++++++++')
        val = fix_missing_locations(ImportFrom(
            module='sherlock_monkey.sauce_code',
            names=[alias(name='*', asname=None)],
            level=0)
        )
        node.body  = list([val] + node.body)
        return node


class RewriteFunctionDef(RewriteBase):

    def __init__(self, file):
        self.file = file
        super().__init__()

    def visit_FunctionDef(self, node):
        print('----------')
        self._visit(node)
        val = fix_missing_locations(Expr(
                value=Call(
                    func=Name(id="functionCal led", ctx=Load()),
                    args=[],
                    keywords=[keyword(arg='name',value=Constant(value=node.name, ctx=Load(), kind=None)),
                            keyword(arg='line',value=Constant(value=Line().parse(node, self.file), ctx=Load(), kind=None))
                    ],
                )
            ))
        node.body  = list([val] + node.body)
        return node