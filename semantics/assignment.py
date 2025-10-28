from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

from semantics.value_node import process_value
from semantics.range_node import process_range
from semantics.condition_node import process_condition
from semantics.expression_node import process_expression

def process_assignment(node: CFGNode, symbol_table: dict[str: CFGNode]) -> None:
    
    if node.type != SR.Types.ASSIGNMENT:
        raise ValueError("Node is not an assignment.")

    leftNode = node.children[0]
    rightNode = node.children[2]

    parsed_value = None

    match rightNode.type:
        case SR.Types.VALUE:
            parsed_value = process_value(rightNode)
        case SR.Types.RANGE:
            parsed_value = process_range(rightNode)
        case SR.Types.CONDITION:
            parsed_value = process_condition(rightNode)
        case SR.Types.EXPRESSION:
            parsed_value = process_expression(rightNode)

    symbol_table[leftNode.children] = parsed_value