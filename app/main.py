import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    cmd = input()
    sys.stdout.write(f"{cmd}: command not found")
    pass


if __name__ == "__main__":
    main()
