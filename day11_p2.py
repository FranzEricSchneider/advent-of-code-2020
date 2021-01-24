import numpy


# Accidentally corrupted this with Day 12 work


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
        self.position = numpy.array([0, 0])
        self.facing = numpy.array([1, 0])

    def execute(line):
        line = line.strip()
        char = line[0]
        number = int(line[1:])

        if char in DIRECTIONS:
            self.position += DIRECTIONS[char] * number
        elif char in TURN:
            self.facing = Rz(TURN[char] * number).dot(self.facing.reshape((2, 1))).flatten()
        elif char == "F":
            self.position += self.facing * number
        else:
            raise ValueError("Shouldn't ever get this")


def main():
    with open("day11.txt", "r") as fin:
        for line in fin.readlines():
            for column, char in enumerate(line.strip()):
                if char == SEAT:
                    seats.append(Seat(row, column))
            row += 1

    # Make a map and populate neighbors
    seat_map = SeatMap(seats)

    last_snapshot = None
    # Give it some sort of upper bound, play with the value as needed
    for _ in range(1000):

        # Calculate a round of changes
        seat_map.step()
        snapshot = seat_map.snapshot

        # Break if we've reached steady state
        if last_snapshot == snapshot:
            break
        # Save this run for the next comparison
        last_snapshot = snapshot
    else:
        raise RuntimeError("Never reached conclusion")

    print(f"{sum(snapshot)} seats occupied in steady state")


if __name__ == '__main__':
    main()
