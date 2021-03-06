from collections import namedtuple
import itertools


Entry = namedtuple("Entry", "min, max, char, password")


def valid(entry):
    count = entry.password.count(entry.char)
    if count < entry.min or count > entry.max:
        return False
    else:
        return True


def main():
    with open("day2.txt", "r") as fin:
        entries = []
        for line in fin.readlines():
            line, password = line.split(":")
            line, char = line.split(" ")
            min_val, max_val = line.split("-")
            entries.append(Entry(
                min=int(min_val.strip()),
                max=int(max_val.strip()),
                char=char.strip(),
                password=password.strip(),
            ))

    num_valid = 0
    for entry in entries:
        if valid(entry):
            num_valid += 1

    print(f"Number valid: {num_valid}")


if __name__ == '__main__':
    main()
