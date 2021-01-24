from day19 import Simplifier


def test_make_key():
    simp = Simplifier()
    assert simp.make_key(["aa", "ba", "ab", "aa"]) == "aaabba"


def test_populate():
    simp = Simplifier()
    simp.populate(3)
    for key, expected in (("aaaaababaabbbaababbbabbb", "..."),
                          ("abaabbbbabbb", ".b."),
                          ("aaaaab", "aa."),
                          ("aababb", "a.b"),
                          ("b.ab.b", "b.."),
                          ):
        assert key in simp.seen[3], f"{key} not in {simp.seen[3]}"
        assert simp.seen[3][key] == expected, f"{simp.seen[3][key]} not equal to {expected}"


# def test_simplify():
#     simp = Simplifier()
#     for given, expected in (
#                             (["a", "b"], ["."]),
#                             (["aa", "ab", "ba", "bb"], [".."]),
#                             (["ba", "bb"], ["b."]),
#                             (["ba", "bb"], ["b."]),
#                             # Two patterns should be found
#                             (["ba", "bb", "aa"], ["b.", ".a"]),
#                             (["aba", "abb", "bbb"], ["ab.", ".bb"]),
#                             # Nothing should be substituted
#                             (["ab", "ba"], ["ab", "ba"]),
#                             # Only some things should be substituted
#                             (["aba", "abb", "baa"], ["ab.", "baa"]),
#                             # The more expansive substitution should dominate
#                             (["aba", "abb", "bba", "bbb", "aaa"], ["a.a", ".b."]),
#                             # Overlapping wilds should be merged
#                             (["abaa.b", "abaa.a"], ["abaa.."]),
#                             (["a.a", "a.."], ["a.."]),
#                             ):
#         answer = sorted(simp.simplify(given))
#         expected = sorted(expected)
#         assert answer == expected, f"{answer} didn't match {expected}"
