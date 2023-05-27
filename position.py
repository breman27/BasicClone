##################
# POSITION
##################
class Position:
    def __init__(self, index, line_num, col_num, file_name, file_txt):
        self.idx = index
        self.ln = line_num
        self.col = col_num
        self.fn = file_name
        self.ftxt = file_txt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

