from enum import Enum, auto
import re

from parser.cfg_grammar import StandardRuleset as SR
from parser.cfg_node import CFGNode

class Token(CFGNode):

    def __init__(self, part: str):
        self.children = None
        match part:
            case '=':
                self.type = SR.Tokens.EQUALS
                return
            case '[':
                self.type = SR.Tokens.SQUARE_START
                return
            case ']':
                self.type = SR.Tokens.SQUARE_END
                return
            case '{':
                self.type = SR.Tokens.CURLY_START
                return
            case '}':
                self.type = SR.Tokens.CURLY_END
                return
            case '(':
                self.type = SR.Tokens.BRACKET_START
                return
            case ')':
                self.type = SR.Tokens.BRACKET_END
                return
            case '<':
                self.type = SR.Tokens.LESS_THAN
                return
            case '>':
                self.type = SR.Tokens.GREATER_THAN
                return
            case ',':
                self.type = SR.Tokens.COMMA
                return
            case ':':
                self.type = SR.Tokens.COLON
                return
            case '+':
                self.type = SR.Tokens.PLUS
                return
            case '-':
                self.type = SR.Tokens.MINUS
                return
            case '*':
                self.type = SR.Tokens.MULTIPLY
                return
            case '/':
                self.type = SR.Tokens.DIVIDE
                return
            case '~':
                self.type = SR.Tokens.NEGATION
                return
            case 'L':
                self.type = SR.Tokens.LITTLE_ENDIAN
                return
            case 'B':
                self.type = SR.Tokens.BIG_ENDIAN
                return
    
        if part and part[0].isalpha():
            self.type = SR.Types.UNKNOWN
            self.children = part
            return

        if part.isdigit():
            self.type = SR.Tokens.NUMBER
            self.children = int(part)

        spec = part[:2]
        num = part[2:]

        if not num.isdigit():
            raise ValueError(f'Invalid Token: {part}')

        match spec:
            case '0x':
                self.type = SR.Tokens.NUMBER
                self.children = int(num, 16)
            case '0b':
                self.type = SR.Tokens.NUMBER
                self.children = int(num, 2)
            case '0o':
                self.type = SR.Tokens.NUMBER
                self.children = int(num, 8)

        raise ValueError(f"Invalid Token: {part}")
    


def tokenise_line(line: str) -> list[Token]:
    
    # truncate at comment start //
    idx = line.find('//')
    if idx != -1:
        line = line[:idx].rstrip()

    if not line or line.isspace():
        return []

    line.strip()

    parts = re.split(r'[a-zA-Z0-9]+', line)

    tokens: list = []

    for part in parts:
        if part is None or part.iswhite():
            continue
        
        token = Token(part)

        tokens.append(Token(part))

    return tokens