import sys
from rich import print
from frontend.syntax_tree import NumericLiteral, Stmt
from runtime.environment import Environment
from runtime.eval.expressions import (
    eval_assignment,
    eval_binary_expr,
    eval_identifier,
    eval_object_expr,
)
from runtime.eval.statements import eval_program, eval_var_declaration
from runtime.values import NumberVal, RuntimeVal


def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    match astNode.kind:
        case "NumericLiteral":
            if isinstance(astNode, NumericLiteral):
                return NumberVal(astNode.value)
        case "Identifier":
            return eval_identifier(astNode, env)
        case "ObjectLiteral":
            return eval_object_expr(astNode, env)
        case "AssignmentExpr":
            return eval_assignment(astNode, env)
        case "BinaryExpr":
            return eval_binary_expr(astNode, env)
        case "Program":
            return eval_program(astNode, env)
        case "VarDeclaration":  # Handle statements
            return eval_var_declaration(astNode, env)
        case _:
            print(
                (
                    f"[bold red]This AST Node has not yet been setup for interpretation.[/bold red]\n"
                    f"{astNode}"
                ),
                file=sys.stderr,
            )
            exit(1)
