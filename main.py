from frontend.parser import Parser

def repl():
    parser = Parser()

    print("Repl v0.0.1")
    while True:
        inp = input("> ")

        # Check for no user input or exit keyword
        if not inp or inp.__contains__("exit"):
            exit(1)

        program = parser.produceAST(inp)
        print(program)


if __name__ == "__main__":
    repl()