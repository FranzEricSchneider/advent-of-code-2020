from collections import defaultdict
from itertools import combinations, product
import re


SPECIAL = ["a", "b"]
WILD = "."
BASE = "".join(SPECIAL)


class Simplifier:
    # Record seen substitution combinations
    seen = defaultdict(dict)
    populated = set()

    def simplify(self, given):
        by_length = defaultdict(list)
        for element in given:
            by_length[len(element)].append(element)

        for length in by_length.keys():
            self.populate(length)

        candidates = []
        for length, values in by_length.items():
            key = self.make_key(values, must_sort=False)
            if key in self.seen[length]:
                candidates.append(self.seen[length][key])
                continue

            value_set = set(values)
            # Find the largest combos first
            for combo_number in range(len(value_set) - 1, 1, -1):
                for combo in combinations(value_set, combo_number):
                    key = self.make_key(combo, must_sort=False)
                    if key in self.seen[length]:
                        value = self.seen[length][key]
                        # Only add values that aren't subsets of already
                        # identified stuff
                        if not any([self.check(regex, value) for regex in candidates]):
                            candidates.append(value)

        # Include elements not yet matched, and exclude duplicates in given
        rebuilt = [
            element for element in given
            if not any([self.check(regex, element) for regex in candidates] +
                       [regex != element and self.check(regex, element)
                        for regex in given])
        ]
        rebuilt.extend(candidates)
        return rebuilt

    def populate(self, length):
        if length in self.populated:
            return
        self.populated.add(length)

        for wild_length in range(length, 0, -1):
            if wild_length == length:
                insert_all = [
                    "".join(a) for a in product(BASE, repeat=length)
                ]
                self.seen[length][self.make_key(insert_all)] = WILD * length
            else:
                for static in product(BASE, repeat=length - wild_length):
                    for wild_indices in combinations(range(length), wild_length):
                        elements = []
                        for dynamic in product(BASE, repeat=wild_length):
                            shtatic = list(static)
                            shmynamic = list(dynamic)
                            construct = "".join([
                                shmynamic.pop(0) if index in wild_indices else shtatic.pop(0)
                                for index in range(length)
                            ])
                            elements.append(construct)
                        shtatic = list(static)
                        value = "".join([
                            WILD if index in wild_indices else shtatic.pop(0)
                            for index in range(length)
                        ])
                        self.seen[length][self.make_key(elements)] = value

        # Reverse engineer some of the values to partially take out the wilds
        new = {}
        for values in self.seen[length].values():
            wild_indices = [index for index, char in enumerate(values) if char == WILD]
            wild_count = len(wild_indices)
            if wild_count >= 2:
                for num_substitute in range(1, wild_count):
                    for sub_indices in combinations(wild_indices, num_substitute):
                        key = []
                        for dynamic in product(BASE, repeat=num_substitute):
                            shtatic = list(values)
                            shmynamic = list(dynamic)
                            construct = "".join([
                                shmynamic.pop(0) if index in sub_indices else shtatic.pop(0)
                                for index in range(length)
                            ])
                            key.append(construct)
                        new[self.make_key(key)] = values
        self.seen[length].update(new)

    @classmethod
    def make_key(cls, element_list, must_sort=True):
        if must_sort:
            return "".join(sorted(list(set(element_list))))
        else:
            return "".join(list(set(element_list)))

    @classmethod
    def check(cls, regex, value):
        test = re.compile(f"^{regex}$")
        return test.match(value) is not None


