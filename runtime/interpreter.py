import sys
from runtime.values import *
from frontend.syntax_tree import *
from runtime.environment import *


def eval_program(program: Program, env: Environment) -> RuntimeVal:
    lastEvaluated = MK_NULL()

    for statement in program.body:
        lastEvaluated = evaluate(statement, env)

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

    return MK_NUMBER(result)


def eval_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    leftHandSide = evaluate(binop.left, env)
    rightHandSide = evaluate(binop.right, env)

    if leftHandSide.type == "number" and rightHandSide.type == "number":
        return eval_numeric_binary_expr(leftHandSide, rightHandSide, binop.operator)

    # One or both are NULL
    return MK_NULL()


def eval_identifier(ident: Identifier, env: Environment) -> RuntimeVal:
    val = env.lookup_var(ident.symbol)
    return val


def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    match astNode.kind:
        case "NumericLiteral":
            if isinstance(astNode, NumericLiteral):
                return NumberVal(astNode.value)
        case "Identifier":
            return eval_identifier(astNode, env)
        case "BinaryExpr":
            return eval_binary_expr(astNode, env)
        case "Program":
            return eval_program(astNode, env)
        case _:
            print(
                f"This AST Node has not yet been setup for interpretation.\n{astNode}",
                file=sys.stderr,
            )
            exit(1)
