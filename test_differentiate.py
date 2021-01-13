import unittest
from Parser import differentiate
import Function_Parser


class DifferentiateTests(unittest.TestCase):
    def test_differentiate_is_ok(self):
        derivative = differentiate('x', '2').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative), '0')
        derivative2 = differentiate('x', 'x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative2), '1')
        derivative3 = differentiate('x', '2x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative3), '2.0')
        derivative4 = differentiate('x', '2x - 1').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative4), '2.0')
        derivative5 = differentiate('x', 'x^2').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative5), '2.0x')
        derivative6 = differentiate('x', '2^x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative6),
                         'ln(2.0) * (2.0 ^ x)')
        derivative7 = differentiate('x', 'x^x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative7),
                         'exp(xln(x)) * (ln(x) + 1)')
        derivative8 = differentiate('x', 'exp(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative8), 'exp(x)')
        derivative9 = differentiate('x', 'sqrt(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative9),
                         '(-1) / (2sqrt(x))')
        derivative10 = differentiate('x', 'sh(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative10),
                         '(exp(x) * 0.5) + (exp((-x)) * 0.5)')
        derivative11 = differentiate('x', 'ch(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative11),
                         '(exp(x) * 0.5) - (exp((-x)) * 0.5)')
        derivative12 = differentiate(
                                    'x', '(x-y)(x+y)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative12), '2x')
        derivative13 = differentiate('x', 'xx').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative13), '2.0x')
        derivative14 = differentiate('x', '1+2x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative14), '2.0')
        derivative15 = differentiate('x', '(x-1)y').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative15), 'y')
        derivative16 = differentiate('x', '(x-1)20').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative16), '20.0')
        derivative17 = differentiate('x', 'x^2*x^2').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative17),
                         '4.0 * (x ^ 3.0)')
        derivative18 = differentiate('x', 'xx*x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative18),
                         '3.0 * (x ^ 2)')
        derivative19 = differentiate('x', '1/x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative19),
                         '(-1.0) / (x ^ 2)')
        derivative20 = differentiate('x', '1/x^7').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative20),
                         '(-7.0) * (x ^ (-8.0))')
        derivative21 = differentiate('x', 'yexp(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative21),
                         'exp(x) * y')
        derivative22 = differentiate('x', '12exp(x)y').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative22),
                         '(exp(x) * 12.0) * y')
        derivative23 = differentiate('x', 'exp(x)exp(x)').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative23),
                         '(exp(x) + exp(x)) * exp(x)')
        derivative0 = differentiate('x', 'x2x').derivative()
        self.assertEqual(Function_Parser.parse_function(derivative0), '4.0x')


if __name__ == '__main__':
    unittest.main()
