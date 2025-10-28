class Range:
    def __init__(self, start: int, s_offset: int, end: int, e_offset: int):
        self.start = start
        self.s_offset = s_offset
        self.end = end
        self.e_offset = e_offset

    def append(self, other):

        self.start += other.start
        self.s_offset += other.s_offset
        self.end += other.end
        self.e_offset += other.e_offset

        if self.s_offset >= 8:
            self.start += self.s_offset // 8
            self.s_offset = self.s_offset % 8

        if self.e_offset >= 8:
            self.end += self.e_offset // 8
            self.e_offset = self.e_offset % 8