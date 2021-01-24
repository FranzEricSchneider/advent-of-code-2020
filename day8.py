class Command:
    def __init__(self, index, line):
        self.index = index
        self.command, number = line.strip().split(" ")
        self.number = int(number)
        self.executed = False

    def execute(self, accumulator):
        if self.executed:
            raise RuntimeError("Already executed, one bite at the apple!")

        if self.command == "nop":
            values = (accumulator, self.index + 1)
        elif self.command == "acc":
            values = (accumulator + self.number, self.index + 1)
        elif self.command == "jmp":
            values = (accumulator, self.index + self.number)
        else:
            raise ValueError(f"Bad command {self.command}")    

        self.executed = True
        return values


def main():
    with open("day8.txt", "r") as fin:
        commands = [Command(index, line)
                    for index, line in enumerate(fin.readlines())]

    accumulator = 0
    index = 0
    try:
        while True:
            accumulator, index = commands[index].execute(accumulator)
    except RuntimeError:
        pass

    print(f"accumulator = {accumulator} at the end")


if __name__ == '__main__':
    main()
