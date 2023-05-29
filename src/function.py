##################
# FUNCTION
##################
from context import Context
from errors import RTError
from runtime_result import RTResult
from symbol_table import SymbolTable
from value import Value
class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        from interpreter import Interpreter
        res = RTResult()
        interpreter = Interpreter()

        new_context = Context(self.name, self.context, self.start_pos)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) != len(self.arg_names):
            return RTError(self.start_pos, self.end_pos,
                           f"{len(args)} arguments passed in to {self.name}. Expected {len(self.arg_names)}",
                           self.context)

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]

            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error:
            return res

        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_position(self.start_pos, self.end_pos)
        return copy

    def __repr__(self):
        return f"function {self.name}"