class Rules:
    def __init__(self):
        self.collection = {}
        self.simpler = Simplifier()

    def add(self, line):
        key, rules = line.strip().replace('"', "").split(":")
        rules = [
            component.split(" ")
            for component in rules.strip().split(" | ")
        ]
        # Get rid of [["a"]] to just make it ["a"]
        if rules == [[SPECIAL[0]]] or rules == [[SPECIAL[1]]]:
            rules = rules[0]
        self.collection[key] = rules

    def get_letters(self):
        return {
            index: rules for index, rules in self.collection.items()
            if all([isinstance(subcomponent, str) for subcomponent in rules])
        }

    def unlettered(self):
        return {
            index: rules for index, rules in self.collection.items()
            if not all([isinstance(subcomponent, str) for subcomponent in rules])
        }

    def reduce_rank(self):
        letters = self.get_letters()

        for index, rules in self.collection.items():
            if index in letters:
                continue

            rebuilt = []
            for subcomponent in rules:
                # If there's no replacement, move on
                if not any([key in letters for key in subcomponent]):
                    rebuilt.append(subcomponent)
                    continue

                # Build out a series of branching options with replacement
                product_options = [
                    letters[key] for key in subcomponent
                    if key in letters
                ]
                for option_set in product(*product_options):
                    poppable = list(option_set)
                    rebuilt.append([
                        key if key not in letters else poppable.pop(0)
                        for key in subcomponent
                    ])

            # Then replace any subcomponents that have been reduced to strings
            for subcomponent_index in range(len(rebuilt)):
                subcomponent = rebuilt[subcomponent_index]
                if all([all([char in SPECIAL + [WILD] for char in entry])
                       for entry in subcomponent]):
                    rebuilt[subcomponent_index] = "".join(subcomponent)

            try:
                self.collection[index] = sorted(rebuilt)
            except TypeError:
                self.collection[index] = rebuilt

    def simplify(self):
        for key, letter_list in self.get_letters().items():
            self.collection[key] = self.simpler.simplify(letter_list)

    def brute_simplify(self):
        rebuilt = defaultdict(list)
        for key, values in self.collection.items():
            if len(values) > 20:
                for value in sorted(values, key=lambda x: x.count(WILD)):
                    if not any([self.simpler.check(regex, value) for regex in rebuilt[key]]):
                        rebuilt[key].append(value)
        self.collection.update(rebuilt)

    def trace(self, current):
        for or_component in current:
            for subcomponent in or_component:
                if subcomponent in SPECIAL:
                    return subcomponent
                else:
                    return self.trace(subcomponent)

    def __repr__(self):
        return "\n".join([str(item) for item in sorted(self.collection.items())])

    def is_valid(self, message, max_len):
        if len(message) > max_len:
            return False
        return any([self.simpler.check(regex, message)
                    for regex in self.collection["0"]])


messages = []


def main():
    rules = Rules()
    with open("day19.txt", "r") as fin:
        for line in fin.readlines():
            if ":" in line:
                rules.add(line)
            elif line.startswith(SPECIAL[0]) or line.startswith(SPECIAL[1]):
                messages.append(line.strip())
            else:
                # There are some noop lines, like the extra blank line
                # betwee rules and messages
                pass

    # from cProfile import Profile
    # profile = Profile()
    # profile.enable()
    print(f"Number of straight letters {len(rules.get_letters())} / {len(rules.collection)}")
    for _ in range(6):
        rules.reduce_rank()
        rules.simplify()
        print(f"Number of straight letters {len(rules.get_letters())} / {len(rules.collection)}")
    # profile.disable()
    # profile.dump_stats("/home/eric/Desktop/profile.runsnake")
    # for _ in range(4):
    #     rules.reduce_rank()
    #     print(f"Number of straight letters {len(rules.get_letters())} / {len(rules.collection)}")
    # rules.brute_simplify()
    # print("Brutes")

    # for k, v in rules.collection.items(): print(v)
    # import ipdb; ipdb.set_trace()

    # assert "0" in rules.get_letters()
    # max_len = max([len(regex) for regex in rules.collection["0"]])
    # count = 0
    # for i, message in enumerate(messages):
    #     if rules.is_valid(message, max_len):
    #         count += 1
    #     print(f"{i} / {len(messages)}, checking {len(rules.collection['0'])} regexes")

    # print(f"Num valid messages: {count}")


if __name__ == '__main__':
    main()
