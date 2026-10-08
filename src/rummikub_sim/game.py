import random

from rummikub_sim.tile import Tile
from rummikub_sim.core.serialization import set_to_str


class Game:
    """
    An instance of a single game of rummikub being played, with its own internal state, players, and game progress.
    """

    # Variables that hold game state, including all the tiles on the board, in players hands, in the draw-pile, and any other relevant game information.
    players = []
    board = []
    current_player_index = 0  # Index indicating which player's turn it is

    def __init__(self, players):
        self.players = players

    def setup_game(self):
        """
        Set up the game, giving each player their initial hand of 14 random tiles.
        """
        self.board = []
        self.draw_pile = []
        self.draw_pile.extend([Tile(color, number) for number in range(1, 14) for color in ["black", "red", "blue", "orange"]])
        self.draw_pile.extend([Tile(color, number) for number in range(1, 14) for color in ["black", "red", "blue", "orange"]])
        self.draw_pile.extend([
            Tile("black", -1, is_joker=True),
            Tile("red", -1, is_joker=True),
        ])

        random.shuffle(self.draw_pile)

        for player in self.players:
            for _ in range(14):
                player.draw_tile(self)

    def tick(self):
        """
        Advance the game by one turn, updating the game state accordingly.
        """

        print(f"Board: {board_to_strs(self.board)}")

        current_player = self.players[self.current_player_index]
        current_player.play_turn(self)

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

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
