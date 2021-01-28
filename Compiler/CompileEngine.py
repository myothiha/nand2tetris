from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from CodeWriter import CodeWriter


class CompileEngine:
    classVarDec = ['static', 'field']

    types = ['int', 'char', 'boolean']

    return_types = ['int', 'char', 'boolean', 'void']

    subroutines = ['constructor', 'function', 'method']

    operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    unary_operators = ["-", "~"]

    keyword_constant = ['true', 'false', 'null', 'this']

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable()
        self.token_buffer = list()
        self.label_index = 0
        output_file = tokenizer.getOutputFile()
        self.code_writer = CodeWriter(output_file)
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
        self.conditionalTerminal(indent - 1, JackTokenizer.IDENTIFIER, category="Class")
        self.className = tokenizer.getToken()

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
        kind = tokenizer.getToken()
        self.writeTerminalRules(indent)

        # Write Data Type
        tokenizer.advance()
        token = tokenizer.getToken()
        data_type = token
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.types:
            self.writeTerminalRules(indent)

        # Write var name List. e.g. x, y;
        while tokenizer.advance():
            token = tokenizer.getToken()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                self.symbol_table.define(token, data_type, kind)
                self.writeTerminalRules(indent, category=kind, define=True)
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

        # Reset subroutine symbol table
        self.symbol_table.startSubroutine()

        # Write subroutines keyword such as constructor, function method
        # Handling Constructor and Method
        is_constructor = False
        is_method = False
        if tokenizer.getToken() == "constructor":
            is_constructor = True
        elif tokenizer.getToken() == "method":
            is_method = True

        self.writeTerminalRules(indent)

        # Write return data type
        tokenizer.advance()
        token = tokenizer.getToken()
        return_type = token
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.return_types:
            self.writeTerminalRules(indent)

        # Write Subroutine name
        tokenizer.advance()
        subroutine_name = tokenizer.getToken()

        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            self.writeTerminalRules(indent, category="subroutine")

        # Open Parentheses
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == "(":
            self.writeTerminalRules(indent)

        # Parameter List
        param_count = self.compileParameterList(indent + 1)

        # Close Parentheses
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == ")":
            self.writeTerminalRules(indent)

        # Subroutine Body
        self.compileSubroutineBody(subroutine_name, indent + 1, is_constructor, is_method)

        # End of subroutine
        self.writeOutput("</subroutineDec>", indent)

    # Compile a (possibly empty) parameter list, not including the enclosing "()"
    def compileParameterList(self, indent):
        self.writeOutput("<parameterList>", indent)
        tokenizer = self.tokenizer
        data_type = None
        param_count = 0
        while tokenizer.advance():
            token = tokenizer.getToken()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER or token in self.types:
                if not data_type:
                    data_type = token
                else:
                    # Register the param in symbol table
                    self.symbol_table.define(token, data_type, SymbolTable.ARG)
                    param_count += 1
                    data_type = None
                self.writeTerminalRules(indent, category=SymbolTable.ARG, define=True)
            elif tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                self.writeTerminalRules(indent)
            elif token == ")":
                break
            else:
                if token == "," and tokenizer.tokenType() == JackTokenizer.SYMBOL:
                    self.writeTerminalRules(indent)

        self.writeOutput("</parameterList>", indent)
        return param_count

    def compileSubroutineBody(self, subroutine_name, indent, is_constructor=False, is_method=False):
        # Subroutine Body here
        tokenizer = self.tokenizer
        self.writeOutput("<subroutineBody>", indent)

        # open {
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, '{')

        # Variable Declaration
        local_var_count = self.compileVarDec(indent + 1)

        # compile subroutine signature
        self.code_writer.writeFunction(self.className + "." + subroutine_name, local_var_count)

        if is_constructor:
            # If current subroutine is a constructor, handle object creation logic here.
            no_of_fields = self.symbol_table.varCount(SymbolTable.FIELD)
            # Push Number of fields declared in class level
            self.code_writer.writePush(CodeWriter.CONST, no_of_fields)
            # Allocate a Memory segment for current object
            self.code_writer.writeCall("Memory.alloc", "1")
            self.code_writer.writePop(CodeWriter.POINTER, "0")
        elif is_method:
            # Compiler Handle Method Compilation
            # Anchor arg0 to this
            self.code_writer.writePush(CodeWriter.ARG, "0")
            self.code_writer.writePop(CodeWriter.POINTER, "0")

        # Compile Statements
        self.compileStatements(indent + 1, is_constructor)

        # close }
        tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == "}":
            self.writeTerminalRules(indent)

        self.writeOutput("</subroutineBody>", indent)
        return local_var_count

    # Compile a var declaration.
    def compileVarDec(self, indent):
        tokenizer = self.tokenizer
        token = tokenizer.next()

        count = 0
        while token == "var":
            self.writeOutput("<varDec>", indent)

            # Write 'var'
            tokenizer.advance()
            self.writeTerminalRules(indent)

            # Write Data Type
            tokenizer.advance()
            data_type = tokenizer.getToken()
            self.writeTerminalRules(indent)

            # Write var name List. e.g. x, y;
            token = tokenizer.next()
            while token != ";":
                tokenizer.advance()
                token = tokenizer.getToken()
                if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:

                    # Register Local vars in Symbol table
                    self.symbol_table.define(token, data_type, SymbolTable.VAR)
                    count += 1

                    self.writeTerminalRules(indent, category=SymbolTable.VAR, define=True)
                else:
                    if token == "," and tokenizer.tokenType() == JackTokenizer.SYMBOL:
                        self.writeTerminalRules(indent)

                token = tokenizer.next()

            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ";")
            token = tokenizer.next()

            self.writeOutput("</varDec>", indent)
        return count

    # Compile a sequence of statements not including enclosing "{}"
    def compileStatements(self, indent, is_constructor=False):
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
                self.compileDo(indent + 1, is_constructor)
            elif token == 'return':
                self.compileReturn(indent + 1, is_constructor)

            token = tokenizer.next()

            if token == "}":
                break

        self.writeOutput("</statements>", indent)

    # Compile a do statement
    def compileDo(self, indent, is_constructor=False):
        self.writeOutput("<doStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Write 'do'
        self.writeTerminalRules(indent)

        # Subroutine Name
        is_method = False
        method_within_class = False
        outside_function = False
        var_name = None
        tokenizer.advance()
        subroutine_name = tokenizer.getToken()

        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            if tokenizer.next() == ".":

                # Check if classname or variable. In other word, check if it is an object
                if self.symbol_table.isObject(subroutine_name):
                    var_name = subroutine_name
                    subroutine_name = self.symbol_table.typeOf(var_name)
                    is_method = True
                else:
                    is_method = False
                    outside_function = True

                subroutine_name += tokenizer.next()
                self.writeTerminalRules(indent, category="class")
            else:
                self.writeTerminalRules(indent, category="subroutine")

        tokenizer.advance()

        # (Classame | Varname) '.' subroutineName
        token = tokenizer.getToken()
        if token == ".":
            self.writeTerminalRules(indent)

            tokenizer.advance()
            if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
                subroutine_name += tokenizer.getToken()
                self.writeTerminalRules(indent, category='subroutine')
                tokenizer.advance()

        # '(' expressionList ')'
        # Open bracket '('
        token = tokenizer.getToken()
        if token == "(":
            self.writeTerminalRules(indent)

        # If it is a object method, push this first before other arguments
        if is_method:
            self.code_writer.writePush(self.symbol_table.kindOf(var_name), self.symbol_table.indexOf(var_name))

        # Check if there is only subroutine name like draw(),
        # then it should be classname.draw()
        if "." not in subroutine_name:
            method_within_class = True
            subroutine_name = self.className + "." + subroutine_name
            self.code_writer.writePush(CodeWriter.POINTER, "0")

        nArgs = self.compileExpressionList(indent + 1)

        # Open bracket ')'
        tokenizer.advance()
        token = tokenizer.getToken()
        if token == ")":
            self.writeTerminalRules(indent)

        # Call function call
        if (is_method or is_constructor or method_within_class) and not outside_function:
            nArgs += 1

        self.code_writer.writeCall(subroutine_name, nArgs)

        # remove unused return value, because it's void method
        self.code_writer.writePop(CodeWriter.TEMP, "0")

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

        # Var Name.
        tokenizer.advance()
        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER:
            var_name = tokenizer.getToken()
            self.writeTerminalRules(indent, category=SymbolTable.VAR)

        # If there is expression
        # Todo Compiler Need to Handle Array
        token = tokenizer.next()
        is_array = False
        if token == "[":
            is_array = True
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "[")
            self.compileExpression(indent + 1)
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "]")

            # VM Code Generation for Array
            # push Arr
            self.code_writer.writePush(self.symbol_table.kindOf(var_name), self.symbol_table.indexOf(var_name))

            # Expression
            self.compileExpression(indent + 1)

            # Add
            self.code_writer.writeArithmetic("+")

        # Write '=' operator
        if not is_array:
            tokenizer.advance()
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == '=':
            self.writeTerminalRules(indent)

        # Expression
        self.compileExpression(indent + 1, is_array=True)

        # if it is an array.
        if is_array:
            # Add
            self.code_writer.writePop(CodeWriter.TEMP, "0")
            self.code_writer.writePop(CodeWriter.POINTER, "1")
            self.code_writer.writePush(CodeWriter.TEMP, "0")
            self.code_writer.writePop(CodeWriter.THAT, "0")
        else:
            # Assign Evaluated Expression (Top most value of the stack) to variable
            self.code_writer.writePop(self.symbol_table.kindOf(var_name), self.symbol_table.indexOf(var_name))

        # End of Statement
        tokenizer.advance()
        self.writeEndOfSentence(indent)
        is_array = False

        self.writeOutput("</letStatement>", indent)

    # Compile a while statement
    def compileWhile(self, indent):
        self.writeOutput("<whileStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        lbl_indx = self.getLabel()
        start_while_label = "startwhile" + lbl_indx
        self.code_writer.writeLabel(start_while_label)

        # Keyword 'while'
        self.writeTerminalRules(indent)

        # Open Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "(")

        self.compileExpression(indent + 1)
        self.code_writer.writeArithmetic("~")

        # If conditional is false, end the loop
        end_while_label = "endwhile" + lbl_indx
        self.code_writer.writeIf(end_while_label)

        # Close Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

        # Open Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "{")

        # Compile Statements
        self.compileStatements(indent + 1)

        # continue to loop
        self.code_writer.writeGoto(start_while_label)

        # Open Close Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "}")

        self.writeOutput("</whileStatement>", indent)

        self.code_writer.writeLabel(end_while_label)

    # Compile a return statement
    def compileReturn(self, indent, is_constructor=False):
        self.writeOutput("<returnStatement>", indent)
        tokenizer = self.tokenizer
        tokenizer.advance()

        # Write 'return'
        self.writeTerminalRules(indent)

        token = tokenizer.next()
        # Todo Compile Handle return value
        if not token == ';':
            if is_constructor:
                self.code_writer.writeReturn(is_constructor=is_constructor)
                tokenizer.advance()
            else:
                self.compileExpression(indent + 1)
                self.code_writer.writeReturn()
        else:
            # Return statement
            self.code_writer.writeReturn(return_type="void")

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
        # not the expression
        self.code_writer.writeArithmetic("~")

        # Goto Else if not(expression)
        lbl_indx = self.getLabel()
        start_if = "else_label" + lbl_indx

        # Endif Label
        end_if = "endif_label" + lbl_indx
        self.code_writer.writeIf(start_if)

        # Close Parentheses
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

        # Open Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "{")

        # Compile Statements
        self.compileStatements(indent + 1)

        # Open Close Bracket
        self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "}")

        # Goto EndIf
        self.code_writer.writeGoto(end_if)

        # Else label
        self.code_writer.writeLabel(start_if)

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

        # End if Label
        self.code_writer.writeLabel(end_if)

    # Compile a (possible Empty), comma-separated list of expressions.
    def compileExpressionList(self, indent):
        self.writeOutput("<expressionList>", indent)
        tokenizer = self.tokenizer

        #  Compile Expressions.
        #  Check if Empty and do nothing.
        token = tokenizer.next()
        arg_count = 0
        while token != ")":
            self.compileExpression(indent + 1)
            token = tokenizer.next()
            if token == ",":
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ",")
            arg_count += 1

        self.writeOutput("</expressionList>", indent)
        return arg_count

    # Compile an expression
    def compileExpression(self, indent, is_array=False):
        self.writeOutput("<expression>", indent)
        tokenizer = self.tokenizer

        # Expression Term
        self.compileTerm(indent + 1, is_array=is_array)

        token = tokenizer.next()

        op = None
        if token in self.operators:
            while token != ";" and token != ")" and token != ",":
                op = token
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL)
                self.compileTerm(indent + 1)

                # If there is operator, before current value, push it after the value.
                if op:
                    self.code_writer.writeArithmetic(op)
                    op = None

                token = tokenizer.next()

        self.writeOutput("</expression>", indent)

    # Compile a term. It is complex.
    # If it is an identifier we need to distinguish between variable, an array entry and subroutine call.
    def compileTerm(self, indent, is_array=False):
        self.writeOutput("<term>", indent)
        tokenizer = self.tokenizer

        tokenizer.advance()
        token_type = tokenizer.tokenType()
        token = tokenizer.getToken()

        op = None
        subroutine_call = None
        # If the term is a constant
        if token_type == JackTokenizer.INT_CONST \
                or token_type == JackTokenizer.STRING_CONST \
                or token in self.keyword_constant \
                or token in self.unary_operators:

            if token in self.unary_operators:
                op = token
                if token == "-":
                    op = "neg"
                self.writeTerminalRules(indent)
                self.compileTerm(indent + 1)
            else:
                # If it is integer constant, push const integer_value
                if token_type == JackTokenizer.INT_CONST:
                    self.code_writer.writePush(CodeWriter.CONST, token)
                elif token == "true":
                    self.code_writer.writePush(CodeWriter.CONST, "0")
                    self.code_writer.writeArithmetic("~")
                elif token == "false":
                    self.code_writer.writePush(CodeWriter.CONST, "0")
                elif token == "this":
                    self.code_writer.writePush(CodeWriter.POINTER, "0")
                elif token_type == JackTokenizer.STRING_CONST:
                    string = token
                    str_len = len(string)
                    self.code_writer.writePush(CodeWriter.CONST, str_len)
                    self.code_writer.writeCall("String.new", "1")

                    for c in string:
                        self.code_writer.writePush(CodeWriter.CONST, ord(c))
                        self.code_writer.writeCall("String.appendChar", "2")

                # If there is operator, before current value, push it after the value.
                # if op:
                #     self.code_writer.writeArithmetic(op)
                #     op = None

                self.writeTerminalRules(indent)
        # if the term contain another expression (expression)
        elif token == "(":
            self.writeTerminalRules(indent)
            self.compileExpression(indent + 1)
            self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")
        elif token_type == JackTokenizer.IDENTIFIER:
            subroutine_call = token
            token = tokenizer.next()

            if not subroutine_call:
                self.writeTerminalRules(indent, category=SymbolTable.VAR)

            # if the term is array
            if token == "[":
                var_name = tokenizer.getToken()
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "[")
                self.compileExpression(indent + 1)
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "]")
                self.code_writer.writePush(self.symbol_table.kindOf(var_name), self.symbol_table.indexOf(var_name))
                self.code_writer.writeArithmetic("+")
                self.code_writer.writePop(CodeWriter.POINTER, "1")
                self.code_writer.writePush(CodeWriter.THAT, "0")

            # Or Sub routine call
            elif token == ".":
                # (Classame | Varname) '.' subroutineName
                # Check if classname or variable. In other word, check if it is an object
                is_method = False
                if self.symbol_table.isObject(subroutine_call) and tokenizer == ".":
                    var_name = subroutine_call
                    print(var_name)
                    subroutine_call = self.symbol_table.typeOf(var_name)
                    is_method = True

                # Write '.'
                subroutine_call += token
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL)

                # Write Identifier
                self.conditionalTerminal(indent, JackTokenizer.IDENTIFIER, 'subroutine')

                # Todo Compiler need to advance token
                subroutine_call += tokenizer.getToken()

                # Write '('
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, "(")

                # If it is a object method, push this first before other arguments
                if is_method:
                    self.code_writer.writePush(self.symbol_table.kindOf(var_name), self.symbol_table.indexOf(var_name))

                # Expression List
                arg_count = self.compileExpressionList(indent + 1)

                # Write ')'
                self.conditionalTerminal(indent, JackTokenizer.SYMBOL, ")")

                # Call function
                if is_method:
                    arg_count += 1

                self.code_writer.writeCall(subroutine_call, arg_count)
            # if the term is simple variable
            else:
                identifier = subroutine_call
                self.code_writer.writePush(self.symbol_table.kindOf(identifier), self.symbol_table.indexOf(identifier))

        self.writeOutput("</term>", indent)

        # If there is operator, before current value, push it after the value.
        if op:
            self.code_writer.writeArithmetic(op)
            op = None

    # Utils
    def writeEndOfSentence(self, indent):
        tokenizer = self.tokenizer
        token = tokenizer.getToken()
        if tokenizer.tokenType() == JackTokenizer.SYMBOL and token == ';':
            self.writeTerminalRules(indent)

    def conditionalTerminal(self, indent, tokenType, compareToken=None, category=None, define=False):
        tokenizer = self.tokenizer
        tokenizer.advance()
        token = tokenizer.getToken()

        if compareToken:
            if tokenizer.tokenType() == tokenType and token == compareToken:
                self.writeTerminalRules(indent, category, define)
        else:
            if tokenizer.tokenType() == tokenType:
                self.writeTerminalRules(indent, category)

    def writeOutput(self, s, indent=0):
        tokenizer = self.tokenizer
        tab = "  "
        initial = indent * tab
        # h = self.output.write(initial + s + "\n")

    def writeTerminalRules(self, indent=0, category=None, define=False):
        tokenizer = self.tokenizer
        token_type = tokenizer.getTokenType()
        tab = "  "

        if tokenizer.tokenType() == JackTokenizer.IDENTIFIER and category:
            self.writeCategory(category, define, indent + 1)

        else:
            xml = f"{indent * tab}  <{token_type}> {tokenizer.getToken()} </{token_type}>"
            self.writeOutput(xml)

    def writeCategory(self, category, define, indent=0):
        tokenizer = self.tokenizer
        token_type = tokenizer.getTokenType()

        self.writeOutput(f"<{token_type}>", indent)
        self.writeOutput(f"<value>{tokenizer.getToken()}</value>", indent + 1)

        if category:
            self.writeOutput(f"<category> {category} </category>", indent + 1)

            if category in SymbolTable.variables:
                name = tokenizer.getToken()
                index = self.symbol_table.indexOf(name)
                self.writeOutput(f"<index> {index} </index>", indent + 1)

                if define:
                    self.writeOutput("<define> true </define>", indent + 1)
                else:
                    self.writeOutput("<define> false </define>", indent + 1)

        self.writeOutput(f"</{token_type}>", indent)

    def getLabel(self):
        self.label_index += 1
        return str(self.label_index)
