from typing import Literal

NodeType = Literal["Program", "NumericLiteral", "Identifier", "BinaryExpr"]


class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.kind}"


class Program(Stmt):
    def __init__(self, body: list[Stmt]):
        super().__init__("Program")
        self.body = body

    def __str__(self, level=0):
        indent = "  " * level
        body_str = "\n".join(stmt.__str__(level + 1) for stmt in self.body)
        return f"{indent}Program:\n{body_str}"


class Expr(Stmt):
    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.kind}"


class BinaryExpr(Expr):
    def __init__(self, left: Expr, right: Expr, operator: str):
        super().__init__("BinaryExpr")
        self.left = left
        self.right = right
        self.operator = operator

    def __str__(self, level=0):
        indent = "  " * level
        left_str = self.left.__str__(level + 2)
        right_str = self.right.__str__(level + 2)
        return (
            f"{indent}BinaryExpr:\n"
            f"{indent}  Operator: {self.operator}\n"
            f"{indent}  Left:\n{left_str}\n"
            f"{indent}  Right:\n{right_str}"
        )


class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__("NumericLiteral")
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}NumericLiteral(value={self.value})"


class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__("Identifier")
        self.symbol = symbol

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}Identifier(symbol={self.symbol})"