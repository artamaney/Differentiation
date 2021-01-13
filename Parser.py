from Constants import (NUMBERS, DOT, ST_BRACKET, END_BRACKET, LETTERS,
                       OPERATIONS, FUNCS, PRIORITIES, UNARY_MINUS)
from Exceptions import (UndefinedSymbolException, IncorrectBracketsException,
                        NumberStartsWithDotException,
                        TooManyOperatorsAtTimeException, TooManyDotsException,
                        NotEnoughArgumentsException)
import Functions
from Function_Parser import unary_funcs, binary_funcs


def parse_statement(statement):
    number = ''
    statement = statement.replace(' ', '')
    is_prev_op = False
    n = len(statement)
    dots = []
    operations = []
    res = []
    i = 0
    known_symbols = (set(NUMBERS) | set(LETTERS) | set(OPERATIONS) |
                     {ST_BRACKET, END_BRACKET})
    is_prev_end_br = False
    is_prev_letter = False
    is_prev_op_for_func = False
    while i != n:
        flag = False
        if statement[i] not in known_symbols:
            raise UndefinedSymbolException(statement, i)
        elif statement[i] == ST_BRACKET:
            if need_in_multiply(statement, statement[i], i, is_prev_op):
                add_operation(operations, res, ('*', i))
            is_prev_op = False
            operations += [(ST_BRACKET, i)]
            i += 1
            is_prev_end_br = False
            is_prev_letter = False
        elif statement[i] == END_BRACKET:
            while operations and operations[-1][0] != ST_BRACKET:
                res += [operations.pop()]
            if not operations:
                raise IncorrectBracketsException(statement, i)
            operations.pop()
            is_prev_letter = False
            is_prev_op = False
            is_prev_end_br = True
            i += 1
        else:
            func_or_var = get_function(statement, i)
            if func_or_var is None:
                was_number = False
                if statement[i] in NUMBERS:
                    was_number = True
                while was_number:
                    if i != n and statement[i] in NUMBERS:
                        number = f'{number}{statement[i]}'
                        if statement[i] is DOT:
                            dots += [i]
                        if statement[i] is DOT and len(number) == 1:
                            raise NumberStartsWithDotException(statement, i)
                        if len(dots) >= 2:
                            raise TooManyDotsException(statement, i)
                        i += 1
                    elif len(number) != 0:
                        res += [(float(number), i - len(number))]
                        number = ''
                        was_number = False
                        is_prev_op = False
                        is_prev_op_for_func = True
                        if is_prev_letter or is_prev_end_br:
                            add_operation(operations, res, ('*', i))
                            is_prev_letter = False
                            is_prev_end_br = False
                        flag = True
                if flag:
                    continue
                if i != n and statement[i] in LETTERS:
                    if need_in_multiply(statement, statement[i],
                                        i,  is_prev_op):
                        add_operation(operations, res, ('*', i))
                        is_prev_end_br = False
                    is_prev_letter = True
                    is_prev_op_for_func = True
                    res += [(statement[i], i)]
                    i += 1
                is_prev_op = False
                if is_prev_end_br:
                    operations.append(('*', i))
                is_prev_end_br = False
            else:
                if is_prev_op and func_or_var not in FUNCS:
                    raise TooManyOperatorsAtTimeException(statement, i)
                if is_prev_op_for_func and func_or_var in FUNCS:
                    add_operation(operations, res, ('*', i))
                if func_or_var in OPERATIONS:
                    is_prev_op_for_func = False
                else:
                    is_prev_op_for_func = True
                add_operation(operations, res, (func_or_var, i))
                i += len(func_or_var)
                if func_or_var == UNARY_MINUS:
                    i -= 1
                is_prev_letter = False
                is_prev_op = True
                is_prev_end_br = False
    res += operations[::-1]
    for op in res:
        if op[0] == ST_BRACKET:
            raise IncorrectBracketsException(statement, op[1])
    check_NotEnoughArgumentsException(statement, res)
    return [r[0] for r in res]


def get_function(statement, start_index):
    if statement[start_index] in OPERATIONS:
        if (start_index == 0 or statement[start_index - 1] == '(' and
                statement[start_index] == '-'):
            return UNARY_MINUS
        return statement[start_index]
    end = start_index
    while end != len(statement) - 1 and statement[end] in LETTERS:
        end += 1
    func = statement[start_index:end]
    if func in FUNCS:
        return func
    return None


def add_operation(operations, res, operation):
    priority = PRIORITIES[operation[0]]
    while len(operations):
        prev = operations.pop()
        prev_pr = PRIORITIES[prev[0]]
        if prev_pr < priority or prev[0] == operation[0] == '^':
            operations += [prev]
            break
        res += [prev]
    operations += [operation]


def need_in_multiply(statement, operation, i, is_prev_op):
    return ((operation in FUNCS or operation in
             [ST_BRACKET, END_BRACKET] + LETTERS) and not
            (i == 0 or is_prev_op or statement[i - 1] == ST_BRACKET))


def check_NotEnoughArgumentsException(statement, operations):
    ops = []
    if not operations:
        raise NotEnoughArgumentsException(statement, 0)
    for op, ind in operations:
        if op not in set(OPERATIONS) | set(FUNCS) and op != UNARY_MINUS:
            ops.append(op)
            continue
        if (op is UNARY_MINUS or op in FUNCS) and not ops:
            raise NotEnoughArgumentsException(statement, ind + 1)
        if op in OPERATIONS and len(ops) < 2:
            raise NotEnoughArgumentsException(statement, ind + 1)
        if op in OPERATIONS:
            ops.pop()


def differentiate(variable, expression):
    parsed_expr = parse_statement(expression)
    if variable not in set(parsed_expr):
        return Functions.Number(0)
    func_stack = []
    n = len(parsed_expr)
    symbol_classes = Functions.symbol_class
    for i in range(n):
        current = parsed_expr[i]
        if current in unary_funcs:
            right = func_stack.pop()
            func_stack.append(symbol_classes[current](right, right.has_var))
        elif current in binary_funcs:
            right = func_stack.pop()
            left = func_stack.pop()
            func_stack.append(symbol_classes[current](
                left, right, left.has_var or right.has_var))
        else:
            has_var = current == variable
            func_stack.append(Functions.Number(current, has_var,
                                               current in LETTERS and
                                               not has_var))
    return func_stack.pop()
