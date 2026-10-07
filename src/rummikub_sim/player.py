import random

from rummikub_sim.core.find_runs import find_runs
from rummikub_sim.core.find_sets import find_sets
from rummikub_sim.core.serialization import set_to_str


class Player:
    """
    An instance of a player in a game of rummikub, with its own hand and score.
    """

    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_tile(self, game):
        """
        Draw a tile from the game's draw pile and add it to the player's hand.
        """
        tile = game.draw_pile.pop()
        print(f"{self.name}: drew a {tile}")
        self.hand.append(tile)

    def play_turn(self, game):
        """
        Play a turn for the player, which may include drawing a tile and playing tiles on the board.
        """
        played_any = False

        # Keep playing moves until there is nothing left to play
        while True:
            potential_moves = self.find_potential_moves(game)

            if len(potential_moves) == 0:
                break

            # TODO: intelligently choose which hand to play

            move = random.choice(potential_moves)
            print(f"{self.name}: played {set_to_str(move)}")

            game.board.append(move)
            for tile in move:
                self.hand.remove(tile)
            played_any = True

        # Only draw if the player couldn't play anything this turn
        if not played_any:
            self.draw_tile(game)

    def find_potential_moves(self, game):
        """
        Find all potential moves that the player can play from their current hand, given the state of the game board.
        """
        potential_hands = []

        runs = find_runs(self.hand)
        potential_hands.extend(runs)

        sets = find_sets(self.hand)
        potential_hands.extend(sets)

        return potential_hands
