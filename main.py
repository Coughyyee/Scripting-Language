import argparse
from rich import print
from frontend.parser import Parser
from runtime.interpreter import evaluate
from runtime.environment import Environment, create_global_env
from runtime.values import *


def run(filename: str):
    parser = Parser()
    env = create_global_env()

    print("[bold]Repl [cyan]v0.0.1[/cyan][/bold]")

    try:
        with open(filename, "r") as file:
            content = file.read()
            # if "exit" in content:
            #     exit(1)
            program = parser.produce_ast(content)
            result = evaluate(program, env)
            print(result)
    except FileNotFoundError:
        print(f"[bold red]error:[/bold red] File '{filename}' does not exist.")
        exit(1)


def repl():
    parser = Parser()
    env = create_global_env()

    print("[bold]Repl [cyan]v0.0.1[/cyan][/bold]")

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
    flag_parser = argparse.ArgumentParser(description="Interpreter argument flags.")
    flag_parser.add_argument("--file", type=str, help="Specify filename")
    args = flag_parser.parse_args()
    if args.file:
        filename = args.file
        run(filename)
    else:
        repl()
