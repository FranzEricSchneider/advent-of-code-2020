from itertools import count
from math import gcd


def get_lcm(values):
    lcm = values[0]
    for value in values[1:]:
      lcm = lcm * value // gcd(lcm, value)
    return lcm 


def good(number, busses, test_index):
    bus, offset = busses[test_index]
    if offset == 0:
        if (number % bus) == offset:
            return True
    else:
        if bus - (number % bus) == offset % bus:
            return True
    return False


def main():

    with open("day13.txt", "r") as fin:
        fin.readline()
        bus_line = fin.readline().strip()

    busses = sorted(
        [(int(x), offset)
         for offset, x in enumerate(bus_line.split(","))
         if x != "x"],
        reverse=True,
    )
    values = [bus[0] for bus in busses]

    step_value = busses[0][0]
    timestamp = -busses[0][1]
    test_index = 1
    while True:
        timestamp += step_value
        if good(timestamp, busses, test_index):
            test_index += 1
            step_value = get_lcm(values[:test_index])

            if test_index == len(busses):
                break

    # Do a last check
    for i in range(len(busses)):
        assert good(timestamp, busses, i)

    print(f"Earliest good time stamp: {timestamp}")


if __name__ == '__main__':
    main()
