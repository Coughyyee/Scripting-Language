import sys

from frontend.syntax_tree import *
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
        if prev is None or prev.type != type:
            print(
                f"Parser Error:\n  {err}\n  {prev} -> Expecting: {type}",
                file=sys.stderr,
            )
            exit(1)

        return prev

    def produce_ast(self, sourceCode: str) -> Program:
        self._tokens = tokenize(sourceCode)
        program = Program([])

        # Parse until EOF.
        while self.not_eof():
            program.body.append(self.parse_stmt())

        return program

    def parse_stmt(self) -> Stmt:
        match self.at().type:
            case TokenType.LET:
                return self.parse_var_declaration()
            case TokenType.CONST:
                return self.parse_var_declaration()
            case _:
                return self.parse_expr()

    # ( LET ) IDENT;
    # ( CONST | LET ) IDENT = EXPR;
    def parse_var_declaration(
        self,
    ) -> Stmt:
        is_constant = self.eat().type == TokenType.CONST
        identifier = self.expect(
            TokenType.IDENTIFIER,
            "Expected identifier name following <let | const> keyword.",
        ).value

        if self.at().type == TokenType.SEMICOLON:
            self.eat()  # expect semicolon.
            if is_constant:
                raise ValueError(
                    "Must assign value to constant expression. No value provided."
                )

            return VarDeclaration(False, identifier)

        self.expect(
            TokenType.EQUALS,
            "Expected equals token following identifier in var declaration.",
        )

        declaration = VarDeclaration(is_constant, identifier, self.parse_expr())

        self.expect(
            TokenType.SEMICOLON,
            "Variable declaration statement must end with a semicolon.",
        )

        return declaration

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
