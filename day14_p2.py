from itertools import product


class Docking:
    def __init__(self):
        self.values = {}

    def process(self, line):
        line = line.strip()
        if line.startswith("mask"):
            self.mask = line[7:]
        else:
            line = line.split(" ")
            address = int(line[0].replace("mem[", "").replace("]", ""))
            set_value = int(line[-1])
            for modified in self.calc_addresses(address):
                self.values[modified] = set_value

    def calc_addresses(self, value):
        # String off the initial "0b" with [2:]
        bitstring = bin(value)[2:]
        # Pad the string to 36
        bitstring = "0" * (len(self.mask) - len(bitstring)) + bitstring
        # Then build the new value up using the mask. This will be a two-step
        # process. First, overwrite anywhere there was a 1
        rebuilt = [
            overwrite if overwrite == "1" else original
            for original, overwrite in zip(bitstring, self.mask)
        ]
        # Floating indices
        solutions = []
        floating = [i for i, char in enumerate(self.mask) if char == "X"]
        if floating:
            for bitvals in product("01", repeat=len(floating)):
                for index, bit in zip(floating, bitvals):
                    rebuilt[index] = bit
                solutions.append(int("".join(rebuilt), 2))
        else:
            solutions.append(int("".join(rebuilt), 2))

        return solutions


def main():
    docking = Docking()
    with open("day14.txt", "r") as fin:
        for line in fin.readlines():
            docking.process(line)

    print(f"The sum of all values is {sum(docking.values.values())}")


if __name__ == '__main__':
    main()
