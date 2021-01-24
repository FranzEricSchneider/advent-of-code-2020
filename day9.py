from itertools import combinations


# Accidentally corrupted day9 with day19


class Rules:
    def __init__(self):
        self.collection = {}

    def add(self, line):
        key, rules = line.strip().split(":")
        rules = [
            component.split(" ")
            for component in rules.strip().split(" | ")
        ]
        self.collection[key] = rules


messages = []


def main():
    rules = Rules()
    with open("day19.txt", "r") as fin:
        for line in fin.readlines():
            if ":" in line:
                rules.add(line)
            elif line.startswith("a") or line.startswith("b"):
                messages.append(line.strip())
            else:
                # There are some noop lines, like the extra blank line
                # betwee rules and messages

    import ipdb; ipdb.set_trace()

    print(f"first invalid number: {numbers[index]}, (index {index})")


if __name__ == '__main__':
    main()
