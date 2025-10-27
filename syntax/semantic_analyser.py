from cfg_grammar import StandardRuleset as SR
from cfg_node import CFGNode

def process_node(node: CFGNode, symbol_table: dict[str: CFGNode]) -> None:
    match node.type:
        case SR.Nodes.ASSIGNMENT:
            pass
        case SR.Nodes.NUMBER