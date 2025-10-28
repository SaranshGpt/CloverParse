from enum import Enum, auto

class Value:

    class Endianness(Enum):
        LITTLE = auto()
        BIG = auto()

    def __init__(self, val: int):
        self.val = val
        self.negated = False

    def __add__(self, other):
        return Value(self.val + other.val)
    
    def __sub__(self, other):
        return Value(self.val - other.val)
    
    def __multiply__(self, other):
        return Value(self.val * other.val)
    
    def __floor_divide__(self, other):
        return Value(self.val // other.val)
    
    def __mod__(self, other):
        return Value(self.val % other.val)
    
    def __or__(self, other):
        return Value(self.val | other.val)
    
    def __and__(self, other):
        return Value(self.val & other.val)
    
    def __xor__(self, other):
        return Value(self.val ^ other.val)
    
    def get_bytes(self, length: int, endianness: Endianness, start_offset =  0, end_offset = 0) -> bytes:
        
        if end_offset > 0:
            length += 1

        val = self.val

        ret = bytes()

        tot_len = length * 8 - start_offset - end_offset

        def get_int_bitsection(value: int, start: int, length: int) -> int:
            mask = (1 << length) - 1
            return (value >> start) & mask

        if endianness == Value.Endianness.LITTLE:

            lsval = get_int_bitsection(val, 0, 8 - start_offset)
            msval = get_int_bitsection(val, tot_len - end_offset, end_offset)

            midval = get_int_bitsection(val, 8 - start_offset, tot_len - (8 - start_offset) - end_offset)

            ret = lsval.to_bytes(1, byteorder='little') + midval.to_bytes(length - 2, byteorder='little') + msval.to_bytes(1, byteorder='little')
            
        else:
            
            lsval = get_int_bitsection(val, 0, end_offset)
            msval = get_int_bitsection(val, tot_len - (8-start_offset), (8-start_offset))

            midval = get_int_bitsection(val, end_offset, tot_len - (8 - start_offset) - end_offset)

            ret = msval.to_bytes(1, byteorder='big') + midval.to_bytes(length - 2, byteorder='big') + lsval.to_bytes(1, byteorder='big')

        return ret