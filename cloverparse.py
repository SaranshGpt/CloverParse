import argparse

from preprocessor.import_file import import_file
from syntax.parse import parse_program

def __main__():
    # parser = argparse.ArgumentParser(description="CloverParse Command Line Interface")
    # parser.add_argument("input_file", help="Path to the input file to be parsed")
    # parser.add_argument("-o", "--output", help="Path to the output file", default="output.txt")

    # args = parser.parse_args()

    # input_path = args.input_file
    # output_path = args.output

    input_path = "pattern"
    output_path = "output.clv"

    program, pattern = import_file(input_path)

    expression = parse_program(program, pattern)

    bytecode = expression.serialize()

    with open(output_path, 'wb') as output_file:
        hex_data = bytecode.hex()
        output_file.write((hex_data + "\n").encode("ascii"))

    print(f"Bytecode written to {output_path}")

if __name__ == "__main__":
    __main__()