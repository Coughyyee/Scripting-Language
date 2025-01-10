from typing import Literal

NodeType = Literal["Program", "NumericLiteral", "Identifier", "BinaryExpr"]


"""
Expressions return a value. e.g -> let x = if true {10} else {0}
Statements do not return a value. e.g -> let x = 10
"""


class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind


class Program(Stmt):
    def __init__(self, body: list[Stmt]):
        super().__init__("Program")
        self.body = body


class Expr(Stmt):
    pass


"""
Binary Expression e.g -> 10 - 5
                         L O R
"""


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str):
        super().__init__("BinaryExpr")
        self.left = left
        self.right = right
        self.operator = operator


class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__("Identifier")
        self.symbol = symbol


class NumericLiteral(Expr):
    def __init__(self, value: float):  # ? float type
        super().__init__("NumericLiteral")
        self.value = value
