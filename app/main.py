import sys


def read() -> str:
    sys.stdout.write("$ ")
    return input()


known_cmds = {}


def eval_command(cmd: str) -> str:
    if cmd in known_cmds:
        return ""
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
