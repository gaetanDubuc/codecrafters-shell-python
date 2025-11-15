import os
import subprocess
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


def type_func(*args: str) -> str:
    arg = args[0]
    if arg in Evaluator.builtins:
        return f"{arg} is a shell builtin"
    full_path = check_path(arg)
    if full_path:
        return f"{arg} is {full_path}"
    return f"{arg}: not found"


def check_path(cmd: str) -> str | None:
    path = os.environ.get("PATH", "")
    for dir in path.split(os.pathsep):
        full_path = os.path.join(dir, cmd)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path


def pwd():
    return os.getcwd()


def cd(path: str) -> None:
    if not os.path.isdir(path):
        return f"cd: {path}: No such file or directory"
    os.chdir(path)


class Evaluator:
    builtins = {
        "exit": exit_func,
        "echo": echo,
        "type": type_func,
        "pwd": pwd,
        "cd": cd,
    }

    def eval(self, cmd: Command) -> str:
        if cmd.func in self.builtins:
            func = self.builtins[cmd.func]
            return func(*cmd.args)

        result = self.eval_program(cmd)
        if result is not None:
            return result
        return f"{cmd.func}: command not found"

    def eval_program(self, cmd: Command) -> str | None:
        full_path = check_path(cmd.func)
        if full_path:
            result = subprocess.run(
                [cmd.func] + cmd.args,
                stdout=subprocess.STDOUT,
                stderr=subprocess.STDOUT,
            )
            return result.stdout.decode()
        return None


def print_result(result: str) -> None:
    if result is None:
        return
    if result.endswith("\n"):
        print(result, end="")
    print(result)


def main():
    # TODO: Uncomment the code below to pass the first stage
    evaluator = Evaluator()
    while True:
        cmd = read()
        result = evaluator.eval(cmd)
        print_result(result)


if __name__ == "__main__":
    main()
