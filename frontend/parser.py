import sys

from frontend.syntax_tree import (
    Stmt,
    Program,
    Expr,
    BinaryExpr,
    NumericLiteral,
    Identifier,
    NullLiteral
)
from frontend.lexer import tokenize, Token, TokenType


class Parser:
    def __init__(self):
        self._tokens: list[Token] = []

    def not_eof(self) -> bool:
        return self._tokens[0].type != TokenType.EOF

    def at(self) -> Token:
        return self._tokens[0]

    def eat(self) -> Token:
        prev = self._tokens.pop(0)
        return prev

    def expect(self, type: TokenType, err):
        prev = self._tokens.pop(0)
        if not prev or prev.type is not type:
            print(
                f"Parser Error:\n{err}{prev}Expecting: {type}",
                file=sys.stderr,
            )
            exit(1)

        return prev

    def produceAST(self, sourceCode: str) -> Program:
        self._tokens = tokenize(sourceCode)
        program = Program([])

        # Parse until EOF.
        while self.not_eof():
            program.body.append(self.parse_stmt())

        return program

    def parse_stmt(self) -> Stmt:
        # Skip to parse_expr
        return self.parse_expr()

    def parse_expr(self) -> Expr:
        return self.parse_additive_expr()

    """
    Orders of Prescidence:
        AssignmentExpr
        MemberExpr
        FunctionCall
        LogicalExpr
        ComparisonExpr
        AdditiveExpr
        MultiplicitaveExpr
        UnaryExpr
        PrimaryExpr
    """

    # 10 + 5 - 5 -> ((10 + 5) - 5)
    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicitave_expr()

        while self.at().value == "+" or self.at().value == "-":
            operator = self.eat().value
            right = self.parse_multiplicitave_expr()
            left = BinaryExpr(left, right, operator)

        return left

    # 10-5*10 -> (10 - (5 * 10)) | Order of operation - BIDMAS/BODMAS
    def parse_multiplicitave_expr(self) -> Expr:
        left = self.parse_primary_expr()

        while (
            self.at().value == "/" or self.at().value == "*" or self.at().value == "%"
        ):
            operator = self.eat().value
            right = self.parse_primary_expr()
            left = BinaryExpr(left, right, operator)

        return left

    def parse_primary_expr(self) -> Expr:
        tk = self.at().type

        match tk:
            case TokenType.IDENTIFIER:
                return Identifier(self.eat().value)
            case TokenType.NULL:
                self.eat() # advance past null keyword
                return NullLiteral()
            case TokenType.NUMBER:
                return NumericLiteral(float(self.eat().value))
            case TokenType.OPENPAREN:
                self.eat()  # eat opening paren
                value = self.parse_expr()
                self.expect(
                    TokenType.CLOSEPAREN,
                    "Unexpected token found inside parenthesised expression. Expected closing parenthesis.",
                )  # eat closing paren
                return value
            case _:
                print(
                    f"Unexpected token found during parsing! {self.at()}",
                    file=sys.stderr,
                )
                exit(1)
