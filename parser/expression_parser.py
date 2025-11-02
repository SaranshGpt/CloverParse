from primitives.expression import Expression
from primitives.condition import Condition
from primitives.range import Range
from primitives.value import Value

from parser.tokenise import Token
from parser.range_parser import get_range
from parser.value_parser import get_value, _get_precedence
from parser.condition_parser import get_condition

def get_expression(tokens: list[Token], symbol_table: dict[str, any]) -> tuple[Expression | None, int]:

    post_fix_expression: list[Token | Condition | Expression] = []

    infix_stack: list[Token | Condition | Expression] = []

    end_index = 0

    for token in tokens:

        end_index += 1

        match token.type:
            case Token.Type.IDENTIFIER:
                if token.value in symbol_table:
                    
                    symbol_val: any = symbol_table[token.value]
                    match symbol_val:
                        case Expression():
                            post_fix_expression.append(symbol_val)
                        case Condition():
                            post_fix_expression.append(symbol_val)
                        case _:
                            break
                else:
                    raise ValueError(f"Identifier {token.value} not found in symbol table.")
                
            case Token.Type.AND | Token.Type.OR | Token.Type.XOR | Token.Type.NEGATE:
                precedence = _get_precedence(token)
                if precedence is None:
                    raise ValueError(f"Unknown operator token: {token.type}")
                
                while len(infix_stack) > 0:
                    top = infix_stack[-1]
                    match top:
                        case Token() if _get_precedence(top) is not None and _get_precedence(top) >= precedence:
                            post_fix_expression.append(infix_stack.pop())
                        case _:
                            break

                infix_stack.append(token)
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
                condition, next_index = get_condition(tokens[end_index - 1:], symbol_table)

                if condition is None:
                    return None, 0
                post_fix_expression.append(condition)
                end_index += next_index - 1

    while len(infix_stack) > 0:
        post_fix_expression.append(infix_stack.pop())

    expression_stack: list[Expression | Condition] = []

    for val in post_fix_expression:

        match val:
            case Condition() | Expression():
                expression_stack.append(val)
            case Token():
                match val.type:
                    case Token.Type.AND | Token.Type.OR | Token.Type.XOR:
                        right = expression_stack.pop()
                        left = expression_stack.pop()

                        type = None

                        match val.type:
                            case Token.Type.AND:
                                type = Expression.Type.AND
                            case Token.Type.OR:
                                type = Expression.Type.OR
                            case Token.Type.XOR:
                                type = Expression.Type.XOR
                            case _:
                                raise ValueError(f"Invalid token in postfix expression: {val.type}")

                        if left.__class__ == Condition:
                            left_expr = Expression(left)
                        
                        if right.__class__ == Condition:
                            left.append_condition(type, right)
                        else:
                            left.append_expression(type, right)

                        expression_stack.append(left)
                    case Token.Type.NEGATE:
                        operand = expression_stack.pop()
                        match operand:
                            case Expression():
                                operand.negate()
                                expression_stack.append(operand)
                            case Condition():
                                new_expr = Expression(operand)
                                new_expr.negate()
                                expression_stack.append(new_expr)
                            case _:
                                raise ValueError(f"Invalid token in postfix expression: {val.type}")
                    case _:
                        raise ValueError(f"Invalid token in postfix expression: {val.type}")
                    
    ret = expression_stack[0]

    if ret.__class__ == Condition:
        ret = Expression(ret)

    return ret, end_index
    