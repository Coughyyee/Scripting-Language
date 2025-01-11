from frontend.parser import Parser
from runtime.interpreter import evaluate
from runtime.environment import Environment
from runtime.values import *


def repl():
    parser = Parser()
    env = Environment()
    env.declare_var(
        "x", MK_NUMBER(1000)
    )  # Because we cant define variables in program just yet.
    env.declare_var("true", MK_BOOL(True))
    env.declare_var("false", MK_BOOL(False))
    env.declare_var("null", MK_NULL())

    print("Repl v0.0.1")
    while True:
        inp = input("> ")

        # Check for no user input or exit keyword
        if not inp or inp.__contains__("exit"):
            exit(1)

        program = parser.produce_ast(inp)
        # print(program) # AST Tree

        result = evaluate(program, env)
        print(result)


if __name__ == "__main__":
    repl()
