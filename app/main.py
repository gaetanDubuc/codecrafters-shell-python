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
    sys.exit(code)


known_cmds = {"exit": exit_func}


def eval_command(cmd: Command) -> str:
    if cmd.func in known_cmds.keys():
        return known_cmds[cmd.func](*cmd.args)
    return f"{cmd}: command not found"


def print_result(result: str) -> None:
    sys.stdout.write(result + "\n")


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        cmd = read()
        result = eval_command(cmd)
        print_result(result)


if __name__ == "__main__":
    main()
