class CodeWriter:
    CONST = 'constant'
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

    pointer = ["THIS", "THAT"]

    boolean_commands = {
        "eq": "JEQ",
        "gt": "JGT",
        "lt": "JLT",
    }

    arithmetic_operator = {
        "+": "add",
        "-": "sub",
        "*": "call Math.multiply 2",
        "/": "call Math.divide 2",
        "neg": "neg",
        "~": "not",
        ">": "gt",
        "<": "lt",
        "=": "eq",
        "&": "and",
        "|": "or"
    }

    negation_commands = {
        "neg": "-",
        "not": "!"
    }

    label_count = 0

    def __init__(self, output_file):
        self.output = open(output_file, "w")

    def writePush(self, segment, index):
        output = f"push {segment} {index}"
        self.writeOutput(output)

    def writePop(self, segment, index):
        output = f"pop {segment} {index}"
        self.writeOutput(output)

    def writeArithmetic(self, command):
        self.writeOutput(self.arithmetic_operator[command])

    def writeFunction(self, name, nLocals):
        output = f"function {name} {nLocals}"
        self.writeOutput(output)

    def writeLabel(self, label):
        self.writeOutput("label " + label)

    def writeGoto(self, label):
        self.writeOutput("goto " + label)

    def writeIf(self, label):
        self.writeOutput("if-goto " + label)

    def writeCall(self, name, nArgs):
        output = f"call {name} {nArgs}"
        self.writeOutput(output)

    def writeReturn(self, return_type = None, is_constructor=False):
        if return_type == "void":
            self.writePush(self.CONST, "0")
        elif is_constructor:
            self.writePush(self.POINTER, "0")
        self.writeOutput("return")

    def close(self):
        self.output.close()

    def writeOutput(self, s):
        self.output.write(s + "\n")
