from collections import defaultdict
from itertools import combinations, product
import numpy


DIRECTIONS = (
    ( 0,  1, 1), ( 0,  1, -1),
    ( 0, -1, 1), ( 0, -1, -1),
    (-1,  0, 1), (-1,  0, -1),
    ( 1,  0, 1), ( 1,  0, -1),
)


class ScrapMap:
    def __init__(self):
        self.scraps = []

    def add(self, scrap):
        self.scraps.append(scrap)

    def calc_possibilities(self):
        for scrap1, scrap2 in combinations(self.scraps, 2):
            for dir1, dir2 in product(DIRECTIONS, repeat=2):
                if scrap1.match(dir1, scrap2, dir2):
                    scrap1.connect(dir1, scrap2, dir2)


class Scrap:
    def __init__(self, tile):
        self.tile = tile
        self._characters = []
        self.edges = {}
        self.possibilities = defaultdict(list)

        self.position = numpy.array([0, 0])
        self.origin = numpy.eye(2)

    def add_line(self, line):
        self._characters.append(line.strip())

    @property
    def characters(self):
        return "\n".join(self._characters)    

    def finalize(self):
        def set(id1, id2, origin):
            self.edges[id1] = origin if isinstance(origin, str) else "".join(origin)
            self.edges[id2] = "".join(reversed(self.edges[id1]))
        set((0, 1, 1), (0, 1, -1), self._characters[0])
        set((0, -1, 1), (0, -1, -1), self._characters[-1])
        set((-1, 0, 1), (-1, 0, -1), [row[0] for row in self._characters])
        set((1, 0, 1), (1, 0, -1), [row[-1] for row in self._characters])

    def match(self, dir1, other, dir2):
        return self.edges[dir1] == other.edges[dir2]

    def connect(self, dir1, other, dir2):
        self.possibilities[dir1].append((other, dir2))
        other.possibilities[dir2].append((self, dir1))


def main():
    scrapmap = ScrapMap()
    with open("day20.txt", "r") as fin:
        scrap = None
        for line in fin.readlines():
            if line == "\n":
                scrap.finalize()
                scrapmap.add(scrap)
                scrap = None
            elif line.startswith("Tile"):
                scrap = Scrap(int(line.strip().replace("Tile ", "").replace(":", "")))
            else:
                scrap.add_line(line)
    scrapmap.calc_possibilities()

    # This would be MUCH harder if there were more than one match per side
    corners = [scrap for scrap in scrapmap.scraps
               if len(scrap.possibilities) == 4]

    answer = 1
    for corner in corners:
        answer *= corner.tile

    print(f"Product of corner IDs: {answer}")


if __name__ == '__main__':
    main()
