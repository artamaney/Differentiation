import unittest
import Parser
from Exceptions import (
    TooManyDotsException, TooManyOperatorsAtTimeException,
    NumberStartsWithDotException, IncorrectBracketsException,
    UndefinedSymbolException)


class ParserInitTests(unittest.TestCase):
    def test_parser_is_ok(self):
        self.assertEqual(Parser.parse_statement("0"), [0.0])
        self.assertEqual(Parser.parse_statement("123.05"), [123.05])
        self.assertEqual(Parser.parse_statement('1 - 2'), [1.0, 2.0, '-'])
        self.assertEqual(Parser.parse_statement('2x-3'),
                         [2.0, 'x', '*', 3.0, '-'])
        self.assertEqual(Parser.parse_statement('-1'), [1.0, 'um'])
        self.assertEqual(Parser.parse_statement('(-1)'), [1.0, 'um'])
        self.assertEqual(Parser.parse_statement('5^(7x)'), [5.0, 7.0, 'x',
                                                            '*', '^'])
        self.assertEqual(Parser.parse_statement('x/x'), ['x', 'x', '/'])
        self.assertEqual(Parser.parse_statement('(2*(x))'), [2.0, 'x', '*'])
        self.assertEqual(Parser.parse_statement('x^(-7*(227))     - 8'),
                         ['x', 7.0, 'um', 227.0, '*', '^', 8.0, '-'])
        self.assertEqual(Parser.parse_statement('x^(exp(2))'),
                         ['x', 2.0, 'exp', '^'])
        self.assertEqual(Parser.parse_statement('ln(x)'), ['x', 'ln'])
        self.assertEqual(Parser.parse_statement('cth(x) - 11'),
                         ['x', 'cth', 11, '-'])
        self.assertEqual(Parser.parse_statement('(x - y)(x + y)'),
                         ['x', 'y', '-', 'x', 'y', '+', '*'])
        self.assertEqual(Parser.parse_statement('cth(x) - th(x)'),
                         ['x', 'cth', 'x', 'th', '-'])
        self.assertEqual(Parser.parse_statement('2^3^4'), [2, 3, 4, '^', '^'])
        self.assertEqual(Parser.parse_statement('2*(-3)'), [2, 3, 'um', '*'])
        self.assertEqual(Parser.parse_statement('1 * 7 * x'),
                         [1, 7, '*', 'x', '*'])
        self.assertEqual(Parser.parse_statement('1+2x'), [1, 2, 'x', '*', '+'])

    def test_exceptions_are_ok(self):
        with self.assertRaises(TooManyDotsException):
            Parser.parse_statement('123.45.0')
            Parser.parse_statement('1.2...3')
        with self.assertRaises(TooManyOperatorsAtTimeException):
            Parser.parse_statement('1--2')
            Parser.parse_statement('1**2')
        with self.assertRaises(UndefinedSymbolException):
            Parser.parse_statement('х^2')  # this is russian х
            Parser.parse_statement('123,642')
        with self.assertRaises(NumberStartsWithDotException):
            Parser.parse_statement('.')
            Parser.parse_statement('.123')
        with self.assertRaises(IncorrectBracketsException):
            Parser.parse_statement('((')
            Parser.parse_statement('(x+y)y)')
            Parser.parse_statement('')


if __name__ == '__main__':
    unittest.main()
