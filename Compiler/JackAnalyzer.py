import sys
import os
import glob

from JackTokenizer import JackTokenizer
from CompileEngine import CompileEngine


def __main__():
    file_list = []
    input_source = sys.argv[1]

    if os.path.isfile(input_source):
        file_list.append(input_source)
    else:
        file_list = glob.glob(input_source + "/*.jack")

    tokenizer = JackTokenizer()

    for file in file_list:
        tokenizer.setNewFile(file)
        compile_engine = CompileEngine(tokenizer)
        compile_engine.compileClass()

    # for file in file_list:
    #     tokenizer.setNewFile(file)
    #     output_file = tokenizer.getOutputFile()
    #     output = open(output_file, "w")
    #     count = 0
    #     output.write("<tokens>\n")
    #     while tokenizer.advance():
    #         if output_file is not tokenizer.getOutputFile():
    #             output.write("</tokens>\n")
    #             output.close()
    #             output_file = tokenizer.getOutputFile()
    #             output = open(output_file, "w")
    #             output.write("<tokens>\n")
    #         count += 1
    #         token_type = tokenizer.getTokenType()
    #         xml = f"<{token_type}> {tokenizer.getToken()} </{token_type}>\n"
    #         output.write(xml)
    #
    #     output.write("</tokens>\n")


__main__()
