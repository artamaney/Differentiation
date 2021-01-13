try:
    from Differentiate import var
except ImportError:
    var = 'x'


class Number:
    def __init__(self, value, has_var=False, letter=False):
        self.value = value
        self.has_var = has_var
        self.letter = letter

    def derivative(self):
        if self.value == var:
            return Number(1)
        return Number(0)


class UnaryMinus:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Multiply(Number(-1), self.right.derivative(), self.has_var)
        return Number(0)


class Minus:
    def __init__(self, left, right, has_var=False):
        self.left = left
        self.right = right
        self.has_var = has_var

    def derivative(self):
        return Minus(self.left.derivative(), self.right.derivative(),
                     self.has_var)


class Plus:
    def __init__(self, left, right, has_var=False):
        self.left = left
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if not self.has_var:
            return Number(0)
        return Plus(self.left.derivative(), self.right.derivative(),
                    self.has_var)


class Multiply:
    def __init__(self, left, right, has_var=False):
        self.left = left
        self.right = right
        self.has_var = has_var or left.has_var or right.has_var

    def derivative(self):
        if not self.has_var:
            return Number(0)
        left_name = type(self.left).__name__
        right_name = type(self.right).__name__
        if (((left_name == 'Minus' and right_name == 'Plus') or
            (left_name == 'Plus' and right_name == 'Minus')) and
                self.left.right.value == self.right.right.value and
                self.left.left.value == self.right.left.value):
            if self.left.has_var:
                return Power(self.left.left, Number(2), True).derivative()
            elif self.right.has_var:
                return Power(self.right.right, Number(2), True).derivative()
        return Plus(Multiply(self.left.derivative(), self.right,
                             self.left.has_var),
                    Multiply(self.right.derivative(), self.left,
                             self.right.has_var), self.has_var)


class Divisor:
    def __init__(self, left, right, has_var=False):
        self.left = left
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if not self.has_var:
            return Number(0)
        return Divisor(
            Minus(Multiply(self.left.derivative(), self.right, self.has_var),
                  Multiply(self.right.derivative(), self.left), self.has_var),
            Power(self.right, Number(2), self.has_var), self.has_var)


class Power:
    def __init__(self, left, right, has_var=False):
        self.left = left
        self.right = right
        self.has_var = has_var or left.has_var or right.has_var

    def derivative(self):
        if self.left.has_var and not self.right.has_var:
            return Multiply(self.right, Power(self.left,
                                              Minus(self.right, Number(1))))
        if not self.left.has_var and self.right.has_var:
            return Multiply(Ln(self.left),
                            Multiply(self, self.right.derivative()),
                            self.has_var)
        if self.left.has_var and self.right.has_var:
            return Multiply(Exp(Multiply(self.right, Ln(self.left))),
                            Multiply(self.left, Ln(self.right, self.has_var),
                                     self.has_var).derivative(), self.has_var)
        return Number(0, var)


class Sqrt:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Divisor(UnaryMinus(self.right.derivative(),
                                      self.right.has_var),
                           Multiply(Number(2), Sqrt(self.right)))
        return Number(0)


class Exp:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Multiply(self, self.right.derivative(), self.has_var)
        return Number(0)


class Ln:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Multiply(self.right.derivative(),
                            Divisor(Number(1), self.right, self.has_var),
                            self.has_var)
        return Number(0)


class Sh:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Multiply(Number(0.5),
                            Minus(Exp(self.right, self.has_var),
                                  Exp(UnaryMinus(self.right, self.has_var),
                                      self.has_var),
                                  self.has_var).derivative(), self.has_var)
        return Number(0)


class Ch:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Multiply(Number(0.5),
                            Plus(Exp(self.right, self.has_var),
                                 Exp(UnaryMinus(self.right, self.has_var),
                                     self.has_var),
                                 self.has_var).derivative(), self.has_var)
        return Number(0)


class Th:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Divisor(
                Multiply(Number(4), self.right.derivative()),
                Power(Plus(Exp(self.right, self.has_var),
                           Exp(UnaryMinus(self.right, self.has_var),
                               self.has_var)), Number(2), self.has_var),
                self.has_var)
        return Number(0)


class Cth:
    def __init__(self, right, has_var=False):
        self.right = right
        self.has_var = has_var

    def derivative(self):
        if self.has_var:
            return Divisor(
                Multiply(UnaryMinus(Number(4)), self.right.derivative()),
                Power(Minus(Exp(self.right, self.has_var),
                            Exp(UnaryMinus(self.right, self.has_var),
                                self.has_var)), Number(2), self.has_var),
                self.has_var)
        return Number(0)


symbol_class = {'+': Plus, '-': Minus, '*': Multiply, '/': Divisor, '^': Power,
                'um': UnaryMinus, 'sqrt': Sqrt, 'exp': Exp, 'ln': Ln, 'sh': Sh,
                'ch': Ch, 'th': Th, 'cth': Cth}
