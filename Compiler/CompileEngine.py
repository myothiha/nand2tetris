from JackTokenizer import JackTokenizer


class CompileEngine:
    classVarDec = ['static', 'field']

    types = ['int', 'char', 'boolean']

    return_types = ['int', 'char', 'boolean', 'void']

    subroutines = ['constructor', 'function', 'method']

    operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    unary_operators = ["-",  "~"]

    keyword_constant = ['true', 'false', 'null', 'this']

    def __init__(self, tokenizer):
        self.tokenizer = JackTokenizer()
        self.tokenizer = tokenizer
        self.token_buffer = list()
        output_file = tokenizer.getOutputFile()
        print(output_file)
        self.file = output_file
        self.output = open(output_file, "w")

    # Compile Complete Class
    def compileClass(self):
        indent = 1
        tokenizer = self.tokenizer
        self.writeOutput("<class>")

        # Keyword Class
        # Must be a keyword and class
        self.conditionalTerminal(indent - 1, JackTokenizer.KEYWORD, "class")

        # Class Name.
        # Must be identifier and must match filename
        self.conditionalTerminal(indent - 1, JackTokenizer.IDENTIFIER)

        # Must be a symbol and open bracket
        self.conditionalTerminal(indent - 1, JackTokenizer.SYMBOL, '{')

        # Compile class variable declaration.
        # For both static and field variable.
        while tokenizer.advance():
            token = tokenizer.getToken()
            if token in self.classVarDec:
                self.compileClassVarDec(indent)
            else:
                break

        # Compile Subroutines Declaration
        # Including constructors, functions and methods
        token = tokenizer.getToken()
        while True:
            if token in self.subroutines:
                self.compileSubroutine(indent)
            else:
                break
            tokenizer.advance()
            token = tokenizer.getToken()

        # Must be a symbol and close bracket
        self.conditionalTerminal(indent - 1, JackTokenizer.SYMBOL, '}')

        self.writeOutput("</class>")

    # Compile a static declaration or a field declaration.
    def compileClassVarDec(self, indent):
        tokenizer = self.tokenizer
        self.writeOutput("<classVarDec>", indent)

        # Write field or static keyword
        self.writeTerminalRules(indent)

        # Write Data Type
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.types:
            self.writeTerminalRules(indent)

        # Write var name List. e.g. x, y;
        while tokenizer.advance():
            token = tokenizer.getToken()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                self.writeTerminalRules(indent)
            elif token == ";":
                self.writeTerminalRules(indent)
                break
            else:
                if token == "," and tokenizer.tokenType() == JackTokenizer.SYMBOL:
                    self.writeTerminalRules(indent)

        self.writeOutput("</classVarDec>", indent)

    # Compile a Complete Method
    def compileSubroutine(self, indent):
        tokenizer = self.tokenizer
        self.writeOutput("<subroutineDec>", indent)

        # Write subroutines keyword such as constructor, function method
        self.writeTerminalRules(indent)

        # Write return data type
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.return_types:
            self.writeTerminalRules(indent)

        # Write Subroutine name
        tokenizer.advance()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            self.writeTerminalRules(indent)

        # Open Parentheses
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == "(":
            self.writeTerminalRules(indent)

        # Parameter List
        self.compileParameterList(indent + 1)

        # Close Parentheses
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == ")":
            self.writeTerminalRules(indent)

        # Subroutine Body
        self.compileSubroutineBody(indent + 1)

        # End of subroutine
        self.writeOutput("</subroutineDec>", indent)

    def compileSubroutineBody(self, indent):
        # Subroutine Body here
        tokenizer = self.tokenizer
        self.writeOutput("<subroutineBody>", indent)

        # open {
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, '{')

        # Variable Declaration
        self.compileVarDec(indent + 1)

        # Compile Statements
        self.compileStatements(indent + 1)

        # close }
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == "}":
            self.writeTerminalRules(indent)

        self.writeOutput("</subroutineBody>", indent)

    # Compile a (possibly empty) parameter list, not including the enclosing "()"
    def compileParameterList(self, indent):
        self.writeOutput("<parameterList>", indent)
        tokenizer = self.tokenizer
        while tokenizer.advance():
            token = tokenizer.getToken()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.types:
                self.writeTerminalRules(indent)
            elif tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                self.writeTerminalRules(indent)
            elif token == ")":
                break
            else:
                if token == "," and tokenizer.tokenType() == JackTokenizer.SYMBOL:
                    self.writeTerminalRules(indent)

        self.writeOutput("</parameterList>", indent)

    # Compile a var declaration.
    def compileVarDec(self, indent):
        tokenizer = self.tokenizer
        token = tokenizer.next()

        while token == "var":
            self.writeOutput("<varDec>", indent)

            # Write 'var'
            tokenizer.advance()
            self.writeTerminalRules(indent)

            # Type
            tokenizer.advance()
            self.writeTerminalRules(indent)

            # Write var name List. e.g. x, y;
            token = tokenizer.next()
            while token != ";":
                tokenizer.advance()
                token = tokenizer.getToken()
                if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                    self.writeTerminalRules(indent)
                else:
                    if token == "," and tokenizer.tokenType() == JackTokenizer.SYMBOL:
                        self.writeTerminalRules(indent)

                token = tokenizer.next()

            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ";")
            token = tokenizer.next()

            self.writeOutput("</varDec>", indent)

    # Compile a sequence of statements not including enclosing "{}"
    def compileStatements(self, indent):
        self.writeOutput("<statements>", indent)
        tokenizer = self.tokenizer
        token = tokenizer.next()

        while True:
            if token == 'let':
                self.compileLet(indent + 1)
            elif token == 'if' or token == 'else':
                self.compileIf(indent + 1)
            elif token == 'while':
                self.compileWhile(indent + 1)
            elif token == 'do':
                self.compileDo(indent + 1)
            elif token == 'return':
                self.compileReturn(indent + 1)

            token = tokenizer.next()

            if token == "}":
                break

        self.writeOutput("</statements>", indent)

    # Compile a do statement
    def compileDo(self, indent):
        self.writeOutput("<doStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Write 'do'
        self.writeTerminalRules(indent)

        # Subroutine Name
        tokenizer.advance()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            self.writeTerminalRules(indent)

        tokenizer.advance()

        # (Classame | Varname) '.' subroutineName
        token = tokenizer.getToken()
        if token == ".":
            self.writeTerminalRules(indent)

            tokenizer.advance()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                self.writeTerminalRules(indent)
                tokenizer.advance()

        # '(' expressionList ')'
        # Open bracket '('
        token = tokenizer.getToken()
        if token == "(":
            self.writeTerminalRules(indent)

        self.compileExpressionList(indent + 1)

        # Open bracket ')'
        tokenizer.advance()
        token = tokenizer.getToken()
        if token == ")":
            self.writeTerminalRules(indent)

        # End of Statement
        tokenizer.advance()
        self.writeEndOfSentence(indent)

        self.writeOutput("</doStatement>", indent)

    # Compile a Let statement
    def compileLet(self, indent):
        self.writeOutput("<letStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Write 'let'
        self.writeTerminalRules(indent)

        # Var Name. Todo might contain expression.
        tokenizer.advance()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            self.writeTerminalRules(indent)

        # If there is expression
        token = tokenizer.next()
        if token == "[":
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "[")
            self.compileExpression(indent + 1)
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "]")


        # Write '=' operator
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == '=':
            self.writeTerminalRules(indent)

        # Expression
        self.compileExpression(indent + 1)

        # End of Statement
        tokenizer.advance()
        self.writeEndOfSentence(indent)

        self.writeOutput("</letStatement>", indent)

    # Compile a while statement
    def compileWhile(self, indent):
        self.writeOutput("<whileStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Keyword 'while'
        self.writeTerminalRules(indent)

        # Open Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "(")

        self.compileExpression(indent + 1)

        # Close Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

        # Open Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "{")

        # Compile Statements
        self.compileStatements(indent + 1)

        # Open Close Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "}")

        self.writeOutput("</whileStatement>", indent)

    # Compile a return statement
    def compileReturn(self, indent):
        self.writeOutput("<returnStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Write 'return'
        self.writeTerminalRules(indent)

        token = tokenizer.next()
        if not token == ';':
            self.compileExpression(indent + 1)

        tokenizer.advance()
        self.writeEndOfSentence(indent)

        self.writeOutput("</returnStatement>", indent)

    # Compile an if statement
    def compileIf(self, indent):
        self.writeOutput("<ifStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Keyword 'if'
        self.writeTerminalRules(indent)

        # Open Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "(")

        self.compileExpression(indent + 1)

        # Close Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

        # Open Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "{")

        # Compile Statements
        self.compileStatements(indent + 1)

        # Open Close Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "}")

        # check if there is else statement
        if tokenizer.next() == "else":

            tokenizer.advance();
            # Keyword 'else'
            self.writeTerminalRules(indent)

            # Open Bracket
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "{")

            # Compile Statements
            self.compileStatements(indent + 1)

            # Open Close Bracket
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "}")

        self.writeOutput("</ifStatement>", indent)

    #  Todo Compile a (possible Empty), comma-separated list of expressions.
    def compileExpressionList(self, indent):
        self.writeOutput("<expressionList>", indent)
        tokenizer = self.tokenizer

        # Todo While Loop. Compile Expressions.
        #  Check if Empty and do nothing.
        token = tokenizer.next()
        while token != ")":
            self.compileExpression(indent + 1)
            token = tokenizer.next()
            if token == ",":
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ",")

        self.writeOutput("</expressionList>", indent)

    # Compile an expression
    def compileExpression(self, indent):
        self.writeOutput("<expression>", indent)
        tokenizer = self.tokenizer

        # Todo Expression Term
        self.compileTerm(indent + 1)

        token = tokenizer.next()

        if token in self.operators:
            while token != ";" and token != ")" and token != ",":
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL)
                self.compileTerm(indent + 1)

                token = tokenizer.next()


        self.writeOutput("</expression>", indent)

    # Compile a term. It is complex.
    # If it is an identifier we need to distinguish between variable, an array entry and subroutine call.
    def compileTerm(self, indent):
        self.writeOutput("<term>", indent)
        tokenizer = self.tokenizer

        tokenizer.advance()
        token_type = tokenizer.tokenType()
        token = tokenizer.getToken()

        if token_type == JackTokenizer.INT_CONST or token_type == JackTokenizer.STRING_CONST or token in self.keyword_constant or token in self.unary_operators:
            if token in self.unary_operators:
                self.writeTerminalRules(indent)
                self.compileTerm(indent + 1)
            else:
                self.writeTerminalRules(indent)
        elif token == "(":
            self.writeTerminalRules(indent)
            self.compileExpression(indent + 1)
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")
        elif token_type == JackTokenizer.IDENTIFIER:
            token = tokenizer.next()
            # Write Identifier
            self.writeTerminalRules(indent)

            # Array Operator
            if token == "[":
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "[")
                self.compileExpression(indent + 1)
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "]")
            # Or Sub routine call
            elif token == ".":
                # (Classame | Varname) '.' subroutineName
                # Write '.'
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL)

                # Write Identifier
                self.conditionalTerminal(indent, JackTokenizer.IDENTIFIER)

                # Write '('
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "(")

                # Expression List
                self.compileExpressionList(indent + 1)

                # Write ')'
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

        self.writeOutput("</term>", indent)

    # Utils
    def writeEndOfSentence(self, indent):
        tokenizer = self.tokenizer
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == ';':
            self.writeTerminalRules(indent)

    def conditionalTerminal(self, indent, tokenType, compareToken=None):
        tokenizer = self.tokenizer
        tokenizer.advance()
        token = tokenizer.getToken()

        if compareToken:
            if tokenizer.tokenType() == tokenType and token == compareToken:
                self.writeTerminalRules(indent)
        else:
            if tokenizer.tokenType() == tokenType:
                self.writeTerminalRules(indent)

    def writeOutput(self, s, indent=0):
        tokenizer = self.tokenizer
        tab = "  "
        initial = indent * tab
        h = self.output.write(initial + s + "\n")

    def writeTerminalRules(self, indent=0):
        tokenizer = self.tokenizer
        token_type = tokenizer.getTokenType()
        tab = "  "
        xml = f"{indent * tab}  <{token_type}> {tokenizer.getToken()} </{token_type}>"

        self.writeOutput(xml)
