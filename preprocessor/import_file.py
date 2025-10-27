import os

from tokenise import Token, tokenise_line
from parser.cfg_grammar import StandardRuleset as SR

def import_file(file_path: str) -> {list[list[Token]] , list[Token]}:

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        content = file.read()

    program: list[list[Token]] = []
    pattern: list[Token] = []

    for line in content.splitlines():
        if line.isspace() or not line:
            continue

        line.strip()

        if line.startswith('#import '):
            import_path_start = line.find('"');
            import_path_end = line.rfind('"');
    
            if import_path_start == -1 or import_path_end == -1 or import_path_end <= import_path_start:
                raise ValueError(f"Invalid import statement: {line}")
            
            import_path = line[import_path_start + 1: import_path_end]

            alias_start = line.rfind(' ');    

            alias = line[alias_start + 1:]

            imported_tokens, _ = import_file(import_path)
                    
            for token_line in imported_tokens:
                for token in token_line:
                    if token.type == SR.Types.UNKNOWN:
                        token.children = alias + "." + token.children

            program.extend(imported_tokens)

        elif line.startswith('#PatternName '):

            name_start = line.find('(')
            name_end = line.find(')')

            pattern_exp = line[name_start + 1: name_end].strip()

            pattern = tokenise_line(pattern_exp)

        elif not line.startswith('#'):
            tokens = tokenise_line(line, {})

            if len(tokens) > 0:
                program.append(tokens)

    return program, pattern