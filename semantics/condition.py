from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

from semantics.value import process_value
from range import process_range, Range

from enum import Enum, auto

class Condition:

    class Type(Enum):
        RANGE = auto()
        SELECTION = auto()

    class Endianness(Enum):
        LITTLE = auto()
        BIG = auto()

    def __init__(self, cond_type: Type, range: Range, data: list[int], endianness: Endianness):
        self.cond_type = cond_type
        self.range = range
        self.data = data
        self.endianness = endianness
        self.negated = False

def process_number_list(node: CFGNode) -> list[int]:
    pass

def process_condition_body(node: CFGNode) -> tuple[list[int], Condition.Type]:

    if node.type != SR.Types.CONDITION_BODY:
        raise ValueError("Node is not a condition body.")

    data: list[int] = []
    cond_type: Condition.Type

    if node.children[0].type == SR.Tokens.LESS_THAN:
        cond_type = Condition.Type.RANGE

        data.append(process_value(node.children[1]))
        data.append(process_value(node.children[3]))

    elif node.children[0].type == SR.Nodes.NUMBER_LIST:


    return data

def process_endianness(node: CFGNode) -> Condition.Endianness:

    if node.type != SR.Types.ENDIANNESS:
        raise ValueError("Node is not an endianness node.")

    match node.children[0].type:
        case SR.Tokens.LITTLE:
            return Condition.Endianness.LITTLE
        case SR.Tokens.BIG:
            return Condition.Endianness.BIG

def process_condition(node: CFGNode) -> Condition:

    children_types: list = [child.type for child in node.children]

    match children_types:

        case [SR.Nodes.RANGE, SR.Nodes.CONDITION_BODY, SR.Nodes.ENDIANNESS]:
            range = process_range(node.children[0])
            body_data, type = process_condition_body(node.children[1])
            endianness_node = process_endianness(node.children[2])

            return Condition(
                cond_type=type,
                range=range,
                data=body_data,
                endianness=endianness_node
            )

        case [SR.Tokens.NEGATION, SR.Nodes.CONDITION]:
            inner_condition = process_condition(node.children[1])
            inner_condition.negated = True
            return inner_condition
        
        case [SR.Types.CONDITION]:
            return node.children[0].children
        
        case _:
            raise ValueError("Invalid condition node structure.")