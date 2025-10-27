from cfg_node import CFGNode, CFGRuleSet
from cfg_grammar import StandardRuleset as SR

def substitute_symbols(tokens: list[CFGNode], symbol_table: dict[str: CFGNode]) -> None:
    for token in tokens:
        if token.type == SR.Types.UNKNOWN:
            if token.children in symbol_table:
                symbol_node = symbol_table[token.children]
                token.type = symbol_node.type
                token.children = symbol_node.children
            else:
                token.type = SR.Types.NEW 

def parse_line(tokens: list[CFGNode], ruleset: CFGRuleSet, symbol_table: dict[str: CFGNode]) -> CFGNode:
    
    substitute_symbols(tokens, symbol_table)

    parse_stack: list[CFGNode] = []

    for token in tokens:

        parse_stack.append(token)

        reduced = True

        while reduced:
            reduced = ruleset.reduce(parse_stack)

    if len(parse_stack) != 1:
        raise ValueError("Could not fully parse line into a single CFGNode.")
    
    return parse_stack[0]


def parse_program(program: list[list[CFGNode]], pattern: list[CFGNode]) -> CFGNode:
    if (len(pattern) == 0):
        raise ValueError("No pattern provided for parsing.")
    
    symbol_table: dict[str: CFGNode] = {}

    for line_tokens in program:
        node = parse_line(line_tokens, symbol_table)
        process_node(node, symbol_table)