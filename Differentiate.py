from Parser import differentiate
import argparse
from Function_Parser import parse_function


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--var', default='x', type=str)
    parser.add_argument('expression')
    return parser


if __name__ == '__main__':
    arg_parser = parse_args().parse_args()
    var = arg_parser.var
    derivative = differentiate(var, arg_parser.expression).derivative()
    parsed_derivative = parse_function(derivative)
    print(parsed_derivative)
