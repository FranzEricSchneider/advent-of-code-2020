from collections import namedtuple
from functools import reduce
import itertools
import operator


class Map():
    def __init__(self, filename):
        with open("day3.txt", "r") as fin:
            self.rows = [line.strip() for line in fin.readlines()]

    def spot(self, row, x):
        # 0-indexed
        row = self.rows[row]
        return row[x % len(row)]

    def is_tree(self, row, x):
        return self.spot(row, x) == "#"

def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def main():
    terrain = Map("day3.py")
    rows = range(len(terrain.rows))

    values = []
    for scalar in [1, 3, 5, 7, 0.5]:
        X = [scalar * row for row in rows]
        count = 0
        for row, x in zip(rows, X):
            # Only check for trees when x is almost an integer (necessary for
            # fractional scales like 2 down 1 over)
            if abs(x % 1) < 1e-6:
                if terrain.is_tree(row, int(x)):
                    count += 1
        values.append(count)

    print(f"{values}")
    print(f"Ran into {prod(values)} trees")


if __name__ == '__main__':
    main()
