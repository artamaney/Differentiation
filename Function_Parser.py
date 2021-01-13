from Constants import FUNCS
import Functions
from copy import deepcopy

try:
    from Differentiate import var
except ImportError:
    var = 'x'

funcs_dict = {'Multiply': '*', 'Plus': '+', 'Minus': '-',
              'Divisor': '/', 'Power': '^', 'UnaryMinus': 'um',
              'Sqrt': 'sqrt', 'Exp': 'exp', 'Ln': 'ln', 'Sh': 'sh', 'Ch': 'ch',
              'Th': 'th', 'Cth': 'cth', 'Number': 'var'}

binary_funcs = {'*', '-', '+', '^', '/'}
unary_funcs = set(FUNCS) | {'um'}


def parse_function(func):
    func = simplify_func(func)
    func = simplify_func(func)
    if is_unary_func(func):
        if isinstance(func, Functions.UnaryMinus):
            return f'(-{parse_function(func.right)})'
        return (f'{funcs_dict[type(func).__name__]}'
                f'({parse_function(func.right)})')
    elif is_binary_func(func):
        if is_binary_func(func.left) and is_binary_func(func.right):
            return (f'({parse_function(func.left)})'
                    f' {funcs_dict[type(func).__name__]}'
                    f' ({parse_function(func.right)})')
        elif is_binary_func(func.left):
            return (f'({parse_function(func.left)}) '
                    f'{funcs_dict[type(func).__name__]}'
                    f' {parse_function(func.right)}')
        elif is_binary_func(func.right):
            return (f'{parse_function(func.left)}'
                    f' {funcs_dict[type(func).__name__]}'
                    f' ({parse_function(func.right)})')
        else:
            if (isinstance(func, Functions.Multiply) and
                    isinstance(func.left, Functions.Number)):
                return (f'{parse_function(func.left)}'
                        f'{parse_function(func.right)}')
            return (f'{parse_function(func.left)}'
                    f' {funcs_dict[type(func).__name__]}'
                    f' {parse_function(func.right)}')
    else:
        if not (func.has_var or func.letter):
            if func.value < 0:
                return f'({func.value})'
        return f'{func.value}'


def is_binary_func(func):
    try:
        return funcs_dict[type(func).__name__] in binary_funcs
    except KeyError:
        return False


def is_unary_func(func):
    try:
        return funcs_dict[type(func).__name__] in unary_funcs
    except KeyError:
        return False


