from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

def process_assignment(node: CFGNode, symbol_table: dict[str: CFGNode]) -> None:
    
    if node.type != SR.Types.ASSIGNMENT:
        raise ValueError("Node is not an assignment.")

    leftNode = node.children[0]
    rightNode = node.children[2]

    match rightNode.type:
        case SR.Types.VALUE:
            pass
        case SR.Types.RANGE:
            pass
        case SR.Types.CONDITION:
            pass
        case SR.Types.EXPRESSION:
            pass

    symbol_table[leftNode.children] = rightNode