import sys


class Command:
    def __init__(self, func: str, args: list[str]) -> None:
        self.func = func
        self.args = args

    def from_string(cmd: str) -> "Command":
        parsed_cmd = cmd.split(" ")
        func = parsed_cmd[0]
        args = parsed_cmd[1:]
        return Command(func, args)


def read() -> Command:
    sys.stdout.write("$ ")
    cmd = Command.from_string(input())
    return cmd


def exit_func(code: int) -> None:
    if isinstance(code, str):
        code = int(code)
    sys.exit(code)


def echo(*args: str) -> str:
    return " ".join(args)


def type_func(arg: str) -> str:
    if arg in Evaluator.builtins:
        return f"{arg} is a shell builtin"
    return f"{arg}: not found"


class Evaluator:
    builtins = {"exit": exit_func, "echo": echo, "type": type_func}

    def eval(self, cmd: Command) -> str:
        if cmd.func in self.builtins:
            func = self.builtins[cmd.func]
            return func(*cmd.args)
        return f"{cmd.func}: command not found"


def print_result(result: str) -> None:
    sys.stdout.write(result + "\n")


def main():
    # TODO: Uncomment the code below to pass the first stage
    evaluator = Evaluator()
    while True:
        cmd = read()
        result = evaluator.eval(cmd)
        print_result(result)


if __name__ == "__main__":
    main()
