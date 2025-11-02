from primitives.value import Value

from enum import Enum, auto

from random import randint, choice

class ValueTest:

    def __init__(self, depth: int, val_size: int):

        self.depth = depth

        self.val_size = val_size

        self.operations = [
            'ADD',
            'SUB',
            'MUL',
            'FLOOR_DIV',
            'MOD',
            'OR',
            'AND',
            'XOR'
        ]

        curr_vals = [randint(0, (2**val_size-1))]

        for i in range(depth):
            ind = randint(0, len(curr_vals) - 1)