def simplify_mult(func):
    func.left = simplify_func(func.left)
    func.right = simplify_func(func.right)
    if isinstance(func.left, Functions.Number) and func.left.value == 0:
        return Functions.Number(0)
    if isinstance(func.right, Functions.Number) and func.right.value == 0:
        return Functions.Number(0)
    if isinstance(func.left, Functions.Number) and func.left.value == 1:
        return deepcopy(func.right)
    if isinstance(func.right, Functions.Number) and func.right.value == 1:
        return deepcopy(func.left)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and not
            func.left.has_var and not func.right.has_var):
        if not (func.left.letter or func.right.letter):
            return Functions.Number(func.left.value * func.right.value)
    if (func.left.has_var and func.right.has_var and
            (isinstance(func.left, Functions.Number) and
             isinstance(func.right, Functions.Number))):
        return Functions.Power(func.left, Functions.Number(2))
    if (isinstance(func.left, Functions.Number) and not
            (func.left.letter or func.left.has_var)):
        if (isinstance(func.right, Functions.Multiply) and
                isinstance(func.right.left, Functions.Number) and not
                (func.right.left.letter or func.right.left.has_var)):
            return Functions.Multiply(Functions.Number
                                      (func.left.value *
                                       func.right.left.value),
                                      func.right.right, func.right.has_var)
    if (isinstance(func.left, Functions.Number) and not
       (func.left.letter or func.left.has_var)):
        if (isinstance(func.right, Functions.Multiply) and
                (isinstance(func.right.right, Functions.Number) and not
                 (func.right.right.letter or func.right.right.has_var))):
            return Functions.Multiply(
                Functions.Number(func.left.value * func.right.right.value),
                func.right.left, func.right.has_var)
    if (isinstance(func.right, Functions.Number) and not (func.right.letter or
                                                          func.right.has_var)):
        if (isinstance(func.left, Functions.Multiply) and
                isinstance(func.left.left, Functions.Number) and not
                (func.left.left.letter or func.left.left.has_var)):
            return Functions.Multiply(
                Functions.Number(func.right.value * func.left.left.value),
                func.left.right, func.left.has_var)
    if (isinstance(func.left, Functions.Power) and
            isinstance(func.right, Functions.Power)):
        if func.left.left == func.right.left:
            return Functions.Power(
                func.left.left, Functions.Plus(func.right.right,
                                               func.left.right,
                                               func.right.right.has_var,
                                               func.left.right.has_var),
                func.left.has_var or func.right.has_var)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and func.left.has_var and
            func.right.has_var):
        return Functions.Power(func.left.value, Functions.Number(2), True)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Power) and
            func.left.has_var and func.right.left.has_var):
        return Functions.Power(
            func.left, Functions.Plus
            (Functions.Number(1), func.right.right, func.right.right.has_var),
            func.left.has_var or func.right.has_var)
    if (isinstance(func.left, Functions.Power) and
            isinstance(func.right, Functions.Number) and
            func.right.has_var and func.left.left.has_var):
        return Functions.Power(
            func.right, Functions.Plus
            (Functions.Number(1), func.left.right, func.left.right.has_var),
            func.right.has_var or func.left.has_var)
    if isinstance(func.left, Functions.Divisor):
        return Functions.Divisor(Functions.Multiply(deepcopy(func.left.left),
                                                    deepcopy(func.right),
                                                    func.has_var),
                                 deepcopy(func.left.right), func.has_var)
    if isinstance(func.right, Functions.Divisor):
        return Functions.Divisor(Functions.Multiply(deepcopy(func.right.left),
                                                    deepcopy(func.left),
                                                    func.has_var),
                                 deepcopy(func.right.right), func.has_var)
    if (isinstance(func.right, Functions.Power) and
            func.left.has_var and func.right.has_var and
            isinstance(func.left, Functions.Multiply)):
        value = func.left.left if func.left.left.has_var else func.left.right
        value2 = func.left.right if func.left.left.has_var else func.left.left
        return Functions.Multiply(value2,
                                  Functions.Multiply(func.right, value), True)
    if (isinstance(func.left, Functions.Plus) and
            isinstance(func.right, Functions.Number)):
        return Functions.Plus(Functions.Multiply
                              (func.left.left, func.right,
                               func.right.has_var or func.left.left.has_var),
                              Functions.Multiply(func.left.right, func.right,
                                                 func.left.right.has_var or
                                                 func.right.has_var))
    if (isinstance(func.right, Functions.Plus) and
            isinstance(func.left, Functions.Number)):
        return Functions.Plus(Functions.Multiply
                              (func.right.left, func.left,
                               func.left.has_var or func.right.left.has_var),
                              Functions.Multiply(func.right.right, func.left,
                                                 func.right.right.has_var or
                                                 func.left.has_var))
    if (isinstance(func.left, Functions.Minus) and
            isinstance(func.right, Functions.Number)):
        return Functions.Minus(Functions.Multiply
                               (func.left.left, func.right,
                                func.right.has_var or func.left.left.has_var),
                               Functions.Multiply(func.left.right, func.right,
                                                  func.left.right.has_var or
                                                  func.right.has_var))
    if (isinstance(func.right, Functions.Minus) and
            isinstance(func.left, Functions.Number)):
        return Functions.Minus(Functions.Multiply
                               (func.right.left, func.left,
                                func.left.has_var or func.right.left.has_var),
                               Functions.Multiply(func.right.right, func.left,
                                                  func.right.right.has_var or
                                                  func.left.has_var))
    if (isinstance(func.left, Functions.Multiply) and
            isinstance(func.right, Functions.Multiply) and
            func.left.has_var and func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        var2, val2 = find_var_and_val(func.right)
        if parse_function(var1) == parse_function(var2):
            return Functions.Multiply(Functions.Multiply(val1, val2),
                                      Functions.Power(var1, var2, True), True)
    if (isinstance(func.left, Functions.Multiply) and
            isinstance(func.right, Functions.Number) and
            func.left.has_var and func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        if parse_function(var1) == parse_function(func.right):
            return Functions.Multiply(val1,
                                      Functions.Power(var1,
                                                      Functions.Number(2),
                                                      True), True)
    if (isinstance(func.right, Functions.Multiply) and
            isinstance(func.left, Functions.Number) and
            func.right.has_var and func.left.has_var):
        var1, val1 = find_var_and_val(func.right)
        if parse_function(var1) == parse_function(func.left):
            return Functions.Multiply(val1, Functions.Power(
                var1, Functions.Number(2), True), True)
    return func


def simplify_plus(func):
    func.left = simplify_func(func.left)
    func.right = simplify_func(func.right)
    if isinstance(func.left, Functions.Number) and func.left.value == 0:
        return deepcopy(func.right)
    if isinstance(func.right, Functions.Number) and func.right.value == 0:
        return deepcopy(func.left)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and not
            func.left.has_var and not func.left.has_var):
        if not (func.left.letter or func.right.letter):
            return Functions.Number(func.left.value + func.right.value)
    if (isinstance(func.right, Functions.Multiply) and
            isinstance(func.right.left, Functions.Number) and
            func.right.left.value == -1):
        return Functions.Minus(func.left, func.right.right,
                               func.left.has_var or func.right.has_var)
    if (isinstance(func.right, Functions.Multiply) and
            isinstance(func.right.right, Functions.Number) and
            func.right.right.value == -1):
        return Functions.Minus(func.left, func.right.left)
    if (isinstance(func.right, Functions.Number) and
            isinstance(func.left, Functions.Number) and
            func.left.has_var and func.right.has_var):
        return Functions.Multiply(Functions.Number(2.0), func.left,
                                  func.left.has_var)
    if (isinstance(func.left, Functions.Multiply) and
            isinstance(func.right, Functions.Multiply) and
            func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        var2, val2 = find_var_and_val(func.right)
        if parse_function(var1) == parse_function(var2):
            return Functions.Multiply(
                simplify_plus(Functions.Plus(val1, val2,
                                             val1.has_var or val2.has_var)),
                var1, True)
    if (isinstance(func.left, Functions.Multiply) and func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        if parse_function(func.right) == parse_function(var1):
            return Functions.Multiply(
                Functions.Plus(val1, Functions.Number(1)), var1, True)
    if (isinstance(func.right, Functions.Multiply) and func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.right)
        if parse_function(func.left) == parse_function(var1):
            return Functions.Multiply(
                Functions.Plus(val1, Functions.Number(1)), var1, True)
    return func


def simplify_minus(func):
    func.left = simplify_func(func.left)
    func.right = simplify_func(func.right)
    if isinstance(func.left, Functions.Number) and func.left.value == 0:
        return Functions.UnaryMinus(func.right, func.right.has_var)
    if isinstance(func.right, Functions.Number) and func.right.value == 0:
        return deepcopy(func.left)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and not
            func.left.has_var and not func.right.has_var):
        if not (func.left.letter or func.right.letter):
            return Functions.Number(func.left.value - func.right.value)
    if (isinstance(func.right, Functions.Multiply) and
            isinstance(func.right.left, Functions.Number) and
            func.right.left.value == -1):
        return Functions.Plus(func.left, func.right.right)
    if (isinstance(func.right, Functions.Multiply) and
            isinstance(func.right.right, Functions.Number) and
            func.right.right.value == -1):
        return Functions.Plus(func.left, func.right.left)
    if (isinstance(func.left, Functions.Multiply) and
            isinstance(func.right, Functions.Multiply) and
            func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        var2, val2 = find_var_and_val(func.right)
        if parse_function(var1) == parse_function(var2):
            return Functions.Multiply(
                simplify_func(Functions.Minus(val1, val2)), var1, True)
    if (isinstance(func.left, Functions.Multiply) and func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.left)
        if parse_function(func.right) == parse_function(var1):
            return Functions.Multiply(
                Functions.Minus(val1, Functions.Number(1)), var1, True)
    if (isinstance(func.right, Functions.Multiply) and func.left.has_var and
            func.right.has_var):
        var1, val1 = find_var_and_val(func.right)
        if parse_function(func.left) == parse_function(var1):
            return Functions.Multiply(
                Functions.Minus(val1, Functions.Number(1)), var1, True)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and
            func.left.has_var and func.right.has_var):
        return Functions.Number(0)
    return func


def simplify_power(func):
    func.left = simplify_func(func.left)
    func.right = simplify_func(func.right)
    if isinstance(func.right, Functions.Number) and func.right.value == 0:
        return Functions.Number(1)
    if isinstance(func.right, Functions.Number) and func.right.value == 1:
        return deepcopy(func.left)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and not
            func.left.has_var and not func.right.has_var):
        if not (func.left.letter or func.right.letter):
            return Functions.Number(func.left.value ** func.right.value)
    if (isinstance(func.left, Functions.Power) and
            isinstance(func.right, Functions.Number)):
        return Functions.Power(func.left.left,
                               Functions.Multiply(func.left.right, func.right),
                               func.right.has_var or func.left.has_var)
    return func


def simplify_dividing(func):
    func.left = simplify_func(func.left)
    func.right = simplify_func(func.right)
    if isinstance(func.left, Functions.Number) and func.left.value == 0:
        return Functions.Number(0)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and not
            func.left.has_var and not func.right.has_var):
        if not (func.left.letter or func.right.letter):
            return Functions.Number(func.left.value / func.right.value)
    if (isinstance(func.left, Functions.Number) and
            isinstance(func.right, Functions.Number) and
            func.left.has_var and func.right.has_var):
        return Functions.Number(1)
    if isinstance(func.right, Functions.Number) and func.right.value == 1:
        return deepcopy(func.left)
    if (isinstance(func.left, Functions.Multiply) and
            isinstance(func.right, Functions.Power) and
            func.left.has_var and func.right.has_var):
        var, val = find_var_and_val(func.left)
        if (isinstance(var, Functions.Power) and
                parse_function(var.left) == parse_function(func.right.left)):
            return Functions.Multiply(
                val, Functions.Power(var.left,
                                     Functions.Minus(var.right,
                                                     func.right.right)))
        if parse_function(var) == parse_function(func.right.left):
            if isinstance(var, Functions.Number):
                return Functions.Multiply(
                    val, Functions.Power(var,
                                         Functions.Minus(Functions.Number(1),
                                                         func.right.right)))
    return func


def simplify_um(func):
    if (not (func.right.has_var or func.right.letter) and
            isinstance(func.right, Functions.Number)):
        return Functions.Number(-func.right.value)
    if isinstance(func.right, Functions.Multiply):
        if (isinstance(func.right.left, Functions.Number) and not
           (func.right.left.has_var or func.right.left.letter)):
            return Functions.Multiply(Functions.Number(-func.right.left.value),
                                      func.right.right)

    return func


def find_var_and_val(func):
    if func.left.has_var:
        var_ = func.left
        val = func.right
    else:
        var_ = func.right
        val = func.left
    return var_, val


def simplify_func(func):
    if isinstance(func, Functions.UnaryMinus):
        return simplify_um(func)
    if isinstance(func, Functions.Multiply):
        return simplify_mult(func)
    if isinstance(func, Functions.Plus):
        return simplify_plus(func)
    if isinstance(func, Functions.Minus):
        return simplify_minus(func)
    if isinstance(func, Functions.Power):
        return simplify_power(func)
    if isinstance(func, Functions.Divisor):
        return simplify_dividing(func)
    return func
