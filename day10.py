from collections import Counter
import numpy


def main():
    with open("day10.txt", "r") as fin:
        joltages = sorted([int(line.strip()) for line in fin.readlines()])

    # Add the starter joltage (0) and the final (+3 over the highest)
    joltages = [0] + joltages + [3 + max(joltages)]

    # Count the different jump levels
    counter = Counter(numpy.diff(joltages))
    
    # Check that we only have differences of (1, 2, 3)
    assert all([diff in [1, 2, 3] for diff in counter.keys()])

    print(f"Diffs of 1 * diffs of 3 = {counter[1] * counter[3]}")


if __name__ == '__main__':
    main()
