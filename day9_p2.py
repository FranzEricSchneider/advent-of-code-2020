GOAL = 41682220


def main():
    with open("day9.txt", "r") as fin:
        numbers = [int(line.strip()) for line in fin.readlines()]

    for index in range(len(numbers)):
        summed = 0
        additional = 0
        while summed < GOAL:
            additional += 1
            collection = numbers[index: index + additional + 1]
            summed = sum(collection)

        if summed == GOAL:
            print(f"min ({min(collection)}) + max ({max(collection)}) = {min(collection) + max(collection)}")


if __name__ == '__main__':
    main()
