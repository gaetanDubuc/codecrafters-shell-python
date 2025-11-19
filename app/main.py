import os
import subprocess
import sys
from dataclasses import dataclass
from shlex import split
from typing import TextIO


@dataclass
class Command:
    func: str
    args: list[str]
    redirection: bool = False
    output_file: TextIO = sys.stdout

    @classmethod
    def from_string(cls, cmd: str) -> "Command":
        parsed_cmd = split(cmd)

        func = parsed_cmd[0]
        args = parsed_cmd[1:]

        redirection = False
        output_file = sys.stdout
        if ">" in args:
            redir_index = args.index(">")
            redirection = True
            output_file: TextIO = open(args[redir_index + 1], "w")
            args = args[:redir_index]
        return Command(func, args, redirection, output_file)


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


def cd(path: str) -> str | None:
    path = os.path.expanduser(path)
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

    def eval(self, cmd: Command) -> str | None:
        if cmd.func in self.builtins:
            func = self.builtins[cmd.func]
            return func(*cmd.args)

        result = self.eval_program(cmd)
        if result:
            return None
        return f"{cmd.func}: command not found"

    def eval_program(self, cmd: Command) -> bool:
        full_path = check_path(cmd.func)
        if full_path:
            subprocess.run(
                [cmd.func] + cmd.args,
                stdout=cmd.output_file,
                stderr=sys.stderr,
            )
            return True
        return False


def print_result(result: str | None) -> None:
    if result is None:
        return
    if result.endswith("\n"):
        print(result, end="")
    print(result)


def main():
    evaluator = Evaluator()
    while True:
        cmd = read()
        try:
            result = evaluator.eval(cmd)
            print_result(result)
        finally:
            cmd.output_file.close()


if __name__ == "__main__":
    main()
