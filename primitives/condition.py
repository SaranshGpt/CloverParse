from enum import Enum, auto

from primitives.range import Range
from primitives.value import Value

class Condition:

    class Type(Enum):
        RANGE = auto()
        SELECTION = auto()

    def __init__(self, cond_type: Type, range: Range, data: list[Value], endianness: Value.Endianness):
        self.cond_type = cond_type
        self.range = range
        self.data = data
        self.endianness = endianness
        self.negated = False

    def _get_params(self) -> bytes:

        start_index = self.range.start
        s_offset = self.range.s_offset

        end_index = self.range.end
        e_offset = self.range.e_offset

        endianness = (1 if self.endianness == Value.Endianness.LITTLE else 0)

        negation = (1 if self.negated else 0)

        consolidated_val = (start_index << 24) | (end_index << 8) | (endianness << 7) | (negation << 6) | (s_offset << 3) | e_offset

        return consolidated_val.to_bytes(5, byteorder='big')
    
    def _get_fixed_bytes(self) -> bytes:
        val: Value = self.data[0]

        length = self.range.end - self.range.start
        
        if self.range.e_offset > 0:
            length += 1

        return val.get_bytes(length, self.endianness, self.range.s_offset, self.range.e_offset)

    def _get_range_bytes(self) -> bytes:
        lower_limit = Value(self.data[0])
        upper_limit = Value(self.data[1])

        length = self.range.end - self.range.start

        if self.range.e_offset > 0:
            length += 1

        lower_bytes = lower_limit.get_bytes(length, self.endianness, self.range.s_offset, self.range.e_offset)
        upper_bytes = upper_limit.get_bytes(length, self.endianness, self.range.s_offset, self.range.e_offset)

        return lower_bytes + upper_bytes

    def _get_selection_bytes(self) -> bytes:
        num_vals = len(self.data)

        length = self.range.end - self.range.start

        ret: bytes

        for i in range(num_vals):
            val = Value(self.data[i])
            ret += val.get_bytes(length, self.endianness, self.range.s_offset, self.range.e_offset)

        return length.to_bytes(2) + ret;

    def create_binary(self) -> bytes:

        enum_val: int
        packet_bytes: bytes

        match self.cond_type:
            case Condition.Type.RANGE:
                packet_bytes = self._get_range_bytes()
                enum_val = 1
            case Condition.Type.SELECTION:
                if len(self.data) > 1:
                    packet_bytes = self._get_selection_bytes()
                    enum_val = 2
                else:
                    packet_bytes = self._get_fixed_bytes()
                    enum_val = 0

        return enum_val.to_bytes(1) + self._get_params() + packet_bytes