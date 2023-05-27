##################
# PARSER
##################
import basic_token
import nodes
from errors import InvalidSyntaxError
from parse_result import ParseResult


class Parser:
    def __init__(self, tokens):
        self.current_token = None
        self.tokens = tokens
        self.idx = -1
        self.advance()

    def parse(self):
        res = self.expression()
        if not res.error and self.current_token.type != basic_token.TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos,
                                                  "Expected '+', '-', '*', '^', or '/'"))
        return res

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_token = self.tokens[self.idx]

        return self.current_token

    def atom(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (basic_token.TT_INT, basic_token.TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(nodes.NumberNode(tok))

        elif tok.type in basic_token.TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(nodes.VarAccessNode(tok))

        elif tok.type == basic_token.TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            if self.current_token.type == basic_token.TT_RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos,
                                                      "Expected ')'"))

        elif tok.matches(basic_token.TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(basic_token.TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(basic_token.TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        return res.failure(InvalidSyntaxError(tok.start_pos, tok.end_pos, "Expected Int, Float, identifier, "
                                                                          "'+', '-', or '('"))

    def power(self):
        return self.bin_operation(self.atom, (basic_token.TT_POWER, ), self.factor)

    def for_expr(self):
        res = ParseResult()

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'FOR' Keyword"))

        res.register_advance()
        self.advance()

        if self.current_token.type != basic_token.TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected Identifier"))

        var_name = self.current_token
        res.register_advance()
        self.advance()

        if self.current_token.type != basic_token.TT_EQ:
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected '='"))

        res.register_advance()
        self.advance()

        start_value = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'TO'"))

        res.register_advance()
        self.advance()

        end_value = res.register(self.expression())
        if res.error:
            return res

        if self.current_token.matches(basic_token.TT_KEYWORD, 'STEP'):
            res.register_advance()
            self.advance()

            step_value = res.register(self.expression())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'THEN' Keyword"))

        res.register_advance()
        self.advance()

        body = res.register(self.expression())

        if res.error:
            return res
        return res.success(nodes.ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()
        if not self.current_token.matches(basic_token.TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'WHILE' Keyword"))
        res.register_advance()
        self.advance()

        condition = res.register(self.expression())

        if res.error:
            return res

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'THEN' Keyword"))

        res.register_advance()
        self.advance()

        body = res.register(self.expression())

        if res.error:
            return res

        return res.success(nodes.WhileNode(condition, body))

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'IF' Keyword"))

        res.register_advance()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if not self.current_token.matches(basic_token.TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos, "Expected 'THEN' Keyword"))

        res.register_advance()
        self.advance()

        expr = res.register(self.expression())
        if res.error:
            return res

        cases.append((condition, expr))

        while self.current_token.matches(basic_token.TT_KEYWORD, 'ELIF'):
            res.register_advance()
            self.advance()

            condition = res.register(self.expression())
            if res.error:
                return res

            if not self.current_token.matches(basic_token.TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                      self.current_token.end_pos, "Expected 'THEN' Keyword"))

            expr = res.register(self.expression())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_token.matches(basic_token.TT_KEYWORD, 'ELSE'):
            res.register_advance()
            self.advance()

            else_case = res.register(self.expression())
            if res.error:
                return res

        return res.success(nodes.IfNode(cases, else_case))

    def factor(self):
        res = ParseResult()
        tok = self.current_token

        if tok.type in (basic_token.TT_PLUS, basic_token.TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(nodes.UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_operation(self.factor, (basic_token.TT_MUL, basic_token.TT_DIV))

    def comp_expr(self):
        res = ParseResult()
        if self.current_token.matches(basic_token.TT_KEYWORD, 'NOT'):
            op_tok = self.current_token
            res.register_advance()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(nodes.UnaryOpNode(op_tok, node))

        node = res.register(self.bin_operation(self.arith_expr, (basic_token.TT_EE, basic_token.TT_NE,
                                                                   basic_token.TT_LT, basic_token.TT_GT,
                                                                   basic_token.TT_GTE, basic_token.TT_LTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                               self.current_token.end_pos, "Expected Int, Float, identifier, '+', '-', 'NOT', or '('"))
        return res.success(node)

    def arith_expr(self):
        return self.bin_operation(self.term, (basic_token.TT_PLUS, basic_token.TT_MINUS))

    def expression(self):
        res = ParseResult()

        if self.current_token.matches(basic_token.TT_KEYWORD, 'VAR'):
            res.register_advance()
            self.advance()
            if self.current_token.type != basic_token.TT_IDENTIFIER:
                res.failure(InvalidSyntaxError(self.current_token.start_pos,
                            self.current_token.end_pos, 'Expected Identifier'))

            var_name = self.current_token
            res.register_advance()
            self.advance()

            if self.current_token.type != basic_token.TT_EQ:
                res.failure(InvalidSyntaxError(self.current_token.start_pos,
                            self.current_token.end_pos, "Expected '='"))

            res.register_advance()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            return res.success(nodes.VarAssignNode(var_name, expr))

        node = res.register(self.bin_operation(self.comp_expr,
                                               ((basic_token.TT_KEYWORD, "AND"), (basic_token.TT_KEYWORD, "OR"))))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.start_pos,
                                                  self.current_token.end_pos,
                                                  "Expected Int, Float, identifier, '+', '-', 'VAR', or '('"))

        return res.success(node)

    def bin_operation(self, func_a, ops, func_b=None):
        res = ParseResult()
        left = res.register(func_a())
        if func_b is None:
            func_b = func_a

        if res.error:
            return res

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op = self.current_token
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = nodes.BinaryOpNode(left, op, right)

        return res.success(left)
