import sys
from Parser import Parser
from CodeWriter import CodeWriter


def __main__():
    source_file = sys.argv[1]

    parser = Parser(source_file)
    # source.readline()

    code_writer = CodeWriter(source_file)
    print(parser.file_list)
    if parser.isMultipleFile:
        code_writer.writeBootstrap()

    while parser.hasMoreCommands():
        command = parser.advance()
        if parser.commandType() == Parser.C_ARITHMETIC:
            code_writer.writeArithmetic(command)
        elif parser.commandType() == Parser.C_IF:
            code_writer.writeIfGoto(command)
        elif parser.commandType() == Parser.C_GOTO:
            code_writer.writeGoto(command)
        elif parser.commandType() == Parser.C_LABEL:
            code_writer.writeLabel(command)
        elif parser.commandType() == Parser.C_CALL:
            code_writer.writeCallFunction(command, parser.arg1(), parser.arg2())
        elif parser.commandType() == Parser.C_FUNCTION:
            code_writer.writeHandleFunction(command, parser.arg1(), parser.arg2())
        elif parser.commandType() == Parser.C_RETURN:
            code_writer.writeReturnFunction(command)
        else:
            code_writer.writePushPop(command, parser.commandType(), parser.arg1(), parser.arg2(),
                                     parser.get_current_source_file())

    code_writer.close()


__main__()
