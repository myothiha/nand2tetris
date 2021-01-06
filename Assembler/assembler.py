import sys

instruction_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"

}

dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_table = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}

variable = {
    "last_address": 16
}

def parser(instruction):
    # A-Instructions
    if instruction.startswith("@"):

        # Get Data Part of A-Instruction
        data = instruction[1:]

        error = False

        try:
            sss = data
            # If data part is integer
            data = int(data)
        except ValueError:
            error = True
        except SyntaxError:
            error = True

        if error:
            # If data part is string
            if data in symbol_table:
                data = symbol_table[data]
            else:
                symbol_table[data] = variable["last_address"]
                data = variable["last_address"]
                variable["last_address"] += 1

        # Convert constant value to binary
        return encode_A_instruction(data)

    # C-Instructions
    else:
        dest = "null"
        jump = "null"
        comp = "0"

        if "=" in instruction and ";" in instruction:
            first_part = instruction.split("=")
            dest = first_part[0]
            second_part = first_part[1]
            second = second_part.split(";")
            jump = second[1]
            comp = second[0]
        else:
            if "=" in instruction:
                split = instruction.split("=")
                dest = split[0]
                comp = split[1]

            if ';' in instruction:
                split = instruction.split(";")
                jump = split[1]
                comp = split[0]

        encode = encode_C_Instruction(dest, comp, jump)
        return encode


def encode_A_instruction(data):
    if isinstance(data, str):
        print(data)
    binary = "{0:016b}".format(data)
    return binary


def encode_C_Instruction(dest, comp, jump):
    return "111" + instruction_table[comp] + dest_table[dest] + jump_table[jump]


source = sys.argv[1]
handle = open(source, 'r')

# first pass
i = 0 # Track Instruction Address
for line in handle:

    # Remove white spaces and \n
    text = line.strip()

    # Ignore blank line and comments
    if len(text) == 0 or text[0] == "/":
        continue

    # Ignore In line comments
    if "//" in text:
        index = text.find("//")
        text = text[0:index]
        text = text.strip()

    # Identify Label
    if text.startswith("("):

        # Remove parenthesis
        label = text.replace("(", "").replace(")", "")

        # Next Address
        address = i

        # Register in Symbol Table
        symbol_table[label] = address
        continue

    i += 1

# Reset File point to the beginning of the file
handle.seek(0)

target = source.split(".")[0] + ".hack"
f = open(target, "w")

# Loop each line
for line in handle:

    # Remove white spaces. such as \n
    text = line.strip()

    # Skip if blank line or comments
    if len(text) == 0 or text[0] == "/":
        continue

    # Skip labels
    if text.startswith("("):
        continue

    # Ignore in line comments
    if "//" in text:
        index = text.find("//")
        text = text[0:index]
        text = text.strip()

    # Translate the line into machine language
    encoded = parser(text)
    f.write(encoded + "\n")

# print(symbol_table)
f.close()
