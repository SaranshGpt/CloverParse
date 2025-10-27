from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

def process_number(node: CFGNode) -> int:
    if node.type != SR.Types.NUMBER:
        raise ValueError("Node is not a number.")

    match node.children[0].type:
        case SR.Tokens.NUMBER:
            return int(node.children[0].children)
        case SR.Tokens.NEGATION:
            return -process_value(node.children[1])
        case SR.Tokens.BRACKET_START:
            return process_value(node.children[1]) 

def process_value(node: CFGNode) -> int:
    
    node_type = node.type

    if node_type == SR.Types.NUMBER:
        return process_number(node)

    children_types: tuple = [child.type for child in node.children]

    len_children = len(node.children) if node.children else 0

    if len_children == 1:
        return process_value(node.children[0])

    match children_types[1]:
        case SR.Tokens.OR:
            return process_value(node.children[0]) | process_value(node.children[2])
        case SR.Tokens.XOR:
            return process_value(node.children[0]) & process_value(node.children[2])
        case SR.Tokens.AND:
            return process_value(node.children[0]) ^ process_value(node.children[2])
        
        case SR.Tokens.PLUS:
            return process_value(node.children[0]) + process_value(node.children[2])
        case SR.Tokens.MINUS:
            return process_value(node.children[0]) - process_value(node.children[2])
        case SR.Tokens.MULTIPLY:
            return process_value(node.children[0]) * process_value(node.children[2])
        case SR.Tokens.DIVIDE:
            return process_value(node.children[0]) // process_value(node.children[2])
        case SR.Tokens.MODULO:
            return process_value(node.children[0]) % process_value(node.children[2])