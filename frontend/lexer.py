from enum import Enum, auto
from util.printer import value_print


# Language Token Types
class TokenType(Enum):

    # Literal Types
    NUMBER = auto()
    IDENTIFIER = auto()

    # Keywords
    LET = auto()
    CONST = auto()

    # Grouping * Operators
    BINARYOPERATOR = auto()
    EQUALS = auto()
    SEMICOLON = auto()
    OPENPAREN = auto()
    CLOSEPAREN = auto()
    EOF = auto()  # Signifies the end of file


# Language Keywords
KEYWORDS = {
    "let": TokenType.LET,
    "const": TokenType.CONST,
}


class Token:
    def __init__(self, value, type: TokenType):
        self.value = value
        self.type = type

    def __str__(self):
        return value_print(self.__class__.__name__, self.value, self.type)


def tokenize(sourceCode: str) -> list[Token]:
    tokens = []
    src = list(sourceCode)

    while len(src) > 0:
        if src[0] == "(":
            tokens.append(Token(src.pop(0), TokenType.OPENPAREN))
        elif src[0] == ")":
            tokens.append(Token(src.pop(0), TokenType.CLOSEPAREN))
        elif (
            src[0] == "+"
            or src[0] == "-"
            or src[0] == "*"
            or src[0] == "/"
            or src[0] == "%"
        ):
            tokens.append(Token(src.pop(0), TokenType.BINARYOPERATOR))
        elif src[0] == "=":
            tokens.append(Token(src.pop(0), TokenType.EQUALS))
        elif src[0] == ";":
            tokens.append(Token(src.pop(0), TokenType.SEMICOLON))
        else:
            # Multi-Character Tokens

            # Build number token
            if src[0].isnumeric():
                num = ""
                while len(src) > 0 and src[0].isnumeric():
                    num += src.pop(0)

                tokens.append(Token(num, TokenType.NUMBER))
            elif src[0].isalpha():
                ident = ""
                while len(src) > 0 and src[0].isalpha():
                    ident += src.pop(0)

                # Check for reserved keywords
                reserved = KEYWORDS.get(ident, None)
                if reserved:  # ? Youtube -> typeof reserved == "number"
                    tokens.append(Token(ident, reserved))
                else:
                    tokens.append(Token(ident, TokenType.IDENTIFIER))
            elif src[0].isspace():
                src.pop(0)
            else:
                print("Unrecognised Character found in src: ", src[0])
                exit(1)

    tokens.append(Token("EOF", TokenType.EOF))
    return tokens


"""
Read File Content
"""
# with open("./test.txt", "r") as file:
#     source = file.read()
#     for token in tokenize(source):
#         print(token)
