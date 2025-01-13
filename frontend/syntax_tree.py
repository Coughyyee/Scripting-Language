from typing import Literal

NodeType = Literal[
    # Statements
    "Program",
    "VarDeclaration",
    # Expressions
    "AssignmentExpr",
    "BinaryExpr",
    # Literals
    "PropertyLiteral",
    "ObjectLiteral",
    "NumericLiteral",
    "Identifier",
]


class Stmt:
    def __init__(self, kind: NodeType):
        self.kind = kind

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.kind}"


class Expr(Stmt):
    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.kind}"


"""Statements"""


class Program(Stmt):
    def __init__(self, body: list[Stmt]):
        super().__init__("Program")
        self.body = body

    def __str__(self, level=0):
        indent = "  " * level
        body_str = "\n".join(stmt.__str__(level + 1) for stmt in self.body)
        return f"{indent}{self.__class__.__name__}:\n{body_str}"


class VarDeclaration(Stmt):
    def __init__(self, constant: bool, identifier: str, value: Expr = None):
        super().__init__("VarDeclaration")
        self.constant = constant
        self.identifier = identifier
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        value_str = (
            self.value.__str__(level + 2)
            if self.value
            else f"{"  " * (level + 2)}<undefined>"  #! Change this to null or something?
        )
        return (
            f"{indent}{self.__class__.__name__}:\n"
            f"{indent}  Constant: {self.constant}\n"
            f"{indent}  Identifier: {self.identifier}\n"
            f"{indent}  Value:\n"
            f"{indent}{value_str}\n"
        )


"""Expressions"""


class AssignmentExpr(Expr):
    def __init__(self, assigne: Expr, value: Expr):
        super().__init__("AssignmentExpr")
        self.assigne = assigne
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        assigne_str = self.assigne.__str__(level + 2)
        value_str = self.value.__str__(level + 2)
        return (
            f"{indent}{self.__class__.__name__}:\n"
            f"{indent}  Assigne:\n{assigne_str}\n"
            f"{indent}  Value:\n{value_str}"
        )


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
            f"{indent}{self.__class__.__name__}:\n"
            f"{indent}  Operator: {self.operator}\n"
            f"{indent}  Left:\n{left_str}\n"
            f"{indent}  Right:\n{right_str}"
        )


class PropertyLiteral(Expr):
    def __init__(self, key: str, value: Expr = None):
        super().__init__("PropertyLiteral")
        self.key = key
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        value_str = (
            self.value.__str__(level + 2)
            if self.value
            else f"{"  " * (level + 2)}<undefined>"  #! Change this to null or something?
        )
        return (
            f"{indent}{self.__class__.__name__}:\n"
            f"{indent}  Key: '{self.key}'\n"
            f"{indent}  Value:\n{value_str}"
        )


class ObjectLiteral(Expr):
    def __init__(self, properties: list[PropertyLiteral]):
        super().__init__("ObjectLiteral")
        self.properties = properties

    def __str__(self, level=0):
        indent = "  " * level
        prop_str = "\n".join(prop.__str__(level + 1) for prop in self.properties)
        return f"{indent}{self.__class__.__name__}:\n{prop_str}"


class NumericLiteral(Expr):
    def __init__(self, value: float):
        super().__init__("NumericLiteral")
        self.value = value

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}(value={self.value})"


class Identifier(Expr):
    def __init__(self, symbol: str):
        super().__init__("Identifier")
        self.symbol = symbol

    def __str__(self, level=0):
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}(symbol={self.symbol})"
