import numpy
import pytest

from day20_p2 import Patch, PatchMap


@pytest.fixture
def basic_patch():
    basic = Patch(2605)
    characters = [".###..",
                  ".#.#..",
                  "....##",
                  "....#.",
                  "....##",
                  "#...#."]
    for line in characters:
        basic.add_line(line)
    return basic


class TestPatch:

    def test_construction(self):
        patch = Patch(12345)
        patch.add_line(".###..\n")
        patch.add_line(".#.#..\n")
        patch.add_line("....##\n")
        patch.add_line("....#.\n")
        patch.add_line("....##\n")
        patch.add_line("#...#.\n")

        assert patch.tile == 12345
        assert patch.characters == [".###..",
                                    ".#.#..",
                                    "....##",
                                    "....#.",
                                    "....##",
                                    "#...#."]
        assert patch.position is None
        assert patch.sides_covered == []
        assert patch.sides_ruled_out == []

    def test_from_chars(self, basic_patch):
        patch = Patch.from_chars(basic_patch.characters, basic_patch.tile)
        assert patch is not basic_patch
        assert patch.tile == basic_patch.tile
        assert patch.characters == basic_patch.characters

    @pytest.mark.parametrize("base_side, rotations, flip, expected", (
        # Check all the basic sides using the base_side
        (2, 0, False, ".#.#.."),    # On the right
        (3, 0, False, "..###."),    # On the top
        (0, 0, False, ".....#"),    # On the left
        (1, 0, False, "#...#."),    # On the bottom
        # Check all the basic sides using rotations
        (2, 0, False, ".#.#.."),    # On the right
        (2, 1, False, "#...#."),    # On the top
        (2, 2, False, ".....#"),    # On the left
        (2, 3, False, "..###."),    # On the bottom
        # Again with a flip
        (2, 0, True, "..#.#."),    # On the right
        (3, 0, True, ".###.."),    # On the top
        (0, 0, True, "#....."),    # On the left
        (1, 0, True, ".#...#"),    # On the bottom
        # Again with a flip
        (2, 0, True, "..#.#."),    # On the right
        (2, 1, True, ".#...#"),    # On the top
        (2, 2, True, "#....."),    # On the left
        (2, 3, True, ".###.."),    # On the bottom
        # And a few more combined cases
        (3, 3, True, "#....."),
        (1, 1, False, ".....#"),
    ))
    def test_view(self, basic_patch, base_side, rotations, flip, expected):
        # Should get the same results mod 4, try a few values to check
        for i in range(4):
            assert basic_patch.view(base_side=base_side,
                                    rotations=(rotations + (4 * i)),
                                    flip=flip) == expected

    def test_basic_match(self, basic_patch):
        for base_side in Patch.SIDES:
            encoding = basic_patch.match(base_side=base_side, other=basic_patch)
            assert encoding == {"base_side": base_side, "rotations": 2, "flip": True}

    def test_got_nothing(self, basic_patch):
        other_patch = Patch(12345)
        for i in range(len(basic_patch.characters)):
            other_patch.add_line("." * len(basic_patch.characters[0]))

        for base_side in Patch.SIDES:
            encoding = basic_patch.match(base_side=base_side, other=other_patch)
            assert encoding is None

    def test_complex_case(self, basic_patch):
        other_patch = Patch(12345)
        characters = ["#....#",
                      "......",
                      "......",
                      "......",
                      "#.....",
                      "..#.#."]
        for line in characters:
            other_patch.add_line(line)

        assert basic_patch.match(base_side=0, other=other_patch) == \
               {"base_side": 0, "rotations": 3, "flip": False}
        assert other_patch.match(base_side=3, other=basic_patch) == \
               {"base_side": 3, "rotations": 1, "flip": False}

        assert basic_patch.match(base_side=2, other=other_patch) == \
               {"base_side": 2, "rotations": 0, "flip": True}
        assert other_patch.match(base_side=0, other=basic_patch) == \
               {"base_side": 0, "rotations": 0, "flip": True}

        assert basic_patch.match(base_side=3, other=other_patch) == \
               {"base_side": 3, "rotations": 3, "flip": True}
        assert other_patch.match(base_side=2, other=basic_patch) == \
               {"base_side": 2, "rotations": 1, "flip": True}

    characters = [".###..",
                  ".#.#..",
                  "....##",
                  "....#.",
                  "....##",
                  "#...#."]
    @pytest.mark.parametrize("encoding, expected", (
        # If we have one rotation, no flip, we get a positive 90 deg spin
        ({"base_side": 0, "rotations": 1, "flip": False},
          ["..#.#.",
           "..####",
           "##....",
           "#.....",
           "##....",
           ".....#"]),
        # Flip around the X axis
        ({"base_side": 0, "rotations": 0, "flip": True},
          ["#...#.",
           "....##",
           "....#.",
           "....##",
           ".#.#..",
           ".###.."]),
        # Flip around the Y axis
        ({"base_side": 3, "rotations": 0, "flip": True},
          ["..###.",
           "..#.#.",
           "##....",
           ".#....",
           "##....",
           ".#...#"]),
        # Try a complex spin-then-flip
        ({"base_side": 3, "rotations": 3, "flip": True},
         [".....#",
          "##....",
          "#.....",
          "##....",
          "..####",
          "..#.#."]),
    ))
    def test_apply(self, basic_patch, encoding, expected):
        basic_patch.apply(**encoding)
        assert basic_patch.characters == expected
        
    @pytest.mark.parametrize("basic_position, side, expected", (
        (numpy.array([3, 2]),  0, numpy.array([4, 2])),
        (numpy.array([-1, 0]), 1, numpy.array([-1, 1])),
        (numpy.array([2, -4]), 2, numpy.array([1, -4])),
        (numpy.array([4, 3]),  3, numpy.array([4, 2])),
    ))
    def test_set_relative_position(self, basic_patch, basic_position,
                                   side, expected):
        basic_patch.position = basic_position
        other_patch = Patch(12345)
        other_patch.set_relative_position(basic_patch, side)
        assert numpy.allclose(other_patch.position, expected)


