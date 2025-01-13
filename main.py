from frontend.parser import Parser
from runtime.interpreter import evaluate
from runtime.environment import Environment
from runtime.values import *

FILE = False


def repl():
    parser = Parser()
    env = Environment()
    env.declare_var("true", MK_BOOL(True), True)
    env.declare_var("false", MK_BOOL(False), False)
    env.declare_var("null", MK_NULL(), True)

    print("Repl v0.0.1")

    if FILE:
        with open("test.txt", "r") as file:
            content = file.read()
            if "exit" in content:
                exit(1)
            program = parser.produce_ast(content)
            result = evaluate(program, env)
            print(result)
    else:
        while True:
            inp = input("> ")

            # Check for no user input or exit keyword
            if inp == "" or "exit" in inp:
                exit(1)

            program = parser.produce_ast(inp)
            # print(program) # AST Tree

            result = evaluate(program, env)
            print(result)


if __name__ == "__main__":
    repl()
