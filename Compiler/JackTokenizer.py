import os
import glob


class JackTokenizer:
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

    keywords = [
        'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
        'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'
    ]

    symbols = [
        "{", "}", "(", ")", "[", "]", ".",
        ",", ";", "+", "-", "*", "/", "&",
        "|", "<", ">", "=", "~"
    ]

    keywords_name = {
        1: "keyword",
        2: "symbol",
        3: "identifier",
        4: "integerConstant",
        5: "stringConstant"
    }

    def __init__(self):
        self.input_source = None
        self.output_file = None
        self.current_line = None
        self.current_token = None
        self.token_type = None
        self.next_token = None
        self.token_list = []

    def setNewFile(self, input_file):
        self.input_source = open(input_file)

        file_split = input_file.split(".")
        file_split[1] = ".vm"
        self.output_file = "".join(file_split)

        # Tokenize current file
        self.tokenize()

    def getOutputFile(self):
        return self.output_file

    def hasMoreTokens(self):
        if len(self.token_list) > 0:
            return True
        return False

    def advance(self):
        if self.hasMoreTokens():
            (self.current_token, self.token_type) = self.token_list[0]
            del self.token_list[0]
            return True
        else:
            return False

    def next(self, index = 0):
        if self.hasMoreTokens():
            token = self.token_list[index][0]
            return token
        else:
            return False

    def getToken(self):
        token = self.current_token

        if token == ">":
            token = "&gt;"
        elif token == "<":
            token = "&lt;"
        elif token == "&":
            token = "&amp;"
        return token

    def tokenType(self):
        return self.token_type

    def keyWord(self):
        if self.tokenType() == self.KEYWORD:
            return self.current_token
        return False

    def symbol(self):
        if self.tokenType() == self.SYMBOL:
            return self.current_token
        return False

    def identifier(self):
        if self.tokenType() == self.IDENTIFIER:
            return self.current_token
        return False

    def intVal(self):
        if self.tokenType() == self.INT_CONST:
            return self.current_token
        return False

    def stringVal(self):
        if self.tokenType() == self.STRING_CONST:
            return self.current_token
        return False

    def getTokenType(self):
        return self.keywords_name[self.token_type]

    def tokenize(self):
        line = self.getNextLine()
        while line:
            if line is None:
                break

            tokens = []
            is_string = False
            is_int = False
            string_const = "";
            int_const = "";
            identifier = ""
            is_keyword = False
            current_keyword = ""
            for c in line:
                identifier += c

                if is_keyword:
                    if c.isalpha():
                        identifier = current_keyword + c
                        is_keyword = False
                        current_keyword = ""
                    else:
                        tokens.append((current_keyword, self.KEYWORD))
                        is_keyword = False
                        current_keyword = ""

                if self.isKeyword(identifier):
                    # tokens.append((identifier, self.KEYWORD))

                    current_keyword = identifier
                    is_keyword = True
                    identifier = ""

                elif self.isSymbol(c) and is_string is False and is_int is False:
                    identifier = identifier[:-1]
                    identifier = self.clean(identifier)
                    if identifier:
                        tokens.append((identifier, self.IDENTIFIER))
                    tokens.append((c, self.SYMBOL))
                    identifier = ""
                elif (identifier.isnumeric() or is_int is True) and is_string is False:
                    if is_int is False:
                        int_const += c
                        is_int = True
                    elif is_int is True:
                        if not c.isnumeric():
                            is_int = False
                            tokens.append((int_const, self.INT_CONST))
                            int_const = ""
                            if self.isSymbol(c):
                                tokens.append((c, self.SYMBOL))
                        else:
                            int_const += c
                    identifier = ""
                elif c == " " and is_string is False and is_int is False:
                    identifier = identifier[:-1]
                    identifier = self.clean(identifier)
                    if identifier:
                        tokens.append((identifier, self.IDENTIFIER))
                        identifier = ""
                elif c == "\"" or is_string is True:
                    if is_string is False:
                        is_string = True
                    elif is_string is True:
                        if c == "\"":
                            is_string = False
                            tokens.append((string_const, self.STRING_CONST))
                            string_const = ""
                        else:
                            string_const += c
                    identifier = ""

            identifier = self.clean(identifier)
            if len(identifier) > 0:
                tokens.append((identifier, self.IDENTIFIER))

            self.token_list += tokens
            line = self.getNextLine()

    def isKeyword(self, token):
        return token in self.keywords

    def isSymbol(self, token):
        return token in self.symbols

    def isComment(self, text):
        # Remove white spaces and \n
        text = text.strip()
        return len(text) == 0 or text[0] == "/"

    def getNextLine(self):
        line = None
        multi_comment = False
        for line in self.input_source:
            # Start Multi Comment
            if "/**" in line:
                multi_comment = True

            # End Multi Comments
            if "*/" in line:
                multi_comment = False
                continue

            # Ignore blank line and comments
            if self.isComment(line) or multi_comment is True:
                continue

            line = self.clean(line)
            break

        return line

    def clean(self, line):
        # Ignore In line comments
        if "//" in line:
            index = line.find("//")
            line = line[0:index]

        line = line.strip()
        return line
