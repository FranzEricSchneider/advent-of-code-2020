import re


class Passport:
    def __init__(self):
        self.params = {}

    def add_line(self, line):
        kv_pairs = line.strip().split(" ")
        for pair in kv_pairs:
            key, value = pair.split(":")
            self.params[key] = value

    def is_valid(self):
        needed = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        if all([thing in self.params for thing in needed]):
            return True
        else:
            return False

    def is_real_passport(self):
        if self.is_valid and "cid" in self.params:
            return True
        else:
            return False

    def is_north_pole_pass(self):
        if self.is_valid and "cid" not in self.params:
            return True
        else:
            return False


def main():
    with open("day4.txt", "r") as fin:
        entries = []
        passport = Passport()
        for line in fin.readlines():
            if line == "\n":
                entries.append(passport)
                passport = Passport()
            else:
                passport.add_line(line)
        entries.append(passport)

    num_valid = len([e for e in entries if e.is_valid()])
    print(f"{num_valid} valid passports")


if __name__ == '__main__':
    main()
