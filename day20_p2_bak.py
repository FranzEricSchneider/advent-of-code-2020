from collections import Counter, defaultdict
from itertools import combinations, product
import numpy


DIRECTIONS = (
    ( 0,  1, 1), ( 0,  1, -1),
    ( 0, -1, 1), ( 0, -1, -1),
    (-1,  0, 1), (-1,  0, -1),
    ( 1,  0, 1), ( 1,  0, -1),
)


def Rz(angle):
    return numpy.array([
        [numpy.cos(angle), -numpy.sin(angle)],
        [numpy.sin(angle),  numpy.cos(angle)],
    ])


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

    # This would be MUCH harder if there were more than one match per side
    def position_tiles(self):
        # Build this first
        self.index_map = {scrap.tile: index
                          for index, scrap in enumerate(self.scraps)}

        last_placed = [0]
        self.scraps[0].positioned = True
        COUNT = 1  # HEYREMOVE
        while not all([scrap.positioned for scrap in self.scraps]):
            placed = []
            for index in last_placed:
                for edge_dir, (neighbor, neighbor_dir) in self.scraps[index].limited_possibilities:
                    if not neighbor.positioned:
                        print(f"COUNT: {COUNT}, ORIGIN TILE: {self.scraps[index].tile}, NEIGHBOR TILE: {neighbor.tile}")    # HEYREMOVE
                        COUNT += 1  # HEYREMOVE
                        neighbor.adjust_to_other(self.scraps[index], edge_dir, neighbor_dir)
                        placed.append(self.index_map[neighbor.tile])
                        
                        counter = Counter([tuple(ss.position.astype(int)) for ss in self.scraps])  # HEYREMOVE
                        for position, count in counter.items():  # HEYREMOVE
                            if not numpy.allclose(position, numpy.array([0, 0])):  # HEYREMOVE
                                if count > 1:  # HEYREMOVE
                                    import ipdb; ipdb.set_trace()  # HEYREMOVE
            last_placed = placed


class Scrap:
    def __init__(self, tile):
        self.tile = tile
        self._characters = []
        self.edges = {}
        self.possibilities = defaultdict(list)

        self.positioned = False
        self.position = numpy.array([0, 0])
        self.x_flip = False
        self.y_flip = False
        self.origin = numpy.eye(2)

    def __repr__(self):
        return f"Position: {self.position}, origin:\n{self.origin}"

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

    # If there were more than one solution per edge this would have to be
    # append instead of =, and we'd need to pick the right solution
    def connect(self, dir1, other, dir2):
        self.possibilities[dir1] = (other, dir2)
        other.possibilities[dir2] = (self, dir1)

    @property
    def limited_possibilities(self):
        for direction, neighbor in self.possibilities.items():
            if abs(direction[0]) > 0.5:
                if self.y_flip:
                    if direction[2] == -1:
                        yield direction, neighbor
                else:
                    if direction[2] == 1:
                        yield direction, neighbor
            else:
                if self.x_flip:
                    if direction[2] == -1:
                        yield direction, neighbor
                else:
                    if direction[2] == 1:
                        yield direction, neighbor

    def adjust_to_other(self, other, other_dir, my_dir):
        # Handle rotating
        goal_dir = -other.origin.dot(numpy.array(other_dir[:2]))
        current_dir = numpy.array(my_dir[:2])
        angle = numpy.arccos(current_dir.dot(goal_dir))
        if numpy.isclose(abs(angle), numpy.pi):
            sign = 1
        else:
            # Gave up on properly determining the sign
            if numpy.allclose(Rz(numpy.pi / 2).dot(current_dir), goal_dir):
                sign = 1
            else:
                sign = -1
        print(f"Rotate {numpy.rad2deg(sign * angle)} degrees")
        self.rotate(angle, sign)

        # And flipping
        should_flip = my_dir[2] == -1
        if should_flip:
            axis = 1 if abs(my_dir[0]) > 0.5 else 0
            print(f"Flipped axis {axis}")
            self.flip(axis)

        # And positioning
        self.set_position(other, other_dir)

        self.positioned = True
        print(f"Other: {other}")
        print(f"other_dir: {other_dir}")
        print(f"Transformed self: {self}")
        print(f"my_dir: {my_dir}")
        print("")

    def flip(self, axis):
        assert not self.positioned
        if axis == 0:
            self.x_flip = True
        else:
            self.y_flip = True
        self.origin[:, axis] *= -1

    def rotate(self, angle, sign):
        assert not self.positioned
        self.origin = self.origin.dot(Rz(sign * angle))

    def set_position(self, other, other_dir):
        assert not self.positioned
        self.position = numpy.round(
            other.position + other.origin.dot(numpy.array(other_dir[:2]))
        )


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
    scrapmap.position_tiles()

    from collections import Counter
    for a, b, in Counter([tuple(ss.position.astype(int)) for ss in scrapmap.scraps]).items():
        print(f"{b} x \t {a}")

    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    main()
