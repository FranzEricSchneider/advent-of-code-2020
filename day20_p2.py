from collections import Counter, defaultdict
from itertools import combinations, product
import numpy
import re


SEA_MONSTER = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


class Patch:

    SIDES = (0, 1, 2, 3)
    DIRECTIONS = (numpy.array([1, 0]),
                  numpy.array([0, 1]),
                  numpy.array([-1, 0]),
                  numpy.array([0, -1]))

    def __init__(self, tile):
        self.tile = tile
        self.characters = []

        self.position = None
        self.sides_covered = []
        self.sides_ruled_out = []

    @classmethod
    def from_chars(cls, characters, tile=0):
        patch = cls(tile)
        for line in characters:
            patch.add_line(line)
        return patch

    def add_line(self, line):
        self.characters.append(line.strip())

    # TODO: I could cache views if we need time savings
    def view(self, base_side, rotations, flip):
        # If the base side is +x, we want to match that with our -x side
        my_side = (base_side + 2) % len(self.SIDES)

        # Then walk back a number of sides set by rotations. Rotation is in 90
        # degree increments, around global Z. If we want to check -x, with one
        # rotation increment, that means we must view our current +y.
        my_side = (my_side - rotations) % len(self.SIDES)

        # Map sides onto characters. We HAVE to read these in a consistent
        # manner, and I am choosing CCW (in positive rotation direction)
        if my_side == 0:
            line = [row[-1] for row in self.characters[::-1]]
        elif my_side == 1:
            line = list(reversed(self.characters[0]))
        elif my_side == 2:
            line = [row[0] for row in self.characters]
        elif my_side == 3:
            line = list(self.characters[-1])
        else:
            raise RuntimeError("How did I get here?")

        if flip:
            line = list(reversed(line))

        return "".join(line)

    # This is simplified by assuming there will only be one match (checked in
    # input)
    def match(self, base_side, other):
        encoding = {}
        # TODO: Should we make separate view and view_other functions so we
        # don't need to do this rotations=2 thing?
        my_view = self.view(base_side, rotations=2, flip=False)
        for flip in [False, True]:
            for rotations in self.SIDES:
                encoding = {"base_side": base_side,
                            "rotations": rotations,
                            "flip": flip}
                if my_view == other.view(**encoding):
                    # We need to report an opposite flip so the two sides
                    # "zipper" correctly
                    encoding["flip"] = not(encoding["flip"])
                    return encoding
        return None

    def apply(self, base_side, rotations, flip):
        # Do a set of 90 deg flips (positive rotation is around global Z)
        for _ in range(rotations):
            rebuilt = [
                "".join([row[i] for row in self.characters])
                for i in reversed(range(len(self.characters[0])))
            ]
            self.characters = rebuilt

        if flip:
            # Figure out which axis we're flipping along (vertical/horizontal)
            if base_side % 2 == 0:
                self.characters = self.characters[::-1]
            else:
                rebuilt = ["".join(reversed(row)) for row in self.characters]
                self.characters = rebuilt

    def set_relative_position(self, neighbor, neighbor_side):
        assert self.position is None, "Trying to set an already set position"
        index = self.SIDES.index(neighbor_side)
        self.position = neighbor.position + self.DIRECTIONS[index]


class PatchMap:
    def __init__(self):
        self.patches = []

    def add(self, patch):
        self.patches.append(patch)

    def position_tiles(self):

        self.patches[0].position = numpy.array([0, 0])
        last_placed = [self.patches[0]]
        sides = set(Patch.SIDES)

        while any([patch.position is None for patch in self.patches]):
            placed = []
            for patch in last_placed:
                for side in sides:
                    if side in patch.sides_covered or side in patch.sides_ruled_out:
                        continue
                    match = None
                    for other in self.patches:
                        if other.position is None:
                            match = patch.match(side, other)
                            if match is not None:
                                break
                    if match is None:
                        patch.sides_ruled_out.append(side)
                    else:
                        patch.sides_covered.append(side)
                        other.apply(**match)
                        other.set_relative_position(patch, side)
                        placed.append(other)
            last_placed = placed

    @property
    def full_view(self):
        full = []

        max_x, max_y = numpy.max([patch.position for patch in self.patches], axis=0)
        min_x, min_y = numpy.min([patch.position for patch in self.patches], axis=0)

        for y_row in range(max_y, min_y - 1, -1):
            # Choose all patches in this row (by Y) and sort by X
            row = [patch for patch in self.patches
                   if numpy.isclose(patch.position[1], y_row)]
            row = sorted(row, key=lambda x: x.position[0])

            # Join up the patch characters
            for patch_index in range(len(self.patches[0].characters)):
                full.append("".join([patch.characters[patch_index] for patch in row]))

        return full

    # Made this a class method for easier testing, so I wouldn't need to figure
    # out how to mock full_view
    @classmethod
    def find_pattern(cls, quilt, pattern):
        num_pattern_rows = len(pattern)
        found = []
        for quilt_index in range(len(quilt) - (num_pattern_rows - 1)):
            subrows = [
                quilt[quilt_index + i] for i in range(num_pattern_rows)
            ]
            for x_index in range(len(subrows[0])):
                matches = [
                    re.match(pattern[index],
                             subrows[index][x_index:x_index+len(pattern[index])])
                    for index in range(num_pattern_rows)
                ]
                if all([m is not None for m in matches]):
                    found.append((quilt_index, x_index))

        return found

    @classmethod
    def find_orientation(cls, patch, pattern):
        for rotations, base_side, flip in product([0, 1, 2, 3],
                                                  [0, 1],
                                                  [True, False]):
            # Remove some double cases
            if flip is False and base_side != 0:
                continue

            encoding = {"base_side": base_side,
                        "rotations": rotations,
                        "flip": flip}
            fresh = Patch.from_chars(patch.characters)
            fresh.apply(**encoding)
            print(f"cls.find_pattern(fresh.characters, pattern): {cls.find_pattern(fresh.characters, pattern)}")
            if cls.find_pattern(fresh.characters, pattern):
                return encoding
        return None


def main():
    patchmap = PatchMap()
    with open("day20.txt", "r") as fin:
        patch = None
        for line in fin.readlines():
            if line == "\n":
                patchmap.add(patch)
                patch = None
            elif line.startswith("Tile"):
                patch = Patch(int(line.strip().replace("Tile ", "").replace(":", "")))
            else:
                patch.add_line(line)
        if patch is not None:
            patchmap.add(patch)
    patchmap.position_tiles()

    # Make a patch so we can rotate and flip it without extending PatchMap
    superpatch = Patch.from_chars(patchmap.full_view)
    encoding = PatchMap.find_orientation(superpatch, SEA_MONSTER)
    superpatch.apply(**encoding)

    found = PatchMap.find_pattern(superpatch.characters, SEA_MONSTER)

    import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    main()
