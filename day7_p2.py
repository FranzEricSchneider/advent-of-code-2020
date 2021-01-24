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
        self.rule_map = {r.outer: r.inner for r in rules}

    def num_children(self, parent):
        children = self.rule_map[parent]
        if len(children) == 0:
            return 0
        else:
            count = 0
            for inner, number in children.items():
                count += number * (1 + self.num_children(inner))
            return count


def main():
    with open("day7.txt", "r") as fin:
        rules = [Rule(line) for line in fin.readlines()]
    rule_map = RuleMap(rules)

    print(f"{KEY} contains {rule_map.num_children(KEY)} bags")


if __name__ == '__main__':
    main()
