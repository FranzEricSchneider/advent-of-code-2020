from collections import defaultdict, namedtuple


class Range:
    def __init__(self, min_val, max_val):
        self.min = min_val
        self.max = max_val

    def in_range(self, value):
        return self.min <= value <= self.max

    def __repr__(self):
        return f"Range({self.min}, {self.max})"


class Rules:
    def __init__(self):
        self.map = defaultdict(list)

    def add(self, line):
        name, temp = line.split(":")
        temp = temp.strip()
        for ranges in temp.split(" or "):
            self.map[name].append(
                Range(*[int(value) for value in ranges.split("-")])
            )

    def any_good(self, value):
        for ranges in self.map.values():
            for this_range in ranges:
                if this_range.in_range(value):
                    return True
        return False


class Ticket:
    def __init__(self, line):
        self.values = [int(value) for value in line.strip().split(",")]

    def bad_values(self, rules):
        bad = []
        for value in self.values:
            if not rules.any_good(value):
                bad.append(value)
        return bad


def throwaway(fin, count):
    for _ in range(count):
        fin.readline()


def main():
    rules = Rules()
    with open("day16.txt", "r") as fin:
        # Read the rules
        for i in range(20):
            rules.add(fin.readline())
        # Read the tickets in
        throwaway(fin, 2)
        my_ticket = Ticket(fin.readline())
        throwaway(fin, 2)
        others = [
            Ticket(line)
            for line in fin.readlines()
        ]

    bad = []
    for ticket in others:
        bad.extend(ticket.bad_values(rules))

    print(f"Sum of bad values: {sum(bad)}")


if __name__ == '__main__':
    main()
