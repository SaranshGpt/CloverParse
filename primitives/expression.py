from enum import Enum, auto

from primitives.condition import Condition
from primitives.value import Value
from primitives.range import Range

class Expression:

    class Operation(Enum):
        OR = auto()
        XOR = auto()
        AND = auto()
        NEGATE = auto()

        PUSH = auto()

    def __init__(self, condition: Condition):
        self.conditions = [condition]
        self.operations = [Expression.Operation.PUSH]

    def append_condition(self, operation: Operation, condition: Condition) -> None:
        self.conditions.append(condition)
        self.operations.append(Expression.Operation.PUSH)
        self.operations.append(operation)

    def append_expression(self, operation: Operation, other) -> None:
        self.conditions.extend(other.conditions)
        self.operations.extend(other.operations)
        self.operations.append(operation)

    def negate(self) -> None:
        self.operations.append(Expression.Operation.NEGATE)

    def serialize(self) -> bytes:

        ret = bytes()

        num_conditions = len(self.conditions)

        ret += num_conditions.to_bytes(2, 'big')

        for condition in self.conditions:
            ret += condition.serialize()

        for operation in self.operations:
            match operation:
                case Expression.Operation.OR:
                    ret += bytes([0x01])
                case Expression.Operation.XOR:
                    ret += bytes([0x02])
                case Expression.Operation.AND:
                    ret += bytes([0x03])
                case Expression.Operation.NEGATE:
                    ret += bytes([0x04])
                case Expression.Operation.PUSH:
                    ret += bytes([0x00])
                case _:
                    raise ValueError(f"Unknown operation type: {operation}")
                
        return ret