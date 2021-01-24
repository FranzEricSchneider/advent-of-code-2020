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
            self.values[address] = self.overwrite(set_value)

    def overwrite(self, value):
        # String off the initial "0b" with [2:]
        bitstring = bin(value)[2:]
        # Pad the string to 32
        bitstring = "0" * (len(self.mask) - len(bitstring)) + bitstring
        # Then build the new value up using the mask
        rebuilt = [
            original if overwrite == "X" else overwrite
            for original, overwrite in zip(bitstring, self.mask)
        ]
        return int("".join(rebuilt), 2)


def main():
    docking = Docking()
    with open("day14.txt", "r") as fin:
        for line in fin.readlines():
            docking.process(line)

    print(f"The sum of all values is {sum(docking.values.values())}")


if __name__ == '__main__':
    main()
