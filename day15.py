def get_next(values):
    voi = values[0]
    compare = values[1:]
    try:
        return compare.index(voi) + 1
    except ValueError:
        return 0


def main():
    # Do everything reversed so list.index() gives us what we want
    values = list(reversed([20, 9, 11, 0, 1, 2]))
    while len(values) < 2020:
        # Prepend each value instead of appending
        values.insert(0, get_next(values))

    print(f"Final value is {values[0]}")


if __name__ == '__main__':
    main()
