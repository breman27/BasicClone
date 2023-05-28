##################
# VALUE
##################
import errors


class Value:
    def __init__(self):
        self.set_position()
        self.set_context()

    def set_position(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos

        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subtracted_by(self, other):
        return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)

    def power(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ee(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def is_true(self):
        return False

    def execute(self, args):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception("No copy method defined!")

    def illegal_operation(self, other=None):
        if not other: other = self
        return errors.RTError(self.start_pos, other.end_pos,
                              'Illegal operation', self.context)
