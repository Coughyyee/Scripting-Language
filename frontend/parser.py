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

    """ Parsing """

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

    """
    Orders of Prescidence:
        AssignmentExpr (x = y, x += y, x -= y)
        LogicalExpr (x && y, x || y)
        ComparisonExpr (x == y, x != y, x < y, x > y)
        AdditiveExpr (x + y, x - y)
        MultiplicativeExpr (x * y, x / y, x % y)
        UnaryExpr (-x, !x, ~x)
        MemberExpr (object.property, array[index])
        FunctionCall (function(arg1, arg2), obj.method())
        PrimaryExpr (123, x, (x + y))
    """

    def parse_expr(self) -> Expr:
        return self.parse_assignment_expr()  # Lowest order of prescidence

    # let x = 10; x = 20;
    def parse_assignment_expr(self) -> Expr:
        left = self.parse_object_expr()

        if self.at().type == TokenType.EQUALS:
            self.eat()  # advance past equals
            value = (
                self.parse_assignment_expr()
            )  # | x = foo = bar <- assignment chaining
            if self.at().type == TokenType.SEMICOLON:
                self.eat()  # eats semi colon if there is one
            return AssignmentExpr(left, value)

        return left

    # { Prop[] }
    def parse_object_expr(self) -> Expr:
        if self.at().type != TokenType.OPENBRACE:
            return self.parse_additive_expr()

        self.eat()  # advances past the open brace.
        properties = []

        while self.not_eof() and self.at().type != TokenType.CLOSEBRACE:
            # { key: val, key2: val2 } <,> optional

            key = self.expect(
                TokenType.IDENTIFIER, "Object literal key expected."
            ).value

            # Allows shorthand key: pair -> { key, }
            if self.at().type == TokenType.COMMA:
                self.eat()  # advance past the comma
                properties.append(PropertyLiteral(key, None))
                continue
            # Allows shorthand key: pair -> { key }
            elif self.at().type == TokenType.CLOSEBRACE:
                properties.append(PropertyLiteral(key, None))
                continue

            # { key: val }
            self.expect(
                TokenType.COLON, "Missing colon following identifier in ObjectExpr."
            )
            value = self.parse_expr()  # let any kind of value be on the RHS.

            properties.append(PropertyLiteral(key, value))
            if self.at().type != TokenType.CLOSEBRACE:
                self.expect(
                    TokenType.COMMA,
                    "Expected comma or closing brace following propery.",
                )

        self.expect(TokenType.CLOSEBRACE, "Object literal missing closing brace.")
        return ObjectLiteral(properties)

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
        left = self.parse_call_member_expr()

        while (
            self.at().value == "/" or self.at().value == "*" or self.at().value == "%"
        ):
            operator = self.eat().value
            right = self.parse_call_member_expr()
            left = BinaryExpr(left, right, operator)

        return left

    # foo.x()
    def parse_call_member_expr(self) -> Expr:
        member = self.parse_member_expr()

        if self.at().type == TokenType.OPENPAREN:
            return self.parse_call_expr(member)

        return member

    def parse_call_expr(self, caller: Expr) -> Expr:
        call_expr = CallExpr(self.parse_args(), caller)

        # foo.x()() - if foo.x() returns a func
        if self.at().type == TokenType.OPENPAREN:
            call_expr = self.parse_call_expr(call_expr)

        return call_expr

    # fn add(x, y) <- x,y are parameters, theyre variables.
    # add(10, foo()) <- these are arguments, we are calling add() - args are just expressions.
    def parse_args(self) -> list[Expr]:
        self.expect(TokenType.OPENPAREN, "Expected open parenthesis")
        args = (
            []
            if self.at().type == TokenType.CLOSEPAREN
            else self.parse_arguments_list()
        )

        self.expect(
            TokenType.CLOSEPAREN, "Missing closing parenthesis inside arguments list"
        )
        return args

    # foo(x = 5, v = "Bar")
    def parse_arguments_list(self) -> list[Expr]:
        args = [self.parse_assignment_expr()]

        while self.at().type == TokenType.COMMA and self.eat():  # ? self.eat() is None?
            args.append(self.parse_assignment_expr())

        return args

    def parse_member_expr(self) -> Expr:
        obj = self.parse_primary_expr()

        while (
            self.at().type == TokenType.DOT or self.at().type == TokenType.OPENBRACKET
        ):
            operator = self.eat()
            prop: Expr
            computed: bool

            # non-computed values aka obj.expr
            if operator.type == TokenType.DOT:
                computed = False
                prop = self.parse_primary_expr()  # get identifier

                if prop.kind != "Identifier":
                    raise ValueError(
                        f"Cannot use dot operator without right hand side being an identifier"
                    )
            else:  # allows obj[computed_value]
                computed = True
                prop = self.parse_expr()
                self.expect(
                    TokenType.CLOSEBRACKET, "Missing closing bracket in computed value."
                )

            obj = MemberExpr(obj, prop, computed)

        return obj

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
