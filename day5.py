import re


class Ticket:
    def __init__(self, line):
        self.chars = line.strip()
        self.row = self.get_row()
        self.column = self.get_column()

    def get_row(self):
        chars = self.chars[:-3]
        return process_thing(
            chars,
            up_char="B",
            down_char="F",
            min_val=0,
            max_val=127,
        )

    def get_column(self):
        chars = self.chars[-3:]
        return process_thing(
            chars,
            up_char="R",
            down_char="L",
            min_val=0,
            max_val=7,
        )

    @property
    def identity(self):
        return self.row * 8 + self.column

    def __repr__(self):
        return f"{self.chars}, row: {self.row}, column: {self.column}, ID: {self.identity}"


def process_thing(chars, up_char, down_char, min_val, max_val):
    char = chars[0]
    half = (max_val + 1 - min_val) / 2
    # Assert that we're always dealing with ints
    assert abs(half % 1) < 1e-6
    if char == up_char:
        min_val += int(half)
    elif char == down_char:
        max_val -= int(half)
    else:
        raise ValueError(
            f"Character {char} didn't match up ({up_char}) or down {down_char}"
            "characters"
        )
    if len(chars) == 1:
        assert min_val == max_val, \
            "We needed to reach a valid value at this point, since chars is" \
            f"empty, but min_val ({min_val}) doesn't match max_val ({max_val})"
        return min_val
    else:
        return process_thing(chars[1:], up_char, down_char, min_val, max_val)


def main():
    with open("day5.txt", "r") as fin:
        tickets = [Ticket(line) for line in fin.readlines()]

    ids = [ticket.identity for ticket in tickets]
    print(f"Max ID is {max(ids)}")


if __name__ == '__main__':
    main()
