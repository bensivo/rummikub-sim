from rummikub_sim.core.find_moves import find_best_move, find_moves
from rummikub_sim.core.serialization import set_from_str, set_to_str


def test__find_moves__extends_run():
    # Given: a board with a run, and a hand with the next tile in the run
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[r5]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: The only option is to extend the run
    assert len(moves) == 1
    new_board, played = moves[0]
    assert board_to_strs(new_board) == ["[r2,r3,r4,r5]"]
    assert set_to_str(played) == "[r5]"


def test__find_moves__extends_set():
    # Given: a board with a 3-tile set, and a hand with the missing color
    board = [set_from_str("[r2,b2,u2]")]
    hand = set_from_str("[o2]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: The only option is to make it a 4-tile set
    assert len(moves) == 1
    new_board, played = moves[0]
    assert board_to_strs(new_board) == ["[b2,u2,o2,r2]"]
    assert set_to_str(played) == "[o2]"


def test__find_moves__splits_run():
    # Given: a long run on the board, and 2 tiles in hand which make a set with one tile from the middle of the run
    board = [set_from_str("[r1,r2,r3,r4,r5,r6,r7]")]
    hand = set_from_str("[b4,o4]")

    # When: We call find_moves
    moves = find_moves(board, hand)
    boards_str = [board_to_strs(new_board) for new_board, _ in moves]

    # Then: The run is split around the 4, and the 4 is moved into a new set
    assert ["[b4,o4,r4]", "[r1,r2,r3]", "[r5,r6,r7]"] in boards_str


def test__find_moves__returns_every_option():
    # Given: a board with a run, and a hand which could extend it by 1, 2, or 3 tiles, or form a run of its own
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[r5,r6,r7]")

    # When: We call find_moves
    moves = find_moves(board, hand)
    boards_str = [board_to_strs(new_board) for new_board, _ in moves]

    # Then: Every option is found, since tiles in hand are optional
    assert len(moves) == 4
    assert ["[r2,r3,r4,r5]"] in boards_str
    assert ["[r2,r3,r4,r5,r6]"] in boards_str
    assert ["[r2,r3,r4,r5,r6,r7]"] in boards_str
    assert ["[r2,r3,r4]", "[r5,r6,r7]"] in boards_str


def test__find_moves__frees_joker():
    # Given: a board with a joker standing in for a 4, and the real 4 in hand
    board = [set_from_str("[r2,r3,rJ]"), set_from_str("[b5,b6,b7]")]
    hand = set_from_str("[r4]")

    # When: We call find_moves
    moves = find_moves(board, hand)
    boards_str = [board_to_strs(new_board) for new_board, _ in moves]

    # Then: The 4 replaces the joker, and the joker is reused to extend the other run, at either end
    assert ["[b5,b6,b7,rJ]", "[r2,r3,r4]"] in boards_str
    assert ["[r2,r3,r4]", "[rJ,b5,b6,b7]"] in boards_str


def test__find_moves__uses_both_copies_of_a_tile():
    # Given: a board with a run, and a hand with an identical run (2 copies of each tile)
    board = [set_from_str("[r3,r4,r5]")]
    hand = set_from_str("[r3,r4,r5]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: Both runs end up on the board
    assert len(moves) == 1
    new_board, played = moves[0]
    assert board_to_strs(new_board) == ["[r3,r4,r5]", "[r3,r4,r5]"]
    assert len(played) == 3


def test__find_moves__no_options():
    # Given: a hand with nothing that can join the board
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[b1,o9]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: There are none
    assert moves == []


def test__find_moves__requires_playing_a_tile():
    # Given: a valid board, and a hand which can't be played
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[b9]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: The unchanged board is not returned as an option
    assert moves == []


def test__find_moves__empty_board():
    # Given: an empty board, and a hand with a set
    board = []
    hand = set_from_str("[r5,b5,o5]")

    # When: We call find_moves
    moves = find_moves(board, hand)

    # Then: The set is played on its own
    assert len(moves) == 1
    new_board, played = moves[0]
    assert board_to_strs(new_board) == ["[b5,o5,r5]"]
    assert len(played) == 3


def test__find_best_move__most_tiles_from_hand():
    # Given: a hand where one option plays 1 tile, and another plays 3
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[r5,b9,o9,u9]")

    # When: We call find_best_move
    new_board, played = find_best_move(board, hand)

    # Then: The option which plays the most tiles is chosen, which is both together
    assert len(played) == 4
    assert board_to_strs(new_board) == ["[b9,u9,o9]", "[r2,r3,r4,r5]"]


def test__find_best_move__none_when_no_options():
    # Given: a hand with nothing that can be played
    board = [set_from_str("[r2,r3,r4]")]
    hand = set_from_str("[b1]")

    # When: We call find_best_move
    result = find_best_move(board, hand)

    # Then: There is nothing to return
    assert result is None


def board_to_strs(board):
    """
    Turn a board into a sorted list of strings like ["[r1,r2,r3]", "[b5,o5,r5]"], so tests can compare
    boards without caring about the order of the melds. Tiles in a set are sorted by color, since their
    order doesn't matter, but tiles in a run keep their order, since that is where the jokers are.
    """
    melds = []
    for meld in board:
        numbers = {tile.number for tile in meld if not tile.is_joker}
        if len(numbers) == 1:
            meld = sorted(meld, key=lambda tile: tile.color)
        melds.append(set_to_str(meld))

    return sorted(melds)
