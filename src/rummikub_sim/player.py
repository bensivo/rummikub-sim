from rummikub_sim.core.find_runs import find_runs
from rummikub_sim.core.serialization import set_to_str


class Player:
    """
    An instance of a player in a game of rummikub, with its own hand and score.
    """

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.has_played_30 = False  # Tracks whether the player has ever played a combination worth 30 points

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
        print(f"{self.name}: starting turn.")
        print(f"  {set_to_str(self.hand)}")
        if not self.has_played_30:
            # The Player has not yet played their initial hand of 30-points in this game
            # They must play only from within their hand to reach the 30-point threshold.

            potential_hands = self.find_potential_hands(game)

            if len(potential_hands) == 0:
                print(f"{self.name}: no potential hands found, drawing a tile.")
                self.draw_tile(game)
                return

            print(f"{self.name}: potential hands to play:")
            for hand in potential_hands:
                print(f"  {set_to_str(hand)}")

            # For now, we just print the potential hands for debugging purposes.
            # In a real implementation, the player would choose one of these hands to play.

    def find_potential_hands(self, game):
        """
        Find all potential hands that the player can play from their current hand, given the state of the game board.
        """
        potential_hands = []

        runs = find_runs(self.hand)
        potential_hands.extend(runs)

        return potential_hands
