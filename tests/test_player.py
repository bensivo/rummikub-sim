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

