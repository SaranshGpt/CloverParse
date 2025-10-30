from primitives.value import Value
from parser.tokenise import Token, tokenize

def _get_precedence(token: Token) -> int| None:
    match token.type:
        case Token.Type.OR:
            return 1
        case Token.Type.XOR:
            return 2
        case Token.Type.AND:
            return 3
        case Token.Type.PLUS | Token.Type.MINUS:
            return 4
        case Token.Type.MULTIPLY | Token.Type.DIVIDE | Token.Type.MODULO:
            return 5
        case Token.Type.NEGATE:
            return 6
        case _:
            return None

def get_value(tokens: list[Token], symbol_table: dict[str, any]) -> tuple[Value, int]:

    post_fix_expression: list[Token | Value] = []
    infix_stack: list[Token | Value] = []

    end_index = 0

    for token in tokens:

        match token.type:
            case Token.Type.LITERAL_INT:
                post_fix_expression.append(Value(token.value))
            case Token.Type.IDENTIFIER:
                if token.value in symbol_table:
                    
                    symbol_val: Value = symbol_table[token.value]
                    if(symbol_val.__class__ == Value):
                        post_fix_expression.append(Value(symbol_val))
                    else:
                        break
                else:
                    raise ValueError(f"Identifier {token.value} not found in symbol table.")
                
            case Token.Type.BRACKET_OPEN:
                infix_stack.append(token)
            case Token.Type.BRACKET_CLOSE:
                while len(infix_stack) > 0:
                    top = infix_stack.pop()
                    match top:
                        case Token() if top.type == Token.Type.BRACKET_OPEN:
                            break
                        case _:
                            post_fix_expression.append(top)
            case _:
                precedence = _get_precedence(token)
                
                if precedence is None:
                    break
                
                while len(infix_stack) > 0:
                    top = infix_stack[-1]
                    match top:
                        case Token() if _get_precedence(top) is not None and _get_precedence(top) >= precedence:
                            post_fix_expression.append(infix_stack.pop())
                        case _:
                            break
        
                infix_stack.append(token)

        end_index += 1

    while len(infix_stack) > 0:
        post_fix_expression.append(infix_stack.pop())

    expression_stack: list[Value] = []

    for val in post_fix_expression:

        match val:
            case Token():
                match val.type:
                    case Token.Type.PLUS:
                        right = expression_stack.pop()
                        left = expression_stack.pop()
                        expression_stack.append(left + right)
                    case Token.Type.MINUS:
                        right = expression_stack.pop()
                        left = expression_stack.pop()
                        expression_stack.append(left - right)
                    case Token.Type.MULTIPLY:
                        right = expression_stack.pop()
                        left = expression_stack.pop()
                        expression_stack.append(left * right)
                    case Token.Type.DIVIDE:
                        right = expression_stack.pop()
                        left = expression_stack.pop()
                        expression_stack.append(left // right)
                    case Token.Type.MODULO:
                        right = expression_stack.pop()
                        left = expression_stack.pop()
                        expression_stack.append(left % right)
                    case Token.Type.NEGATE:
                        operand = expression_stack.pop()
                        operand.negated = not operand.negated
                        expression_stack.append(operand)
                    case _:
                        raise ValueError(f"Invalid token in postfix expression: {val.type}")
                    
            case Value():
                expression_stack.append(val)

    if len(expression_stack) != 1:
        return None, 0
    
    return expression_stack[0], end_index
