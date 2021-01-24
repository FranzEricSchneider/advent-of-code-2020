import itertools


def main():
    with open("day1.txt", "r") as fin:
        numbers = [int(line.strip()) for line in fin.readlines()]
        for combo in itertools.permutations(numbers, 3):
            if sum(combo) == 2020:
                print(f"Answer = {combo[0] * combo[1] * combo[2]}")


if __name__ == '__main__':
    main()
