import re


class Passport:
    def __init__(self):
        self.params = {}

    def add_line(self, line):
        kv_pairs = line.strip().split(" ")
        for pair in kv_pairs:
            key, value = pair.split(":")
            if validated(key, value):
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


def validated(key, value):
    if key == "byr":
        return is_valid_year(value, 1920, 2002)
    elif key == "iyr":
        return is_valid_year(value, 2010, 2020)
    elif key == "eyr":
        return is_valid_year(value, 2020, 2030)
    elif key == "hgt":
        try:
            if value.endswith("cm"):
                hgt = int(value.replace("cm", ""))
                assert hgt >= 150
                assert hgt <= 193
                return True
            elif value.endswith("in"):
                hgt = int(value.replace("in", ""))
                assert hgt >= 59
                assert hgt <= 76
                return True
        except (ValueError, AssertionError):
            pass
    elif key == "hcl":
        try:
            assert value[0] == "#"
            assert len(value) == 7
            matches = re.search("[0-9a-z]*", value[1:]).group(0)
            assert len(matches) == len(value[1:])
            return True
        except (ValueError, AssertionError):
            pass
    elif key == "ecl":
        try:
            assert value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
            return True
        except (ValueError, AssertionError):
            pass
    elif key == "pid":
        try:
            assert len(value) == 9
            int(value)
            return True
        except (ValueError, AssertionError):
            pass
    elif key == "cid":
        return True
    else:
        raise ValueError("What? Got key {}".format(key))
    return False


def is_valid_year(value, min_valid, max_valid):
    try:
        assert len(value) == 4
        year = int(value)
        assert year >= min_valid
        assert year <= max_valid
        return True
    except (ValueError, AssertionError):
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
