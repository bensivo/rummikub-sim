from rummikub_sim import Game, Player

def test_game_setup():

    # Given a game with 2 players
    player1 = Player("Ben")
    player2 = Player("Austin")
    game = Game(players=[player1, player2])

    # When setup() is called
    game.setup_game()

    # Then each player should have 14 tiles in their hand
    assert len(player1.hand) == 14
    assert len(player2.hand) == 14

    # Then the draw_pile should have 78 tiles remaining
    assert len(game.draw_pile) == 78


