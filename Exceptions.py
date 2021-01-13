class ParseAndDiffExceptions(Exception):
    EXCEPTION_NAME = ''

    def __init__(self, statement, index):
        super().__init__(
            f'{self.EXCEPTION_NAME}:\n{statement}\n{index * " "}^')


class TooManyDotsException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "There is more than one dot in number"


class NumberStartsWithDotException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "Your word should not starts with dot"


class UndefinedSymbolException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "I don`t know what this symbol means"


class IncorrectBracketsException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "You have got an extra bracket"


class TooManyOperatorsAtTimeException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "There are more than one operator at time"


class NotEnoughArgumentsException(ParseAndDiffExceptions):
    EXCEPTION_NAME = "There are not enough arguments in statement"
