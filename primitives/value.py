from enum import Enum, auto

class Value:

    class Endianness(Enum):
        LITTLE = auto()
        BIG = auto()

    def __init__(self, val):
        
        if type(val) == Value:
            self.val = val.val
        else:
            self.val = val

    def __add__(self, other):
        return Value(self.val + other.val)
    
    def __sub__(self, other):
        return Value(self.val - other.val)
    
    def __mul__(self, other):
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

            msbytes = msval.to_bytes(1, byteorder='big') if end_offset > 0 else b''
            lsbytes = lsval.to_bytes(1, byteorder='big') if start_offset < 8 else b''

            ret = lsbytes + midval.to_bytes(length - 2, byteorder='little') + msbytes
            
        else:
            
            lsval = get_int_bitsection(val, 0, end_offset)
            msval = get_int_bitsection(val, tot_len - (8-start_offset), (8-start_offset))

            midval = get_int_bitsection(val, end_offset, tot_len - (8 - start_offset) - end_offset)

            lsbytes = lsval.to_bytes(1, byteorder='big') if end_offset > 0 else b''
            msbytes = msval.to_bytes(1, byteorder='big') if start_offset < 8 else b''

            ret = msbytes + midval.to_bytes(length - 2, byteorder='big') + lsbytes

        return ret