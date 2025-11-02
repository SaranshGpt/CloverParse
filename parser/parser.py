import os

from primitives.expression import Expression
from primitives.condition import Condition
from primitives.value import Value
from primitives.range import Range

from parser.range_parser import get_range
from parser.value_parser import get_value
from parser.condition_parser import get_condition
from parser.expression_parser import get_expression

from parser.tokenise import Token, tokenize

def import_file(file_path) -> list[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    return [line.strip() for line in lines if line.strip()]

def handle_import(file_path, prefix, dict):
    new_dict, _ = parse_file(file_path)

    for key, value in new_dict.items():
        new_key = f"{prefix}.{key}" if prefix else key
        dict[new_key] = value

def parse_file(file_path) -> tuple[dict[str, any], Expression | None]:
    
    lines = import_file(file_path)

    pattern_expression: Expression | None = None

    dict = {}

    for line in lines:

        comment_index = line.find('//')
        if comment_index != -1:
            line = line[:comment_index]

        line = line.strip()

        if len(line) == 0:
            continue

        if line.startswith("#import "):
            
            path_start = line.find('"') + 1
            path_end = line.rfind('"')

            import_path = line[path_start:path_end]

            before_prefix = line.find('as')

            if before_prefix == -1:
                raise ValueError(f"Import statement missing 'as' for prefix in line: {line}")
            
            prefix = line[before_prefix + 2:].strip()

            handle_import(import_path, prefix, dict)
            continue

        if line.startswith("#pattern(") and line.endswith(")"):
            exp_start = line.find('(') + 1
            exp_end = line.rfind(')')

            pattern_expression_str = line[exp_start:exp_end].strip()
            pattern_tokens = tokenize(pattern_expression_str)
            pattern_expression, next_ind = get_expression(pattern_tokens, dict)

            if pattern_expression is None or next_ind != len(pattern_tokens):
                raise ValueError(f"Invalid pattern expression in line: {line}")
            
            continue

        tokens = tokenize(line)

        if not (tokens[0].type == Token.Type.IDENTIFIER and tokens[1].type == Token.Type.EQUALS):
            raise ValueError(f"Invalid syntax in line: {line}")

        rhs = None

        rhs, next_ind = get_condition(tokens[2:], dict)

        if rhs is None or len(tokens) != next_ind + 2:
            rhs, next_ind = get_expression(tokens[2:], dict)

        if rhs is None or len(tokens) != next_ind + 2:
            rhs, next_ind = get_range(tokens[2:], dict)

        if rhs is None or len(tokens) != next_ind + 2:
            rhs, next_ind = get_value(tokens[2:], dict)

        if rhs is None or len(tokens) != next_ind + 2:
            raise ValueError(f"Unable to parse right-hand side of assignment in line: {line}")

        dict[tokens[0].value] = rhs

    return dict, pattern_expression