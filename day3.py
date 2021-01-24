from collections import namedtuple
import itertools


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
    X = [3 * row for row in rows]
    count = 0
    for row, x in zip(rows, X):
        if terrain.is_tree(row, x):
            count += 1
    values.append(count)

    print(f"Ran into {count} trees")


if __name__ == '__main__':
    main()
