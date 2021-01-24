def parse(line, offset=0):
    parsed = []
    index = offset
    while index < len(line):
        char = line[index]
        if char in ("+", "*"):
            parsed.append(char)
            index += 1
        elif char == "(":
            parsed.append(parse(line, index + 1))
            index += walked_length(parsed[-1])
        elif char == ")":
            return parsed
        else:
            parsed.append(int(char))
            index += 1
    return parsed


def walked_length(equation):
    # Length of innards plus parentheses
    return sum([walked_length(thing) if isinstance(thing, list) else 1
                for thing in equation]) + 2


def solve(equation):
    unsolved = [i for i, thing in enumerate(equation)
                if isinstance(thing, list)]
    for i in unsolved:
        equation[i] = solve(equation[i])

    # Make some basic assertions
    for i, thing in enumerate(equation):
        if i % 2 == 0:
            assert isinstance(thing, int)
        else:
            assert thing in ("*", "+")
    value = equation[0]
    for operator, number in zip(equation[1::2], equation[2::2]):
        if operator == "*":
            value *= number
        else:
            value += number
    return value


def main():
    results = []
    with open("day18.txt", "r") as fin:
        for line in fin.readlines():
            equation = parse(line.strip().replace(" ", ""))
            results.append(solve(equation))

    print(f"Results sum: {sum(results)}")


if __name__ == '__main__':
    main()
