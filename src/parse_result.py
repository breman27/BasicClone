##################
# PARSE RESULT
##################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advanced_count = 0

    def register_advance(self):
        self.advanced_count += 1

    def register(self, res):
        self.advanced_count += res.advanced_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advanced_count == 0:
            self.error = error
        return self
