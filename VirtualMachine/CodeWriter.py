from Parser import Parser
import os

class CodeWriter:
    base_memory_segments = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": 5
    }

    pointer = ["THIS", "THAT"]

    boolean_commands = {
        "eq": "JEQ",
        "gt": "JGT",
        "lt": "JLT",
    }

    arithmetic_logical_commands = {
        "add": "+",
        "sub": "-",
        "and": "&",
        "or": "|",
    }

    negation_commands = {
        "neg": "-",
        "not": "!"
    }

    label_count = 0

    return_address_count = 1

    def __init__(self, sourcefile):

        # Remove "/" from directory
        if sourcefile[-1] == "/":
            sourcefile = list(sourcefile)
            del sourcefile[-1]
            sourcefile = "".join(sourcefile)


        path = sourcefile.split(".")[0].split("/")
        self.filename = path[-1]

        if os.path.isdir(sourcefile):
            output_file = sourcefile + "/" + self.filename + ".asm"

            self.target = open(output_file, "w")
        else:
            output_file = sourcefile.split(".")[0] + ".asm"
            self.target = open(output_file, "w")

    def writeBootstrap(self):
        output = "//Call Init\n"
        # SP=261. It should be 256 why ?
        output += "@261\n"
        output += "D=A\n"
        output += "@SP\n"
        output += "M=D\n"

        # call Sys.init
        output += "@Sys.init\n"
        output += "0;JMP\n"
        self.target.write(output)

    def writeArithmetic(self, command):
        output = "// " + command + "\n"
        if command in self.arithmetic_logical_commands:
            output += self.getArithmeticAndLogicalCommand(command)
        elif command in self.negation_commands:
            output += self.getNegationCommand(command)
        elif command in self.boolean_commands:
            output += self.getBooleanCommand(command)
        self.target.write(output)

    def writePushPop(self, command, command_type, segment, index, current_source_file):
        output = "// " + command + "\n"
        if command_type == Parser.C_PUSH:
            if segment == "constant":
                output += self.writePushConstant(index)
            elif segment == "pointer":
                output += self.writePushPointer(index)
            elif segment == "static":
                # D = static i
                output += "@" + current_source_file + "." + str(index) + "\n"
                output += "D=M\n"

                # sp.push(D)
                output += self.pushStack()
            else:
                output += self.pushOtherSegments(segment, index)
        elif command_type == Parser.C_POP:
            if segment == "pointer":
                output += self.writePopPointer(index)
            elif segment == "static":
                # D = sp.pop()
                output += self.popStack()

                # static i = D
                output += "@" + current_source_file + "." + str(index) + "\n"
                output += "M=D\n"
            else:
                output += self.writePopOtherSegments(segment, index)
        self.target.write(output)

    def writeIfGoto(self, command):
        label = command.split(" ")[1]
        output = "// " + command + "\n"

        # D = stack.pop()
        output += self.popStack()

        # Jump if D > 0 or D < 0. That mean. D is not equal to zero
        output += "@" + label + "\n"
        output += "D;JLT\n"
        output += "@" + label + "\n"
        output += "D;JGT\n"
        self.target.write(output)

    def writeGoto(self, command):
        label = command.split(" ")[1]
        output = "// " + command + "\n"
        output += "@" + label + "\n"
        output += "0;JMP\n"
        self.target.write(output)

    def writeLabel(self, command):
        label = command.split(" ")[1]
        output = "// " + command + "\n"
        output += "(" + label + ")\n"
        self.target.write(output)

    def writeHandleFunction(self, command, function_name, local_vars):
        output = "// " + command + "\n"

        output += "(" + function_name + ")\n"

        # push 0 to local var. repeat n times.
        for _ in range(local_vars):
            output += self.writePushConstant(0)

        self.target.write(output)

    def writeCallFunction(self, command, function_name, args):

        # define return address filename$ret.0
        return_address = self.filename + "$ret." + str(self.return_address_count)
        self.return_address_count += 1

        output = "// " + command + "\n"

        # push return address
        output += self.pushLabelAddressToStack(return_address)

        # push LCL
        output += self.pushVariableToStack("LCL")

        # push ARG
        output += self.pushVariableToStack("ARG")

        # push THIS
        output += self.pushVariableToStack("THIS")

        # push THAT
        output += self.pushVariableToStack("THAT")

        # ARG = SP - n - 5
        output += "@" + str(args) + "\n"  # D = n
        output += "D=A\n"
        output += "@SP\n"  # D = SP - n
        output += "D=M-D\n"
        output += "@5\n"  # D = D - 5 = SP - n - 5
        output += "D=D-A\n"
        output += "@ARG\n"  # ARG = D = SP - n - 5
        output += "M=D\n"

        # LCL = SP
        output += "@SP\n"  # D = SP
        output += "D=M\n"
        output += "@LCL\n"  # LCL = D
        output += "M=D\n"


        # GOTO function
        output += "@" + function_name + "\n"
        output += "0;JMP\n"

        # return address
        output += f"({return_address})\n"

        self.target.write(output)

    def pushVariableToStack(self, variable_name):
        # D = variable_value
        output = "@" + variable_name + "\n"
        output += "D=M\n"

        # push D to stack
        output += self.pushStack()
        return output

    def pushLabelAddressToStack(self, label_name):
        # D = label address
        output = "@" + label_name + "\n"
        output += "D=A\n"

        # push D to stack
        output += self.pushStack()
        return output

    def writeReturnFunction(self, command):
        output = "// " + command + "\n"

        # FRAME = LCL
        output += "@LCL\n"
        output += "D=M\n"
        output += "@FRAME\n"
        output += "M=D\n"

        # RET = * (FRAME - 5)
        output += self.point_arithmetic_operation("RET", "FRAME", "-", "5")

        # pop and push return value to arg[0]
        # *ARG = stack.pop()
        # D = stack.pop()
        output += self.popStack()
        output += "@ARG\n"
        output += "A=M\n"
        output += "M=D\n"

        # SP = ARG + 1
        output += "@ARG\n"
        output += "D=M\n"
        output += "@SP\n"
        output += "M=D+1\n"

        # That = * (FRAME - 1)
        output += self.point_arithmetic_operation("THAT", "FRAME", "-", "1")

        # THIS = * (FRAME - 2)
        output += self.point_arithmetic_operation("THIS", "FRAME", "-", "2")

        # ARG = * (FRAME - 3)
        output += self.point_arithmetic_operation("ARG", "FRAME", "-", "3")

        # LCL = * (FRAME - 4)
        output += self.point_arithmetic_operation("LCL", "FRAME", "-", "4")

        # GOTO RET
        output += "@RET\n"
        output += "A=M\n"
        output += "0;JMP\n"

        self.target.write(output)

    def point_arithmetic_operation(self, result, pointer, op, value):

        if int(value) == 1:
            output = "@" + pointer + "\n"
            output += "A=M" + op + "1\n"
            output += "D=M\n"
        else:
            # result = * (pointer (op) value)
            output = "@" + pointer + "\n"
            output += "D=M\n"
            output += "@" + value + "\n"
            output += "A=D" + op + "A\n"
            output += "D=M\n"

        output += "@" + result + "\n"
        output += "M=D\n"
        return output

    def writePushConstant(self, index):
        index = str(index)
        # D = index
        output = "@" + index + "\n"
        output += "D=A\n"

        # push D to SP
        output += self.pushStack()
        return output

    def writePushPointer(self, index):
        # D  = THIS/THAT
        output = "@" + self.pointer[index] + "\n"
        output += "D=M\n"

        # push D to stack
        output += self.pushStack()
        return output

    def getArithmeticAndLogicalCommand(self, command):
        # D = sp.pop()
        output = self.popStack()

        # num1 = D
        output += "@num1\n"
        output += "M=D\n"

        # D = sp.pop()
        output += self.popStack()

        # D = D (operator) num1
        output += "@num1\n"
        output += "D=D" + self.arithmetic_logical_commands[command] + "M\n"

        # sp.push D
        output += self.pushStack()
        return output

    # For both arithmetic and bitwise: -y and !y
    def getNegationCommand(self, command):
        # D = sp.pop()
        output = self.popStack()

        # D = -D or !D
        output += "D=" + self.negation_commands[command] + "D\n"

        # sp.push D
        output += self.pushStack()
        return output

    def getBooleanCommand(self, command):
        # D = sp.pop()
        output = self.popStack()

        # op = D
        output += "@op\n"
        output += "M=D\n"

        # D = sp.pop()
        output += self.popStack()

        # D = D - op
        output += "@op\n"
        output += "D=D-M\n"

        label_count = str(self.label_count)
        # If D = op, goto TRUE Label
        output += "@TRUE" + label_count + "\n"
        output += "D;" + self.boolean_commands[command] + "\n"
        # Else, D=0 and goto False Label
        output += "D=0\n"
        output += "@FALSE" + label_count + "\n"
        output += "0;JMP\n"

        # TRUE Body
        output += "(TRUE" + label_count + ")\n"
        output += "D=-1\n"

        # False Body, stack push D
        output += "(FALSE" + label_count + ")\n"
        output += self.pushStack()
        self.label_count += 1
        return output

    def close(self):
        self.target.close()

    def pushOtherSegments(self, segment, index):
        if segment == "temp":
            # addr = 5 + i
            base_addr = self.base_memory_segments[segment] + index
            output = "@" + str(base_addr) + "\n"
            output += "D=A\n"
        else:
            # D=i
            output = "@" + str(index) + "\n"
            output += "D=A\n"

            # D = segment + i
            output += "@" + self.base_memory_segments[segment] + "\n"
            output += "D=D+M\n"

        # addr = D = segment + i
        output += "@addr\n"
        output += "M=D\n"

        # D= *addr
        output += "@addr\n"
        output += "A=M\n"
        output += "D=M\n"

        # push D to stack
        output += self.pushStack()
        return output

    def writePopPointer(self, index):

        # D= stack.pop
        output = self.popStack()

        # THIS/THAT = D = *SP
        output += "@" + self.pointer[index] + "\n"
        output += "M=D\n"
        return output

    def popStack(self):
        # SP--
        output = "@SP\n"
        output += "M=M-1\n"

        # D = *SP
        output += "@SP\n"
        output += "A=M\n"
        output += "D=M\n"
        return output

    def pushStack(self):
        # push sp D
        output = "@SP\n"
        output += "AM=M+1\n"
        output += "A=A-1\n"
        output += "M=D\n"
        return output

    def writePopOtherSegments(self, segment, index):
        if segment == "temp":
            # addr = 5 + i
            base_addr = self.base_memory_segments[segment] + index
            output = "@" + str(base_addr) + "\n"
            output += "D=A\n"
        else:
            # D=i
            output = "@" + str(index) + "\n"
            output += "D=A\n"
            # D = segment + i
            output += "@" + self.base_memory_segments[segment] + "\n"
            output += "D=D+M\n"

        # addr = D = segment + i
        output += "@addr\n"
        output += "M=D\n"

        # D = stack.pop()
        output += self.popStack()

        # *addr = D = *SP
        output += "@addr\n"
        output += "A=M\n"
        output += "M=D\n"
        return output
