from collections import defaultdict
STOP = 30000000


def get_next(values, last_value):
    if len(values[last_value]) == 1:
        return 0
    else:
        return values[last_value][0] - values[last_value][1]


def main():
    # Do everything reversed so list.index() gives us what we want
    values = defaultdict(list)
    values[20] = [1]
    values[9] = [2]
    values[11] = [3]
    values[0] = [4]
    values[1] = [5]
    values[2] = [6]
    counter = 6
    last_value = 2
    while counter < STOP:
        counter += 1
        last_value = get_next(values, last_value)
        values[last_value].insert(0, counter)
        while len(values[last_value]) > 2:
            values[last_value].pop()

    print(f"Final value is {last_value}")


if __name__ == '__main__':
    main()
