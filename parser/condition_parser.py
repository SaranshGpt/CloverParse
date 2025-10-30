from primitives.condition import Condition
from primitives.value import Value
from primitives.range import Range

from parser.tokenise import Token
from parser.range_parser import get_range
from parser.value_parser import get_value

def get_condition(tokens: list[Token], symbol_table: dict[str, any]) -> tuple[Condition | None, int]:

    try:

        next_ind = 0

        if tokens[0].type == Token.Type.IDENTIFIER:
            ident_name = tokens[next_ind].value

            if ident_name in symbol_table:

                condition: Condition = symbol_table[ident_name]

                match condition:
                    case Condition():
                        return condition, next_ind + 1
                    case Range():
                        pass
                    case _:
                        return None, 0
            else:
                raise ValueError(f"Identifier {ident_name} not found in symbol table.")

        range, range_ind = get_range(tokens, symbol_table)

        next_ind += range_ind

        if range is None:
            return None, 0

        condition_type = None

        if tokens[next_ind].type == Token.Type.LESSER_THAN:
            condition_type = Condition.Type.RANGE
        elif tokens[next_ind].type == Token.Type.CURLY_OPEN:
            condition_type = Condition.Type.SELECTION
        else:
            return None, 0

        next_ind += 1

        values = []

        while True:

            value, val_ind = get_value(tokens[next_ind:], symbol_table)

            if value is None:
                break
            
            values.append(value)

            if condition_type == Condition.Type.RANGE and len(range) == 2:
                break

            if condition_type == Condition.Type.SELECTION and tokens[next_ind + val_ind].type == Token.Type.CURLY_CLOSE:
                next_ind += val_ind
                break

            next_ind += val_ind

            if tokens[next_ind].type == Token.Type.COMMA:
                next_ind += 1
            elif condition_type == Condition.Type.SELECTION and tokens[next_ind].type == Token.Type.CURLY_CLOSE or condition_type == Condition.Type.RANGE and tokens[next_ind].type == Token.Type.GREATER_THAN:
                next_ind += 1
                break
            else:
                return None, 0

        endianness = None

        match tokens[next_ind].type:
            case Token.Type.LITTLE_ENDIAN:
                endianness = Value.Endianness.LITTLE
                next_ind += 1
            case Token.Type.BIG_ENDIAN:
                endianness = Value.Endianness.BIG
                next_ind += 1
            case _:
                raise ValueError("Endianness not specified in condition.")

        condition = Condition(
            type=condition_type,
            range=range,
            values=values,
            endianness=endianness
        )

    except IndexError:
        return None, 0

    return condition, next_ind