##################
# INTERPRETER
##################
import basic_token
from basic_number import Number
from basic_string import String
from basic_list import List
from errors import RTError
from function import Function
from runtime_result import RTResult


class Interpreter:

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.token.value)
                                  .set_context(context)
                                  .set_position(node.token.start_pos, node.token.end_pos))

    def visit_StringNode(self, node, context):
        return RTResult().success(String(node.token.value)
                                  .set_context(context)
                                  .set_position(node.token.start_pos, node.token.end_pos))

    def visit_BinaryOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))

        if res.error:
            return res

        right = res.register(self.visit(node.right_node, context))

        if res.error:
            return res

        if node.op.type == basic_token.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op.type == basic_token.TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.op.type == basic_token.TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.op.type == basic_token.TT_DIV:
            result, error = left.divided_by(right)
        elif node.op.type == basic_token.TT_POWER:
            result, error = left.power(right)
        elif node.op.type == basic_token.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op.type == basic_token.TT_EE:
            result, error = left.get_comparison_ee(right)
        elif node.op.type == basic_token.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op.type == basic_token.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op.type == basic_token.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op.type == basic_token.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op.matches(basic_token.TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op.matches(basic_token.TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_position(node.start_pos, node.end_pos))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))

        if res.error:
            return res

        if node.op.type == basic_token.TT_MINUS:
            number, error = number.multiplied_by(Number(-1))
        elif node.op.matches(basic_token.TT_KEYWORD, 'NOT'):
            number, errors = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_position(node.start_pos, node.end_pos))

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(node.start_pos, node.end_pos,
                                       f"'{var_name}' is not defined", context))

        value = value.copy().set_position(node.start_pos, node.end_pos)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res
        end_node = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)

        i = start_value.value
        if step_value.value >= 0:
            condition = lambda: i < end_node.value
        else:
            condition = lambda: i > end_node.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(List(elements).set_context(context).set_position(node.start_pos, node.end_pos))

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res

            if not condition.is_true():
                break
            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error:
                return res

        return res.success(List(elements).set_context(context).set_position(node.start_pos, node.end_pos))

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]

        func_value = Function(func_name, body_node, arg_names).set_context(context)\
            .set_position(node.start_pos, node.end_pos)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error:
            return res
        value_to_call = value_to_call.copy().set_position(node.start_pos, node.end_pos)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res
        return res.success(return_value)

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []
        print(node)

        for element in node.element_nodes:
            elements.append(res.register(self.visit(element, context)))
            if res.error:
                return res

        return res.success(List(elements).set_context(context).set_position(node.start_pos, node.end_pos))
