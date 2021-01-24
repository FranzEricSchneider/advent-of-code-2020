# The special bag we are looking for
KEY = "shinygold"


class Rule:
    def __init__(self, line):
        line = line.strip()
        # Remove some troublesome stuff to make our job easier
        for bad in [" ", "bags", "bag", "."]:
            line = line.replace(bad, "")
        # Get the outer bag directly
        self.outer, inner = line.split("contain")
        # The count is not yet relevant but save it anyway
        self.inner = {
            component[1:]: int(component[0]) for component in inner.split(",")
            if component != "noother"
        }


class RuleMap:
    def __init__(self, rules):
        self.rule_map = {r.outer: list(r.inner.keys()) for r in rules}

    def could_contain(self, outer, key):
        children = self.rule_map[outer]
        if key in children:
            return True
        else:
            for inner in children:
                if self.could_contain(inner, key):
                    return True
        return False


def main():
    with open("day7.txt", "r") as fin:
        rules = [Rule(line) for line in fin.readlines()]
    rule_map = RuleMap(rules)

    could_contain = [
        rule for rule in rules
        if rule_map.could_contain(rule.outer, KEY)
    ]

    print(f"{len(could_contain)} bags could contain {KEY}")


if __name__ == '__main__':
    main()
