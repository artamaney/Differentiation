NUMBERS = '1234567890.'
DOT = '.'
ST_BRACKET = '('
END_BRACKET = ')'
PLUS = '+'
MINUS = '-'
MULTIPLY = '*'
DIVIDE = '/'
POWER = '^'
UNARY_MINUS = 'um'
FUNCS = ['sqrt', 'exp', 'ln', 'sh', 'ch', 'th', 'cth']
PRIORITIES = {POWER: 10, MULTIPLY: 8, DIVIDE: 8, PLUS: 4, MINUS: 4,
              ST_BRACKET: 3, END_BRACKET: 3, 'sqrt': 20, 'exp': 20, 'ln': 20,
              'sh': 20, 'ch': 20, 'th': 20, 'cth': 20, UNARY_MINUS: 19}
OPERATIONS = [PLUS, MINUS, MULTIPLY, DIVIDE, POWER]
LETTERS = ([chr(i) for i in range(ord('a'), ord('z') + 1)] +
           [chr(i) for i in range(ord('A'), ord('Z') + 1)])
