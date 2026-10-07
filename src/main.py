from rummikub_sim import Game, Player, Tile

if __name__ == '__main__':
    player1 = Player("Ben")
    # player2 = Player("Austin")

    game = Game(players=[
        player1,
        # player2
    ])

    game.setup_game()

    print(f"Game setup complete. Game starting with {game.players[game.current_player_index].name}")

    for _ in range(10):
        game.tick()

