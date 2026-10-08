from rummikub_sim.core.find_runs import _slot_value

INITIAL_MELD_MIN_POINTS = 30


def set_value(tiles):
    """
    Point value of a valid run or set. Jokers are worth the tile they stand in for.

    Example: [r10,u10,o10] is 30, and [r1,r2,rJ] is 6.
    """
    real_numbers = {tile.number for tile in tiles if not tile.is_joker}

    # A group of tiles sharing one number is a set; otherwise it's a run
    if len(real_numbers) == 1:
        return real_numbers.pop() * len(tiles)

    return sum(_slot_value(tiles, i) for i in range(len(tiles)))
