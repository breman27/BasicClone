##################
# NUMBER
##################
import math

from errors import RTError


class Number:
    def __init__(self, value):
        self.value = value
        self.start_pos = None
        self.end_pos = None
        self.context = None
        self.set_position()
        self.set_context()

    def set_position(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos

        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.start_pos, other.end_pos, 'Division by zero', self.context)
            else:
                return Number(self.value / other.value).set_context(self.context), None

    def power(self, other):
        if isinstance(other, Number):
            return Number(math.pow(self.value, other.value)).set_context(self.context), None

    def get_comparison_ee(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_position(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def set_context(self, context=None):
        self.context = context
        return self

    def __repr__(self):
        return str(self.value)
