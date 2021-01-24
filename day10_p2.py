from itertools import combinations
import numpy


def main():
    with open("day10.txt", "r") as fin:
        joltages = sorted([int(line.strip()) for line in fin.readlines()])

    # Add the starter joltage (0) and the final (+3 over the highest)
    joltages = [0] + joltages + [3 + max(joltages)]
    # Get the diffs
    diffs = numpy.diff(joltages)

    # Count the sizes of discrete groups of "1"s. Nothing matters other than
    # the size and number of these groups
    group_count = 0
    groups = []
    for value in diffs:
        if value == 1:
            group_count += 1
        elif value == 3:
            if group_count > 0:
                groups.append(group_count)
            group_count = 0
        else:
            raise ValueError("Shouldn't exist")

    # This is the number of valid combos you can make with a group of "1" diffs
    # of this size.
    # This is a handmade map. I was going to write code for "number of valid
    # groupings from a given group size" but then I saw the max group size was
    # 4 and I thought "why bother"
    group_options = {
        1: 1,
        2: 2,
        3: 4,
        4: 7,
    }
    options = [group_options[group_count] for group_count in groups]

    value = 1
    for option in options:
        value *= option

    print(f"Total number of options: {value}")


if __name__ == '__main__':
    main()
