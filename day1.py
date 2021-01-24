import itertools


def main():
    with open("day1.txt", "r") as fin:
        numbers = [int(line.strip()) for line in fin.readlines()]
        for a, b in itertools.permutations(numbers, 2):
            if a + b == 2020:
                print(f"Answer = {a * b}")


if __name__ == '__main__':
    main()
