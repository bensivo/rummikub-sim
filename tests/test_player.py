from rummikub_sim import Game, Player
from rummikub_sim.core.serialization import set_from_str, set_to_str


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


def test_play_turn_plays_set():
    # Given a player with a set in their hand (r10,u10,o10)
    game, player = make_game_with_hand("r10,u10,o10")

    # When the player takes their turn
    player.play_turn(game)

    # Then they will play that set
    assert len(game.board) == 1
    assert sorted(set_to_str(game.board[0])) == sorted(set_to_str(set_from_str("r10,u10,o10")))
    assert player.hand == []

    # Then they do not draw a tile
    assert len(game.draw_pile) == 1


def test_play_turn_draws_when_no_valid_moves():
    # Given a player in a game, who has no valid moves in their hand
    game, player = make_game_with_hand("b1,r5,u9,o12", draw_pile_str="b13")

    # When the player takes their turn
    player.play_turn(game)

    # Then they will draw a tile
    assert len(player.hand) == 5
    assert set_from_str("b13")[0] in player.hand
    assert len(game.draw_pile) == 0
    assert game.board == []


def test_play_turn_initial_meld_under_30_draws():
    # Given a player who hasn't played yet, with a set worth only 15 points (r5,u5,o5)
    game, player = make_game_with_hand("r5,u5,o5", draw_pile_str="b1")

    # When the player takes their turn
    player.play_turn(game)

    # Then they can't play it, and draw a tile instead
    assert game.board == []
    assert len(player.hand) == 4
    assert player.has_melded is False


def test_play_turn_initial_meld_combines_sets_to_reach_30():
    # Given a player who hasn't played yet, with two sets worth 15 and 18 points
    game, player = make_game_with_hand("r5,u5,o5,b6,r6,u6")

    # When the player takes their turn
    player.play_turn(game)

    # Then they play both sets, since together they pass 30
    assert len(game.board) == 2
    assert player.hand == []
    assert player.has_melded is True


def test_play_turn_after_initial_meld_has_no_minimum():
    # Given a player who has already made their initial play, with a low-value set
    game, player = make_game_with_hand("r5,u5,o5")
    player.has_melded = True

    # When the player takes their turn
    player.play_turn(game)

    # Then they play it
    assert len(game.board) == 1
    assert player.hand == []


def test_play_turn_takes_tiles_from_board():
    # Given: a player who has already melded, with 2 tiles that make a set with the 4 in the middle of a run on the board
    game, player = make_game_with_hand("b4,o4")
    player.has_melded = True
    game.board = [set_from_str("[r1,r2,r3,r4,r5,r6,r7]")]

    # When: the player takes their turn
    player.play_turn(game)

    # Then: they split the run to take the 4, and play their whole hand
    assert player.hand == []
    assert len(game.board) == 3
    assert sum(len(meld) for meld in game.board) == 9

    # Then: they do not draw a tile
    assert len(game.draw_pile) == 1


def make_game_with_hand(hand_str, draw_pile_str="b1"):
    """
    Build a game with one player holding exactly the given hand (e.g. "r10,u10,o10"),
    an empty board, and a draw pile containing exactly the given tiles (last tile is drawn first).
    """
    player = Player("Ben")
    game = Game(players=[player])
    game.board = []
    game.draw_pile = set_from_str(draw_pile_str)
    player.hand = set_from_str(hand_str)
    return game, player