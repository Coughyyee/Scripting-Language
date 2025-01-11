import sys
from runtime.values import *
from frontend.syntax_tree import *


def eval_program(program: Program) -> RuntimeVal:
    lastEvaluated = NullVal()

    for statement in program.body:
        lastEvaluated = evaluate(statement)

    return lastEvaluated


def eval_numeric_binary_expr(
    leftHandSide: NumberVal, rightHandSide: NumberVal, operator: str
) -> NumberVal:
    result: float = 0
    if operator == "+":
        result = leftHandSide.value + rightHandSide.value
    elif operator == "-":
        result = leftHandSide.value - rightHandSide.value
    elif operator == "*":
        result = leftHandSide.value * rightHandSide.value
    elif operator == "/":
        # TODO: Division by zero checks
        result = leftHandSide.value / rightHandSide.value
    elif operator == "%":
        result = leftHandSide.value % rightHandSide.value

    return NumberVal(result)


def eval_binary_expr(binop: BinaryExpr) -> RuntimeVal:
    leftHandSide = evaluate(binop.left)
    rightHandSide = evaluate(binop.right)

    if leftHandSide.type == "number" and rightHandSide.type == "number":
        return eval_numeric_binary_expr(leftHandSide, rightHandSide, binop.operator)

    # One or both are NULL
    return NullVal()


def evaluate(astNode: Stmt) -> RuntimeVal:
    match astNode.kind:
        case "NumericLiteral":
            if isinstance(astNode, NumericLiteral):
                return NumberVal(astNode.value)
        case "NullLiteral":
            return NullVal()
        case "BinaryExpr":
            return eval_binary_expr(astNode)  # ?
        case "Program":
            return eval_program(astNode)  # ?
        case _:
            print(
                f"This AST Node has not yet been setup for interpretation.\n{astNode}",
                file=sys.stderr,
            )
            exit(1)
