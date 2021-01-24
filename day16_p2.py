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

    def populate_indices(self):
        # Initially all indices are possible
        self.map_indices = {
            key: set(range(len(self.map)))
            for key in self.map.keys()
        }

    def apply_ticket(self, ticket):
        for key in self.map_indices.keys():
            self.map_indices[key] = self.map_indices[key].intersection(
                ticket.possibilities(self.map[key])
            )

    def finalize_indices(self):
        # Solve so there is only one solution left for each key
        while any([len(v) > 1 for v in self.map_indices.values()]):
            claimed = [v for v in self.map_indices.values() if len(v) == 1]
            for possible_set in self.map_indices.values():
                if len(possible_set) > 1:
                    for gone in claimed:
                        possible_set -= gone

        # Take it from a set to an index
        self.finalized = {
            key: value.pop()
            for key, value in self.map_indices.items()
        }


class Ticket:
    def __init__(self, line):
        self.values = [int(value) for value in line.strip().split(",")]

    def bad_values(self, rules):
        bad = []
        for value in self.values:
            if not rules.any_good(value):
                bad.append(value)
        return bad

    def possibilities(self, ranges):
        return set(
            i for i, value in enumerate(self.values)
            if any([this_range.in_range(value) for this_range in ranges])
        )


def throwaway(fin, count):
    for _ in range(count):
        fin.readline()


def main():
    rules = Rules()
    with open("day16.txt", "r") as fin:
        # Read the rules
        for i in range(20):
            rules.add(fin.readline())
        rules.populate_indices()
        # Read the tickets in
        throwaway(fin, 2)
        my_ticket = Ticket(fin.readline())
        throwaway(fin, 2)
        others = [
            Ticket(line)
            for line in fin.readlines()
        ]

    # Winnow down to good tickets
    winnowed = []
    for ticket in others:
        if not ticket.bad_values(rules):
            winnowed.append(ticket)

    for ticket in winnowed:
        rules.apply_ticket(ticket)
    rules.finalize_indices()


    product = 1
    for k, v in rules.finalized.items():
        if k.startswith("departure"):
            product *= my_ticket.values[v]
    print(f"Departure product: {product}")


if __name__ == '__main__':
    main()
