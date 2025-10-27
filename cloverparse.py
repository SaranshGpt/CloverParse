import argparse

import tokensizer as tkn

def __main__():
    parser = argparse.ArgumentParser(description="CloverParse Command Line Interface")
    parser.add_argument("input_file", help="Path to the input file to be parsed")
    parser.add_argument("-o", "--output", help="Path to the output file", default="output.txt")

    args = parser.parse_args()

    