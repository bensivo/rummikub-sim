import itertools


from rummikub_sim.util import print_set, set_str


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
        print(f"  {set_str(self.hand)}")
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
                print_set(hand)

            # For now, we just print the potential hands for debugging purposes.
            # In a real implementation, the player would choose one of these hands to play.

    def find_potential_hands(self, game):
        """
        Find all potential hands that the player can play from their current hand, given the state of the game board.
        """
        potential_hands = []

        # Find all potential runs within the player's hand.
        # By organizing by color, sorting, then iterating in order.
        jokers = [tile for tile in self.hand if tile.is_joker]

        tiles_by_color = {}
        for tile in self.hand:
            if not tile.is_joker:
                tiles_by_color.setdefault(tile.color, {}).setdefault(tile.number, tile)  # dedupe same color/number

        # Every window of consecutive numbers (length >= 3) is a candidate run. Numbers the player
        # doesn't hold must be filled by jokers. Spare jokers may also replace held tiles.
        # Each run must contain at least one real tile.
        for tile_by_number in tiles_by_color.values():
            for low in range(1, 14):
                for high in range(low + 2, 14):
                    window = range(low, high + 1)
                    missing = [n for n in window if n not in tile_by_number]
                    held = [n for n in window if n in tile_by_number]
                    spare = len(jokers) - len(missing)
                    if spare < 0 or not held:
                        continue

                    for num_replaced in range(0, min(spare, len(held) - 1) + 1):
                        for replaced in itertools.combinations(held, num_replaced):
                            joker_numbers = set(missing) | set(replaced)
                            joker_iter = iter(jokers)
                            potential_hands.append([next(joker_iter) if n in joker_numbers else tile_by_number[n] for n in window])

        return potential_hands
