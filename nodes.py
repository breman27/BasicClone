##################
# NODES
##################

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.start_pos = self.token.start_pos
        self.end_pos = self.token.end_pos

    def __repr__(self):
        return f'{self.token}'

class BinaryOpNode:
    def __init__(self, left_node, op, right_node):
        self.left_node = left_node
        self.op = op
        self.right_node = right_node

        self.start_pos = self.left_node.start_pos
        self.end_pos = self.right_node.end_pos

    def __repr__(self):
        return f'({self.left_node}, {self.op}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

        self.start_pos = self.op.start_pos
        self.end_pos = self.node.end_pos

    def __repr__(self):
        return f'({self.op}{self.node})'

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.start_pos = self.var_name_tok.start_pos
        self.end_pos = self.var_name_tok.end_pos

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.start_pos = self.var_name_tok.start_pos
        self.end_pos = self.value_node.end_pos

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.start_pos = self.cases[0][0].start_pos
        self.end_pos = (self.else_case or self.cases[len(self.cases) - 1][0]).end_pos

class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.start_pos = self.var_name_tok.start_pos
        self.end_pos = self.body_node.end_pos

class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.start_pos = self.condition_node.start_pos
        self.end_pos = self.body_node.end_pos