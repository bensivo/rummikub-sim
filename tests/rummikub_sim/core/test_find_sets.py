from rummikub_sim.core.find_sets import find_sets
from rummikub_sim.core.serialization import set_from_str, set_to_str


def test__find_sets__basic():
    # Given: A list of tiles forming a basic set
    tiles = set_from_str("[r2,b2,u2]")

    # When: We call find_sets
    sets = find_sets(tiles)
    sets_str = [set_to_str(s) for s in sets]

    # Then: The set is returned
    assert sets_str == ["[r2,b2,u2]"]


def test__find_sets__multiple_sets():
    # Given: 2 sets of different numbers in the same tiles
    tiles = set_from_str("[r2,b2,u2,r5,b5,o5]")

    # When: We call find_sets
    sets = find_sets(tiles)
    sets_str = [set_to_str(s) for s in sets]

    # Then: both sets are identified
    assert len(sets) == 2
    assert "[r2,b2,u2]" in sets_str
    assert "[r5,b5,o5]" in sets_str


def test__find_sets__with_overlapping():
    # Given: 4 colors of the same number
    tiles = set_from_str("[r2,b2,u2,o2]")

    # When: We call find_sets
    sets = find_sets(tiles)
    sets_str = [set_to_str(s) for s in sets]

    # Then: all four 3-wide sets, plus the 4-wide set are identified
    assert len(sets) == 5
    assert "[r2,b2,u2]" in sets_str
    assert "[r2,b2,o2]" in sets_str
    assert "[r2,u2,o2]" in sets_str
    assert "[b2,u2,o2]" in sets_str
    assert "[r2,b2,u2,o2]" in sets_str


def test__find_sets__ignores_same_color():
    # Given: 3 tiles with the same number, but only 2 colors
    tiles = set_from_str("[r2,r2,b2]")

    # When: We call find_sets
    sets = find_sets(tiles)

    # Then: no sets are found
    assert sets == []


def test__find_sets__handles_jokers():
    # Given: 2 tiles of a set with 1 joker
    tiles = set_from_str("[r2,b2,rJ]")

    # When: We call find_sets
    sets = find_sets(tiles)
    sets_str = [set_to_str(s) for s in sets]

    # Then: The set is returned with the joker
    assert sets_str == ["[r2,b2,rJ]"]


def test__find_sets__jokers_extend_to_four():
    # Given: 3 tiles of a set with 1 joker
    tiles = set_from_str("[r2,b2,u2,rJ]")

    # When: We call find_sets
    sets = find_sets(tiles)
    sets_str = [set_to_str(s) for s in sets]

    # Then: the 3-wide set, the 4-wide set using the joker, and the 3-wide sets using the joker are found
    assert len(sets) == 5
    assert "[r2,b2,u2]" in sets_str
    assert "[r2,b2,u2,rJ]" in sets_str
    assert "[r2,b2,rJ]" in sets_str
    assert "[r2,u2,rJ]" in sets_str
    assert "[b2,u2,rJ]" in sets_str
