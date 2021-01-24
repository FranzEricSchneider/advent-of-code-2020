from itertools import product
import numpy


ACTIVE = "#"


class Point:
    def __init__(self, x, y, z, active=False):
        self.position = numpy.array([x, y, z], dtype=int)
        self.active = active

    def __repr__(self):
        return "{}:{}".format(self.id, "ON" if self.active else "OFF")

    def __lt__(self, other):
        return self.id < other.id

    @property
    def id(self):
        return "{},{},{}".format(*self.position.tolist())

    @classmethod
    def from_id(cls, identity):
        return cls(*map(int, identity.split(",")))

    def neighbor_ids(self):
        for offsets in product([-1, 0, 1], repeat=3):
            if offsets == (0, 0, 0):
                continue
            else:
                yield Point(
                    *(self.position + numpy.array(offsets)).tolist()
                ).id

    def num_active_neighbors(self, point_map):
        return len([
            neighbor_id
            for neighbor_id in self.neighbor_ids()
            if neighbor_id in point_map and point_map[neighbor_id].active
        ])

    def next_value(self, point_map):
        if self.active:
            if self.num_active_neighbors(point_map) in  [2, 3]:
                return True
        else:
            if self.num_active_neighbors(point_map) == 3:
                return True
        return False


class Grid:
    def __init__(self, points):
        self.map = {point.id: point for point in points}
        self.populate_active_neighbors()

    def __repr__(self):
        return "\n".join(str(point) for point in sorted(self.map.values()))

    def populate_active_neighbors(self):
        for point in list(self.map.values()):
            if point.active:
                for neighbor_id in point.neighbor_ids():
                    if neighbor_id not in self.map:
                        self.map[neighbor_id] = Point.from_id(neighbor_id)

    @property
    def num_active(self):
        return len([point for point in self.map.values() if point.active])

    def step(self):
        # Calculate this first, and then apply, instead of changing in place as
        # you go
        new_values = {
            key: self.map[key].next_value(self.map) for key in self.map.keys()
        }
        # And apply the new values all at once
        for key, new_value in new_values.items():
            self.map[key].active = new_value

        # Then build up the edges
        self.populate_active_neighbors()


def main():
    points = []
    row = 0
    with open("day17.txt", "r") as fin:
        for line in fin.readlines():
            for column, char in enumerate(line.strip()):
                points.append(Point(x=row, y=column, z=0, active=char == ACTIVE))
            row += 1

    # Make a map and populate neighbors
    grid = Grid(points)

    # Give it some sort of upper bound, play with the value as needed
    for _ in range(6):
        # Calculate a round of changes
        grid.step()

    print(f"{grid.num_active} points occupied at the end of 6")


if __name__ == '__main__':
    main()
