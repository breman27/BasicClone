##################
# LIST
##################
from numbers import Number
from errors import RTError
from value import Value


class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subtracted_by(self, other):
        if isinstance(other.value, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(other.start_pos, other.end_pos,
                                     "Could not remove element from the list", self.context)
        else:
            return None, Value.illegal_operation(other)

    def multiplied_by(self, other):
        if isinstance(other.value, Number):
            return List(self.elements * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(other)

    def copy(self):
        copy = List(self.elements[:])
        copy.set_position(self.start_pos, self.end_pos)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.elements}"
