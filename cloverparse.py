import argparse

from parser.parser import parse_file

from primitives.expression import Expression

def __main__():
    parser = argparse.ArgumentParser(description="CloverParse Command Line Interface")
    parser.add_argument("input_file", help="Path to the input file to be parsed")
    parser.add_argument("-o", "--output", help="Path to the output file", default="output.txt")
    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output

    symbol_table, pattern_expression = parse_file(input_path)

    if pattern_expression is None:
        print("No pattern expression found in the input file.")
        return

    ret: bytes = pattern_expression.serialize()

    with open(output_path, "wb") as output_file:
        output_file.write(ret.hex().encode("ascii"))

    print(f"Output written to {output_path}")

if __name__ == "__main__":
    __main__()