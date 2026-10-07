from rummikub_sim import Game, Player
from rummikub_sim.util import set_from_str


def test_draw_tile():
    # Given a player in a game
    player1 = Player("Ben")
    game = Game(players=[player1])
    game.setup_game()

    hand_size_before = len(player1.hand)
    draw_pile_size_before = len(game.draw_pile)

    # When draw_tile() is called
    player1.draw_tile(game)

    # Then the player gets 1 more tile
    assert len(player1.hand) == hand_size_before + 1

    # Then the game's draw-pile has 1 less tile
    assert len(game.draw_pile) == draw_pile_size_before - 1


def test_find_potential_hands__single_run():
    # Given a player with a hand containing a single run (e.g. black 1,2,3)
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,b2,b3")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the player's potential hands include the existing run
    assert set_from_str("b1,b2,b3") in potential_hands


def test_find_potential_hands__multiple_runs():
    # Given a player with a hand containing a multiple runs (e.g. black 1,2,3, red 1,2,3)
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,b2,b3,r1,r2,r3")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the player's potential hands include the existing runs
    assert set_from_str("b1,b2,b3") in potential_hands
    assert set_from_str("r1,r2,r3") in potential_hands


def test_find_potential_hands__overlapping_runs():
    # Given a player with a hand containing a 3+ run (b1,b2,b3,b4)
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,b2,b3,b4")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the player's potential hands include the full run and each shorter overlapping run
    assert set_from_str("b1,b2,b3,b4") in potential_hands
    assert set_from_str("b1,b2,b3") in potential_hands
    assert set_from_str("b2,b3,b4") in potential_hands


def test_find_potential_hands__no_runs():
    # Given a player with a hand containing no valid runs (e.g. black 1, red 2)
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,r2")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the player's potential hands include no runs
    assert len(potential_hands) == 0


def test_find_potential_hands__single_joker():
    # Given a player with 2 tiles of a run, plus a joker
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,b2,bJ")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the joker is considered as part of the potential run
    assert set_from_str("b1,b2,bJ") in potential_hands


def test_find_potential_hands__joker_at_either_end():
    # Given a player with b2, b3, and a joker
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b2,b3,bJ")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the joker is used in both the 1 and the 4 positions
    assert set_from_str("bJ,b2,b3") in potential_hands
    assert set_from_str("b2,b3,bJ") in potential_hands


def test_find_potential_hands__two_jokers():
    # Given a player with 1 real tile, plus 2 jokers
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b1,bJ,rJ")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then both jokers are used to extend the run
    assert set_from_str("b1,bJ,rJ") in potential_hands


def test_find_potential_hands__two_jokers_in_any_position():
    # Given a player with 1 real tile in the middle of the board, plus 2 jokers
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("bJ,b5,rJ")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the jokers can both be before the tile, split around it, or both after it
    assert set_from_str("bJ,rJ,b5") in potential_hands
    assert set_from_str("bJ,b5,rJ") in potential_hands
    assert set_from_str("b5,bJ,rJ") in potential_hands


def test_find_potential_hands__joker_with_existing_run():
    # Given a player with a run b2,b3,b4 plus a joker
    player1 = Player("Ben")
    game = Game(players=[player1])
    player1.hand = set_from_str("b2,b3,b4,bJ")

    # When find_potential_hands() is called
    potential_hands = player1.find_potential_hands(game)

    # Then the potential hands include the joker at either end, or replacing any single tile
    expected = [
        "b2,b3,b4",  # not using joker
        "bJ,b2,b3,b4",  # joker at front
        "b2,b3,b4,bJ",  # joker at end
        "bJ,b2,b3",  # joker at front, leaving out b4
        "b3,b4,bJ",  # joker at end, leaving out b2
        "bJ,b3,b4",  # joker replacing b2
        "b2,bJ,b4",  # joker replacing b3
        "b2,b3,bJ",  # joker replacing b4
    ]
    for s in expected:
        assert set_from_str(s) in potential_hands
    assert len(potential_hands) == len(expected)
