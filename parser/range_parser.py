from parser.tokenise import Token
from primitives.range import Range
from primitives.value import Value

from parser.value_parser import get_value

def _get_range_interval(tokens: list[Token], symbol_table: dict[str: any]) -> tuple[int , int, int]:
    
    value, next_ind = get_value(tokens, symbol_table)

    offset = Value(0)

    if value is None:
        raise ValueError("Invalid range interval value.")
    
    if tokens[next_ind].type == Token.Type.COLON:
        offset, off_ind = get_value(tokens[next_ind + 1:], symbol_table)

        if offset is None:
            raise ValueError("Invalid range interval offset value.")
        
        next_ind += off_ind + 1

    return value.val, offset.val, next_ind

def get_range(tokens: list[Token], symbol_table: dict[str: any]) -> tuple[Range | None, int]:
    
    range: Range
    final_ind = 0

    if len(tokens) == 0:
        return None, 0

    match tokens[0].type:

        case Token.Type.SQUARE_OPEN:
            start_ind, s_offset, next_ind = _get_range_interval(tokens[1:], symbol_table)

            if( tokens[next_ind + 1].type != Token.Type.COMMA):
                return None, 0
            
            final_ind = next_ind + 1

            end_ind, e_offset, next_ind = _get_range_interval(tokens[next_ind + 2:], symbol_table)

            final_ind += next_ind + 1

            range = Range(start_ind, end_ind, s_offset, e_offset)
            
            if (final_ind < len(tokens) and tokens[final_ind].type == Token.Type.SQUARE_CLOSE):
                final_ind += 1
            else:
                return None, 0

        case Token.Type.IDENTIFIER:
            range = symbol_table[tokens[0].value]
            final_ind = 1
        case _:
            return None, 0
        
    next_range, next_ind = get_range(tokens[final_ind + 1:], symbol_table)

    if next_range is not None:
        range.append(next_range)

    return range, final_ind + next_ind
        