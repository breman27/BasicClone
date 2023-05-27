##################
# ERRORS
##################

def string_with_arrows(text, start_pos, end_pos):
    result = ''

    idx_start = max(text.rfind('\n', 0, start_pos.idx), 0)
    idx_end = text.find('\n', idx_start + 1)

    if idx_end < 0:
        idx_end = len(text)

    line_count = end_pos.ln - start_pos.ln + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = start_pos.col if i == 0 else 0
        col_end = end_pos.col if i == line_count - 1 else len(line) - 1

        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0:
            idx_end = len(text)

    return result.replace('\t', '')


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details} \n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'Invalid Syntax', details)

class ExpectedCharError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'Expected Character Error', details)

class RTError(Error):
    def __init__(self, start_pos, end_pos, details, context):
        super().__init__(start_pos, end_pos, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        context = self.context

        while context:
            result = f'File {pos.fn}, line {pos.ln + 1}, in context {context.display_name}\n' + result
            pos = context.parent_entry_pos
            context = context.parent

        return f'Traceback (most recent call last):\n {result}'
