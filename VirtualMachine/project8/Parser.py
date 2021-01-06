import os
import glob


class Parser:
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8

    file_list = []
    arithmetic_operations = [
        "add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"
    ]

    stack_operations = [
        "push", "pop"
    ]

    def __init__(self, source_file):
        self.currentCommand = None
        self.source = None
        self.nextCommand = None
        self.current_source_file = None
        self.isDir = False
        if os.path.isfile(source_file):
            self.file_list.append(source_file)
        else:
            self.file_list = glob.glob(source_file + "/*.vm")
            if len(self.file_list) > 1:
                self.isDir = True

        self.setFileName()

    def get_current_source_file(self):
        filename = self.current_source_file.split(".")[0].split("/")[-1]
        return filename

    def setFileName(self):
        source_file = self.file_list[0]
        self.current_source_file = source_file
        source = open(source_file, 'r')
        self.source = source
        self.nextCommand = self.getNextCommand()

        del self.file_list[0]

    def emptyFileList(self):
        return not bool(self.file_list)

    def hasMoreCommands(self):
        return bool(self.nextCommand)

    def advance(self):
        if self.hasMoreCommands():
            self.currentCommand = self.nextCommand
            self.nextCommand = self.getNextCommand()

            if self.nextCommand is None:
                if not self.emptyFileList():
                    self.setFileName()
        else:
            self.source.close()
            return None

        return self.currentCommand

    def commandType(self):
        if self.currentCommand:
            if self.currentCommand in self.arithmetic_operations:
                return self.C_ARITHMETIC
            elif "pop" in self.currentCommand:
                return self.C_POP
            elif "push" in self.currentCommand:
                return self.C_PUSH
            elif "function" in self.currentCommand:
                return self.C_FUNCTION
            elif "label" in self.currentCommand:
                return self.C_LABEL
            elif "if-goto" in self.currentCommand:
                return self.C_IF
            elif "goto" in self.currentCommand:
                return self.C_GOTO
            elif "return" in self.currentCommand:
                return self.C_RETURN
            elif "call" in self.currentCommand:
                return self.C_CALL

    def arg1(self):
        current_command = self.currentCommand

        if self.commandType() in [self.C_ARITHMETIC, self.C_RETURN]:
            return current_command

        arguments = current_command.split(" ")

        return arguments[1]

    def arg2(self):
        current_command = self.currentCommand

        if self.commandType() in [self.C_PUSH, self.C_POP, self.C_FUNCTION, self.C_CALL]:
            arguments = current_command.split(" ")
            return int(arguments[2])

    def getNextCommand(self):
        line = None
        for line in self.source:

            # Ignore blank line and comments
            if self.isComment(line):
                continue

            # Ignore In line comments
            if "//" in line:
                index = line.find("//")
                line = line[0:index]

            line = line.strip()
            break

        return line

    def isComment(self, text):
        # Remove white spaces and \n
        text = text.strip()
        return len(text) == 0 or text[0] == "/"
