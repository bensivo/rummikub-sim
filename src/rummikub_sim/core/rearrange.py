from collections import Counter

from rummikub_sim.core.find_runs import find_runs
from rummikub_sim.core.find_sets import find_sets
from rummikub_sim.core.serialization import set_to_str

def best_rearrangement(board, hand):
    """
    Find the rearrangement of the board that plays the most tiles from the hand.
    Ties go to the first one found.

    Parameters:
        board (list of list of Tile): The melds currently on the board.
        hand (list of Tile): The tiles in the player's hand.

    Returns:
        tuple of (new_board, played), or None if no rearrangement plays at least one tile from the hand.
            new_board (list of list of Tile): The melds on the board after the rearrangement.
            played (list of Tile): The tiles from the hand that were put on the board.
    """
    rearrangements = find_rearrangements(board, hand)
    if len(rearrangements) == 0:
        return None

    return max(rearrangements, key=lambda rearrangement: len(rearrangement[1]))

def find_rearrangements(board, hand):
    """
    Find every way to rearrange the board into valid melds, such that every tile currently
    on the board stays on the board, and at least one tile from the hand is added to it.

    Parameters:
        board (list of list of Tile): The melds currently on the board.
        hand (list of Tile): The tiles in the player's hand.

    Returns:
        list of tuple of (new_board, played): All the rearrangements found, where
            new_board (list of list of Tile): The melds on the board after the rearrangement.
            played (list of Tile): The tiles from the hand that were put on the board.
    """
    board_tiles = [tile for meld in board for tile in meld]
    pool = board_tiles + hand

    # Every meld that could be made from the pool. Each is paired with its tile counts,
    # since the pool can hold 2 copies of a tile but a rearrangement can't use more than that.
    candidates = [(meld, Counter(meld)) for meld in find_runs(pool) + find_sets(pool)]

    rearrangements = []
    seen = set()
    for melds in _search(board_tiles, Counter(board_tiles), Counter(pool), candidates, 0, []):
        # The same board can be reached more than once, e.g. by covering a tile with either of its 2 copies
        key = _board_key(melds)
        if key in seen:
            continue
        seen.add(key)

        played = list((Counter(tile for meld in melds for tile in meld) - Counter(board_tiles)).elements())
        if len(played) > 0:
            rearrangements.append((melds, played))

    return rearrangements

def _search(board_tiles, required, available, candidates, start, melds):
    """
    Recursively build boards out of the candidate melds. Works in 2 phases:
        1. Cover every tile that was already on the board, by trying each candidate meld that contains the
           first uncovered tile.
        2. With the board covered, optionally add more melds made from whatever is left over.

    Parameters:
        board_tiles (list of Tile): The tiles that were on the board, used to pick the next uncovered tile.
        required (Counter of Tile): The board tiles which are not in a meld yet.
        available (Counter of Tile): The tiles that are not in a meld yet, from both the board and the hand.
        candidates (list of tuple of (meld, Counter)): Every meld that could be made, with its tile counts.
        start (int): In phase 2, only candidates from this index on are considered, so each combination is only built once.
        melds (list of list of Tile): The melds chosen so far.

    Yields:
        list of list of Tile: Every board which covers all the board tiles.
    """
    if not required:
        yield melds

        for i in range(start, len(candidates)):
            meld, counts = candidates[i]
            if _fits(counts, available):
                yield from _search(board_tiles, required, available - counts, candidates, i + 1, melds + [meld])
        return

    uncovered = next(tile for tile in board_tiles if required[tile] > 0)
    for meld, counts in candidates:
        if uncovered in meld and _fits(counts, available):
            yield from _search(board_tiles, required - counts, available - counts, candidates, start, melds + [meld])

def _fits(counts, available):
    """
    Check if there are enough tiles available to build a meld with the given tile counts.
    """
    return not (counts - available)

def _board_key(melds):
    """
    Build a key which is the same for any 2 boards holding the same melds, regardless of their order.
    """
    return tuple(sorted(set_to_str(meld) for meld in melds))
