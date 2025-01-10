from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    EQUALS = auto()
    OPENPAREN = auto()
    CLOSEPAREN = auto()
    BINARYOPERATOR = auto()
    LET = auto()


KEYWORDS = {
    "let": TokenType.LET,
}


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return f"< value: {self.value}, type: {self.type} >"


def tokenize(sourceCode: str) -> list[Token]:
    tokens = []
    src = list(sourceCode)

    while len(src) > 0:
        if src[0] == "(":
            tokens.append(Token(src.pop(0), TokenType.OPENPAREN))
        elif src[0] == ")":
            tokens.append(Token(src.pop(0), TokenType.CLOSEPAREN))
        elif src[0] == "+" or src[0] == "-" or src[0] == "*" or src[0] == "/":
            tokens.append(Token(src.pop(0), TokenType.BINARYOPERATOR))
        elif src[0] == "=":
            tokens.append(Token(src.pop(0), TokenType.EQUALS))
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
                if reserved:
                    tokens.append(Token(ident, reserved))
                else:
                    tokens.append(Token(ident, TokenType.IDENTIFIER))
            elif src[0].isspace():
                src.pop(0)
            else:
                print("Unrecognised Character found in src: ", src[0])
                exit(1)

    return tokens


with open("./test.txt", "r") as file:
    source = file.read()
    for token in tokenize(source):
        print(token)
