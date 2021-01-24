SEAT = "L"


class Seat:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.neighbors = []
        self.full = False

    @property
    def id(self):
        return make_id(self.row, self.column)

    def __repr__(self):
        return f"Seat(id {self.id}, full: {self.full})"

    def __lt__(self, other):
        return self.id < other.id

    @property
    def full_neighbors(self):
        return len([n for n in self.neighbors if n.full])

    def next_value(self):
        if self.full and self.full_neighbors >= 4:
            return False
        elif not self.full and self.full_neighbors == 0:
            return True
        else:
            return self.full


def make_id(row, column):
    return (row, column)


class SeatMap:
    def __init__(self, seat_list):
        self.map = {seat.id: seat for seat in seat_list}
        # Populate neighbors
        for key, seat in self.map.items():
            for dy, dx in ((-1, 1),  (0, 1),  (1, 1),
                           (-1, 0),           (1, 0),
                           (-1, -1), (0, -1), (1, -1)):
                neighbor_id = make_id(seat.row + dy, seat.column + dx)
                try:
                    seat.neighbors.append(self.map[neighbor_id])
                except KeyError:
                    # Neighbor ID didn't exist
                    pass
            seat.neighbors = sorted(seat.neighbors)

        # Make a fixed order view into the keys
        self.key_list = tuple(sorted(self.map.keys()))

    @property    
    def snapshot(self):
        return [self.map[key].full for key in self.key_list]

    def step(self):
        # Calculate this first, and then apply, instead of changing in place as
        # you go
        new_values = [self.map[key].next_value() for key in self.key_list]
        # And apply the new values all at once
        for key, new_value in zip(self.key_list, new_values):
            self.map[key].full = new_value


def main():
    seats = []
    row = 0
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
