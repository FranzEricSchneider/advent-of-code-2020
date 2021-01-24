class Command:
    def __init__(self, index, line):
        self.index = index
        self.operator, number = line.strip().split(" ")
        self.number = int(number)
        self.executed = False

    def execute(self, accumulator):
        if self.executed:
            raise RuntimeError("Already executed, one bite at the apple!")

        if self.operator == "nop":
            values = (accumulator, self.index + 1)
        elif self.operator == "acc":
            values = (accumulator + self.number, self.index + 1)
        elif self.operator == "jmp":
            values = (accumulator, self.index + self.number)
        else:
            raise ValueError(f"Bad command {self.operator}")    

        self.executed = True
        return values


def main():
    with open("day8.txt", "r") as fin:
        commands = [Command(index, line)
                    for index, line in enumerate(fin.readlines())]

    for command in commands:

        # Switch the commands
        if command.operator == "acc":
            continue
        else:
            command.original = command.operator
            command.operator = "jmp" if command.operator == "nop" else "nop"

        # Make bookkeeping variables
        accumulator = 0
        index = 0
        # Reset the execution counter
        for reset in commands:
            reset.executed = False
        try:
            while index < len(commands):
                accumulator, index = commands[index].execute(accumulator)
        except RuntimeError:
            pass

        if index == len(commands):
            break

        # Reset it to the original value
        command.operator = command.original

    else:
        raise RuntimeError("Couldn't find any solution")

    print(f"accumulator = {accumulator} at the end")


if __name__ == '__main__':
    main()
