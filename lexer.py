##################
# LEXER
##################
import position
import errors
import constants
import basic_token

class Lexer:
    def __init__(self, file_name, text):
        self.fn = file_name
        self.text = text
        self.pos = position.Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_identifier(self):
        res_str = ''
        start_pos = self.pos.copy()

        while self.current_char is not None and self.current_char in (constants.LETTERS_DIGITS + '_'):
            res_str += self.current_char
            self.advance()

        tok_type = basic_token.TT_KEYWORD if res_str in basic_token.KEYWORDS else basic_token.TT_IDENTIFIER

        return basic_token.Token(tok_type, res_str, start_pos, self.pos)

    def make_number(self):
        num_str = ''
        dot_count = 0
        start_pos = self.pos.copy()

        while self.current_char is not None and self.current_char in (constants.DIGITS + '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return basic_token.Token(basic_token.TT_INT, int(num_str), start_pos, self.pos)
        else:
            return basic_token.Token(basic_token.TT_FLOAT, float(num_str), start_pos, self.pos)

    def make_equals(self):
        start_pos = self.pos.copy()
        tok_type = basic_token.TT_EQ
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = basic_token.TT_EE

        return basic_token.Token(tok_type, start_pos=start_pos, end_pos=self.pos)

    def make_less_than(self):
        start_pos = self.pos.copy()
        tok_type = basic_token.TT_LT
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = basic_token.TT_LTE

        return basic_token.Token(tok_type, start_pos=start_pos, end_pos=self.pos)

    def make_greater_than(self):
        start_pos = self.pos.copy()
        tok_type = basic_token.TT_GT
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = basic_token.TT_GTE

        return basic_token.Token(tok_type, start_pos=start_pos, end_pos=self.pos)

    def make_minus_or_arrow(self):
        start_pos = self.pos.copy()
        tok_type = basic_token.TT_MINUS
        self.advance()
        if self.current_char == '>':
            self.advance()
            tok_type = basic_token.TT_ARROW
        return basic_token.Token(tok_type, start_pos=start_pos, end_pos=self.pos)

    def make_not_equals(self):
        start_pos = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return basic_token.Token(basic_token.TT_NE, start_pos=start_pos, end_pos=self.pos), None

        self.advance()
        return None, errors.ExpectedCharError(start_pos, self.pos, "Expected an '=' after '!'")

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in constants.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in constants.LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(basic_token.Token(basic_token.TT_PLUS, start_pos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(basic_token.Token(basic_token.TT_MUL, start_pos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(basic_token.Token(basic_token.TT_DIV, start_pos=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(basic_token.Token(basic_token.TT_LPAREN, start_pos=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(basic_token.Token(basic_token.TT_RPAREN, start_pos=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(basic_token.Token(basic_token.TT_POWER, start_pos=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(basic_token.Token(basic_token.TT_COMMA, start_pos=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], errors.IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(basic_token.Token(basic_token.TT_EOF, start_pos=self.pos))
        return tokens, None
