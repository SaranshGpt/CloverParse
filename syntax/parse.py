from syntax.cfg_node import CFGNode, CFGRuleSet
from syntax.cfg_grammar import StandardRuleset as SR

from semantics.assignment import process_assignment
from semantics.expression_node import Expression, process_expression
from semantics.condition_node import process_condition

def substitute_symbols(tokens: list[CFGNode], symbol_table: dict[str: CFGNode]) -> None:
    for token in tokens:
        if token.type == SR.Types.UNKNOWN:
            if token.children in symbol_table:
                symbol_node = symbol_table[token.children]
                token.type = symbol_node.type
                token.children = symbol_node.children
            else:
                token.type = SR.Types.NEW 

def parse_line(tokens: list[CFGNode], symbol_table: dict[str: CFGNode]) -> CFGNode:
    
    substitute_symbols(tokens, symbol_table)

    parse_stack: list[CFGNode] = []

    ruleset = SR()

    for token in tokens:

        parse_stack.append(token)

        reduced = True

        while reduced:
            reduced = ruleset.reduce(parse_stack)

    if len(parse_stack) != 1:
        raise ValueError("Could not fully parse line into a single CFGNode.")
    
    return parse_stack[0]


def parse_program(program: list[list[CFGNode]], pattern: list[CFGNode]) -> Expression:
    if (len(pattern) == 0):
        raise ValueError("No pattern provided for parsing.")
    
    symbol_table: dict[str: CFGNode] = {}

    for line_tokens in program:
        node = parse_line(line_tokens, symbol_table)
        process_assignment(node, symbol_table)

    pattern_node = parse_line(pattern, symbol_table)

    match pattern_node.type:
        case SR.Nodes.CONDITION:
            condition = process_condition(pattern_node)
            return Expression(condition)
        case SR.Nodes.EXPRESSION:
            return process_expression(pattern_node)
        case _:
            raise ValueError("Pattern did not parse to a condition or expression.")