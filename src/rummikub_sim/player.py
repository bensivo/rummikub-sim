from rummikub_sim.core.find_runs import find_runs
from rummikub_sim.core.find_sets import find_sets
from rummikub_sim.core.find_moves import find_best_move
from rummikub_sim.core.scoring import INITIAL_MELD_MIN_POINTS, set_value
from rummikub_sim.core.serialization import set_to_str


class Player:
    """
    An instance of a player in a game of rummikub, with its own hand and score.
    """

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.has_melded = False  # True once the player has made their initial 30+ point play

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

        # The first play must total at least 30 points, otherwise the player can't play at all
        if not self.has_melded:
            initial_moves = self.plan_initial_meld()
            if len(initial_moves) == 0:
                self.draw_tile(game)
                return

            for meld in initial_moves:
                self.play_meld(game, meld)
            self.has_melded = True
            played_any = True

        # Keep rearranging the board to play tiles from the hand, until there is nothing left to play
        while True:
            move = find_best_move(game.board, self.hand)

            if move is None:
                break

            # TODO: intelligently choose which move to play, instead of the one using the most tiles

            self.play_move(game, move)
            played_any = True

        # Only draw if the player couldn't play anything this turn
        if not played_any:
            self.draw_tile(game)

    def play_meld(self, game, meld):
        """
        Put the tiles of a single meld from the player's hand onto the board.
        """
        print(f"{self.name}: played {set_to_str(meld)}")
        game.board.append(meld)
        for tile in meld:
            self.hand.remove(tile)

    def play_move(self, game, move):
        """
        Replace the board with the rearranged one from the move, and take the tiles it played out of the player's hand.
        """
        new_board, played = move
        print(f"{self.name}: played {set_to_str(played)}, board is now {[set_to_str(meld) for meld in new_board]}")
        game.board = new_board
        for tile in played:
            self.hand.remove(tile)

    def plan_initial_meld(self):
        """
        Find moves from the player's hand that together are worth at least 30 points.
        Greedily takes the highest-value move first. Returns an empty list if 30 can't be reached.
        """
        remaining = list(self.hand)
        planned = []
        total = 0

        while total < INITIAL_MELD_MIN_POINTS:
            moves = find_runs(remaining) + find_sets(remaining)
            if len(moves) == 0:
                return []

            """
            TODO: instead of just using the max value set first, do an exhaustive search of all possible set combos

            Counter-example for the greedy plan_initial_meld():

            r4,r5,r6,r7,u7,o7,u4,o4
                - Best actual play: set [r7,u7,o7] (21) + set [r4,u4,o4] (12) = 33 points
                - Greedy picks the highest-value single move first: [r4,r5,r6,r7] (22)
                - That uses up the r4 and r7 that both sets need, leaving u7,o7,u4,o4. Player would fail to meld
            
            """
            best = max(moves, key=set_value)
            planned.append(best)
            total += set_value(best)
            for tile in best:
                remaining.remove(tile)

        return planned
