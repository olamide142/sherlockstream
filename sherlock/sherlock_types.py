from collections import namedtuple

TYPES = {
    'FunctionCall' : namedtuple(
        'FunctionCall',
        ['name', 'line']
    )
}