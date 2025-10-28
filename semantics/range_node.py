from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

from semantics.value_node import process_value

from primitives.range import Range

def process_range(node: CFGNode) -> Range:

    if node.type != SR.Types.RANGE:
        raise ValueError("Node is not a range.")

    children_types: tuple = [child.type for child in node.children]

    match children_types:
        case [  SR.Tokens.SQUARE_START, 
                    SR.Nodes.VALUE, SR.Tokens.COLON, SR.Nodes.VALUE, 
                    SR.Tokens.COMMA, 
                    SR.Nodes.VALUE, SR.Tokens.COLON, SR.Nodes.VALUE, 
                SR.Tokens.SQUARE_END]:
            
            return Range(
                start=process_value(node.children[1]),
                s_offset=process_value(node.children[3]),
                end=process_value(node.children[5]),
                e_offset=process_value(node.children[7])
            )
        
        case [  SR.Tokens.SQUARE_START, 
                    SR.Nodes.VALUE, SR.Tokens.COLON, SR.Nodes.VALUE, 
                    SR.Tokens.COMMA, 
                    SR.Nodes.VALUE,
                SR.Tokens.SQUARE_END]:
            
            return Range(
                start=process_value(node.children[1]),
                s_offset=process_value(node.children[3]),
                end=process_value(node.children[5]),
                e_offset=0
            )
        
        case [  SR.Tokens.SQUARE_START, 
                    SR.Nodes.VALUE,
                    SR.Tokens.COMMA, 
                    SR.Nodes.VALUE, SR.Tokens.COLON, SR.Nodes.VALUE, 
                SR.Tokens.SQUARE_END]:
            
            return Range(
                start=process_value(node.children[1]),
                s_offset=0,
                end=process_value(node.children[3]),
                e_offset=process_value(node.children[5])
            )
        
        case [  SR.Tokens.SQUARE_START, 
                    SR.Nodes.VALUE,
                    SR.Tokens.COMMA, 
                    SR.Nodes.VALUE,
                SR.Tokens.SQUARE_END]:
            
            return Range(
                start=process_value(node.children[1]),
                s_offset=0,
                end=process_value(node.children[3]),
                e_offset=0
            )

        case [ SR.Nodes.RANGE, SR.Nodes.RANGE]:
            range1 = process_range(node.children[0])
            range2 = process_range(node.children[1])

            range1.append(range2)

            return range1
        
        case [ SR.Types.RANGE]:
            return node.children[0].children

        case _:
            raise ValueError("Invalid range node structure.")