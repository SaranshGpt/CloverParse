from enum import Enum, auto

import re

class Token:

    class Type(Enum):
        IDENTIFIER = auto()
        
        LITERAL_INT = auto()

        COLON = auto()

        SQUARE_OPEN = auto()
        SQUARE_CLOSE = auto()

        CURLY_OPEN = auto()
        CURLY_CLOSE = auto()

        BRACKET_OPEN = auto()
        BRACKET_CLOSE = auto()

        LESSER_THAN = auto()
        GREATER_THAN = auto()

        COMMA = auto()

        OR = auto()
        AND = auto()
        XOR = auto()

        PLUS = auto()
        MINUS = auto()
        MULTIPLY = auto()
        DIVIDE = auto()
        MODULO = auto()

        NEGATE = auto()
        
        EQUALS = auto()

        LITTLE_ENDIAN = auto()
        BIG_ENDIAN = auto()

    def __init__(self, value: str):

        value = value.strip()

        self.type = None
        self.value = None
        
        match value:
            case ":":
                self.type = Token.Type.COLON
            case "[":
                self.type = Token.Type.SQUARE_OPEN
            case "]":
                self.type = Token.Type.SQUARE_CLOSE
            case "{":
                self.type = Token.Type.CURLY_OPEN
            case "}":
                self.type = Token.Type.CURLY_CLOSE
            case "(":
                self.type = Token.Type.BRACKET_OPEN
            case ")":
                self.type = Token.Type.BRACKET_CLOSE
            case "<":
                self.type = Token.Type.LESSER_THAN
            case ">":
                self.type = Token.Type.GREATER_THAN
            case ",":
                self.type = Token.Type.COMMA
            case "|":
                self.type = Token.Type.OR
            case "&":
                self.type = Token.Type.AND
            case "^":
                self.type = Token.Type.XOR
            case "+":
                self.type = Token.Type.PLUS
            case "-":
                self.type = Token.Type.MINUS
            case "*":
                self.type = Token.Type.MULTIPLY
            case "/":
                self.type = Token.Type.DIVIDE
            case "%":
                self.type = Token.Type.MODULO
            case "~":
                self.type = Token.Type.NEGATE
            case "=":
                self.type = Token.Type.EQUALS
            case "L":
                self.type = Token.Type.LITTLE_ENDIAN
            case "B":
                self.type = Token.Type.BIG_ENDIAN
            
        if self.type is not None:
            return
        
        if value == "":
            raise ValueError("Empty token.")
        
        if value[0].isalpha() or value[0] == "_":
            self.type = Token.Type.IDENTIFIER
            self.value = value
            return

        if value.isdigit():
            self.type = Token.Type.LITERAL_INT
            self.value = int(value)
            return
        
        if value.startswith("0x"):
            self.type = Token.Type.LITERAL_INT
            self.value = int(value, 16)
        elif value.startswith("0b"):
            self.type = Token.Type.LITERAL_INT
            self.value = int(value, 2)
        elif value.startswith("0o"):
            self.type = Token.Type.LITERAL_INT
            self.value = int(value, 8)
        else:
            raise ValueError(f"Unknown token: {value}")
        
def tokenize(input_str: str) -> list[Token]:
    tokens: list[Token] = []

    input_str = input_str.strip()

    parts = re.findall(r"([\w.]+|[^\w.\s])", input_str)

    for part in parts:
        if part.strip() == "":
            continue
        tokens.append(Token(part))

    return tokens