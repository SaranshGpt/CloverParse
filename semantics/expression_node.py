from syntax.cfg_grammar import StandardRuleset as SR
from syntax.cfg_node import CFGNode

from semantics.condition_node import Condition, process_condition

from enum import Enum, auto

from primitives.expression import Expression

def process_condval(node: CFGNode) -> Expression:

    match node.children[0].type:
        case SR.Types.CONDITION:
            condition = process_condition(node.children[0])
            return Expression(condition)
        case SR.Nodes.BRACKET_START:
            return process_expression(node.children[1])
        case SR.Types.CONDITION:
            return Expression(process_condition(node.children[0]))
        case SR.Types.EXPRESSION:
            return process_expression(node.children[0])
        
    raise ValueError("Invalid condition value node.")

def process_and_expr(node: CFGNode) -> Expression:
    
    child_types  = [child.type for child in node.children]

    match child_types:

        case [SR.Nodes.AND_EXPR, SR.Tokens.AND, SR.Nodes.COND_VAL]:
            left_expr = process_and_expr(node.children[0])
            right_expr = process_condition(node.children[2])
            left_expr.append_expression(Expression.Operation.AND, Expression(right_expr))
            return left_expr

        case [SR.Nodes.COND_VAL]:
            condition = process_condition(node.children[0])
            return Expression(condition)
        
    raise ValueError("Invalid and expression node.")

def process_xor_expr(node: CFGNode) -> Expression:
    
    child_types  = [child.type for child in node.children]

    match child_types:

        case [SR.Nodes.XOR_EXPR, SR.Tokens.XOR, SR.Nodes.AND_EXPR]:
            left_expr = process_xor_expr(node.children[0])
            right_expr = process_and_expr(node.children[2])
            left_expr.append_expression(Expression.Operation.XOR, right_expr)
            return left_expr

        case [SR.Nodes.AND_EXPR]:
            return process_and_expr(node.children[0])
        

    raise ValueError("Invalid xor expression node.")

def process_expression(node: CFGNode) -> Expression:
    
    child_types  = [child.type for child in node.children]

    match child_types:

        case [SR.Nodes.EXPRESSION, SR.Tokens.OR, SR.Nodes.XOR_EXPR]:
            left_expr = process_expression(node.children[0])
            right_expr = process_xor_expr(node.children[2])
            left_expr.append_expression(Expression.Operation.OR, right_expr)
            return left_expr
        
        case [SR.Nodes.XOR_EXPR]:
            return process_xor_expr(node.children[0])
        
    raise ValueError("Invalid expression node.")