class TestPatchMap:
    def test_full_view(self):
        patchmap = PatchMap()

        def make_patch(tile, lines, position):
            patch = Patch(tile)
            for line in lines:
                patch.add_line(line)
            patch.position = numpy.array(position)
            patchmap.add(patch)

        # Make a 3x3 grid in arbitrary order
        make_patch(5, ["...", ".X.", "..."], [4, -4])
        make_patch(6, ["...", "...", "..."], [5, -3])
        make_patch(4, ["^^^", "^^^", "^^."], [4, -2])
        make_patch(2, ["!..", "...", "..."], [5, -2])
        make_patch(8, [".**", ".**", ".**"], [4, -3])
        make_patch(7, ["@..", ".@.", "@.."], [3, -4])
        make_patch(0, [".#.", ".#.", ".#."], [3, -2])
        make_patch(1, ["#>#", "#.#", "#>#"], [5, -4])
        make_patch(3, ["..%", "..%", "..%"], [3, -3])

        assert patchmap.full_view == [
            ".#.^^^!..",
            ".#.^^^...",
            ".#.^^....",
            "..%.**...",
            "..%.**...",
            "..%.**...",
            "@.....#>#",
            ".@..X.#.#",
            "@.....#>#",
        ]

    def test_find_pattern(self):
        characters = [
            "..OO.##...",
            ".##O#...#.",
            "...#..OO..",
            "OO...OO.##",
            ".OOO##O#..",
            "...O..#..O",
            "......##.#",
        ]
        pattern1 = ["....##",
                    "##.#..",
                    "..#..."]
        pattern2 = ["OO",
                    ".O"]
        assert PatchMap.find_pattern(characters, pattern1) == [(0, 1), (3, 4)]
        assert PatchMap.find_pattern(characters, pattern2) == [(0, 2), (3, 0), (3, 5), (4, 2)]

    @pytest.mark.parametrize("encoding, inverse", (
        # Cover all rotations
        ({"base_side": 0, "rotations": 0, "flip": False}, None),
        ({"base_side": 0, "rotations": 1, "flip": False}, None),
        ({"base_side": 0, "rotations": 2, "flip": False}, None),
        ({"base_side": 0, "rotations": 3, "flip": False}, None),
        # Cover all flips
        ({"base_side": 0, "rotations": 0, "flip": True}, None),
        ({"base_side": 1, "rotations": 0, "flip": True}, None),
        # And some combinations. For the more complicated cases there are
        # multiple solutions, so we manually give one
        ({"base_side": 1, "rotations": 2, "flip": True},
         {"base_side": 0, "rotations": 0, "flip": True,}),
        ({"base_side": 1, "rotations": 1, "flip": True},
         {"base_side": 1, "rotations": 1, "flip": True,}),
        ({"base_side": 0, "rotations": 3, "flip": True},
         {"base_side": 1, "rotations": 1, "flip": True,}),
    ))
    def test_find_orientation(self, encoding, inverse):
        characters = [
            "..OO.##...",
            ".##O#...#.",
            "...#..OO..",
            "OO...OO.##",
            ".OOO##O#..",
            "...O..#..O",
            "..........",
        ]
        patch = Patch.from_chars(characters)
        patch.apply(**encoding)

        if inverse is None:
            encoding["rotations"] = -encoding["rotations"] % 4
            inverse = encoding

        # Only check for the more complex pattern to avoid multiple matches
        pattern = ["....##",
                   "##.#..",
                   "..#..."]
        assert PatchMap.find_orientation(patch, pattern) == inverse
