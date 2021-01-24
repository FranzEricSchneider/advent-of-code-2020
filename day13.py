def main():

    with open("day13.txt", "r") as fin:
        leave_time = int(fin.readline().strip())
        bus_line = fin.readline().strip()

    busses = [int(x) for x in bus_line.split(",") if x != "x"]
    deltas = [bus - leave_time % bus for bus in busses]
    min_time = min(deltas)

    print(f"Answer is {min_time * busses[deltas.index(min_time)]}")


if __name__ == '__main__':
    main()
