import numpy


DIRECTIONS = {
    "E": numpy.array([ 1,  0]),
    "W": numpy.array([-1,  0]),
    "N": numpy.array([ 0,  1]),
    "S": numpy.array([ 0, -1]),
}

# Sign of the turn around z axis
TURN = {
    "L": 1,
    "R": -1,
}


def Rz(angle):
    # Comes in as degrees
    angle = numpy.deg2rad(angle)
    return numpy.array([
        [numpy.cos(angle), -numpy.sin(angle)],
        [numpy.sin(angle),  numpy.cos(angle)],
    ])


class Ship:
    def __init__(self):
        self.position = numpy.array([0, 0], dtype=float)
        self.waypoint = numpy.array([10, 1], dtype=float)

    def execute(self, line):
        line = line.strip()
        char = line[0]
        number = int(line[1:])

        if char in DIRECTIONS:
            self.waypoint += DIRECTIONS[char] * number
        elif char in TURN:
            self.waypoint = Rz(TURN[char] * number).dot(self.waypoint.reshape((2, 1))).flatten()
        elif char == "F":
            self.position += self.waypoint * number
        else:
            raise ValueError("Shouldn't ever get this")


def main():
    ship = Ship()
    with open("day12.txt", "r") as fin:
        for line in fin.readlines():
            ship.execute(line)

    print(f"Ship now at {ship.position}, Manhattan distance = {sum(abs(ship.position))}")


if __name__ == '__main__':
    main()
