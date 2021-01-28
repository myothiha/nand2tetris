class SymbolTable:
    STATIC = 'static'
    FIELD = 'field'
    ARG = 'argument'
    VAR = 'local'

    categories = ['var', 'arg', 'static', 'field', 'class', 'subroutine']

    variables = ['var', 'arg', 'static', 'field']

    maps = {
        "field": "this"
    }

    def __init__(self):
        self.class_table = []
        self.subroutine_table = []
        self.static_index = -1
        self.field_index = -1
        self.arg_index = -1
        self.var_index = -1

    def startSubroutine(self):
        self.arg_index = -1
        self.var_index = -1
        self.subroutine_table = []

    def define(self, name, type, kind):
        if kind in [self.STATIC, self.FIELD]:
            if kind == self.STATIC:
                self.static_index += 1
                new_symbol = {"name": name, "type": type, "kind": kind, "index": self.static_index}
            else:
                self.field_index += 1
                new_symbol = {"name": name, "type": type, "kind": kind, "index": self.field_index}

            self.class_table.append(new_symbol)
        else:
            if kind == self.ARG:
                self.arg_index += 1
                new_symbol = [name, type, kind, self.arg_index]
                new_symbol = {"name": name, "type": type, "kind": kind, "index": self.arg_index}

            else:
                self.var_index += 1
                new_symbol = [name, type, kind, self.var_index]
                new_symbol = {"name": name, "type": type, "kind": kind, "index": self.var_index}

            self.subroutine_table.append(new_symbol)

    def varCount(self, kind):
        if kind in self.variables:
            if kind is self.STATIC:
                return self.static_index + 1
            elif kind is self.FIELD:
                return self.field_index + 1
            elif kind is self.VAR:
                return self.var_index + 1
            elif kind is self.ARG:
                return self.arg_index + 1

    def isObject(self, name):
        symbol = self.getFromClass(name)
        if not symbol:
            symbol = self.getFromSubroutine(name)
        if not symbol:
            return False
        return True

    def kindOf(self, name):
        symbol = self.getFromClass(name)
        if not symbol:
            symbol = self.getFromSubroutine(name)
        if symbol["kind"] == "field":
            return self.maps["field"]
        return symbol["kind"]

    def typeOf(self, name):
        symbol = self.getFromClass(name)
        if not symbol:
            symbol = self.getFromSubroutine(name)

        return symbol["type"]

    def indexOf(self, name):
        symbol = self.getFromClass(name)
        if not symbol:
            symbol = self.getFromSubroutine(name)

        return symbol["index"]

    def getFromClass(self, name):
        symbols = self.class_table
        for symbol in symbols:
            if name == symbol["name"]:
                return symbol

        return None

    def getFromSubroutine(self, name):
        symbols = self.subroutine_table
        for symbol in symbols:
            if name == symbol["name"]:
                return symbol

        return None