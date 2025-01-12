from frontend.syntax_tree import Program, VarDeclaration
from runtime.environment import Environment
from runtime.values import MK_NULL, RuntimeVal


def eval_program(program: Program, env: Environment) -> RuntimeVal:
    from runtime.interpreter import evaluate

    lastEvaluated = MK_NULL()

    for statement in program.body:
        lastEvaluated = evaluate(statement, env)

    return lastEvaluated


def eval_var_declaration(declaration: VarDeclaration, env: Environment) -> RuntimeVal:
    from runtime.interpreter import evaluate

    value = (
        evaluate(declaration.value, env) if declaration.value is not None else MK_NULL()
    )

    return env.declare_var(declaration.identifier, value, declaration.constant)
