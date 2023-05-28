##################
# SYMBOL TABLE
##################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, var_name):
        value = self.symbols.get(var_name, None)
        if value is None and self.parent:
            return self.parent.get(var_name)
        return value

    def set(self, var_name, value):
        self.symbols[var_name] = value

    def remove(self, var_name):
        del self.symbols[var_name]
