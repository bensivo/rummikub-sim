class Tile:
    """
    An instance of a tile in the game of rummikub, with its own number and color.
    """

    def __init__(self, color, number, is_joker = False):
        self.number = number  # NOTE: if joker, number should be -1
        self.color = color  # NOTE: if joker, color should be "black" or "red"
        self.is_joker = is_joker

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return NotImplemented
        return (self.color, self.number, self.is_joker) == (other.color, other.number, other.is_joker)

    def __hash__(self):
        return hash((self.color, self.number, self.is_joker))

    def __str__(self):
        if self.is_joker:
            return f"{self.color} Joker"
        return f"{self.color} {self.number}"
