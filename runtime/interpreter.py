import sys
from frontend.syntax_tree import NumericLiteral, Stmt
from runtime.environment import Environment
from runtime.eval.expressions import eval_binary_expr, eval_identifier
from runtime.eval.statements import eval_program, eval_var_declaration
from runtime.values import NumberVal, RuntimeVal


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
        case "VarDeclaration":  # Handle statements
            return eval_var_declaration(astNode, env)
        case _:
            print(
                f"This AST Node has not yet been setup for interpretation.\n{astNode}",
                file=sys.stderr,
            )
            exit(1)
