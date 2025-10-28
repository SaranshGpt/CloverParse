from enum import Enum, auto

from primitives.condition import Condition
from primitives.value import Value
from primitives.range import Range

class Expression:

    class Operation(Enum):
        OR = auto()
        XOR = auto()
        AND = auto()

        PUSH = auto()

    def __init__(self, condition: Condition):
        self.expression = [condition]

    def append_expression(self, operation: Operation, other) -> None:
        self.expression.extend(other.expression)
        self.expression.append(operation)

    def serialize(self) -> bytes:

        conditions = []
        operations = []

        for item in self.expression:
            match item:
                case Condition():
                    conditions.append(item)
                    operations.append(Expression.Operation.PUSH)
                    
                case Expression.Operation():
                    operations.append(item)

        num_conditions = len(conditions)

        ret = num_conditions.to_bytes(2)

        for cond in conditions:
            ret += cond.serialize()
        
        for op in operations:
            match op:
                case Expression.Operation.OR:
                    ret += (1).to_bytes(1)
                case Expression.Operation.XOR:
                    ret += (2).to_bytes(1)
                case Expression.Operation.AND:
                    ret += (3).to_bytes(1)
                case Expression.Operation.PUSH:
                    ret += (0).to_bytes(1)
                case _:
                    raise ValueError("Invalid operation in expression.")
                
        return ret