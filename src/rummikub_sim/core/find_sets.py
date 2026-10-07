from itertools import combinations

def find_sets(tiles):
    """
    Find all the possible sets (3 or 4 tiles of the same number, each a different color)
    contained in the tiles given

    Parameters:
        tiles (list of Tile): The list of tiles to search for sets in.

    Returns:
        list of list of Tile: A list of all the sets found in the input tiles.
    """
    tile_map = _build_tile_map(tiles)
    jokers = _find_jokers(tiles)

    sets = []
    for number in range(1, 14):
        sets.extend(_find_sets_for_number(tile_map.get(number, {}), jokers))

    return sets

def _build_tile_map(tiles):
    """
    Build a map of tiles by number and color from the given list of tiles.
    Used as a quickly-accessed lookup structure for finding sets.
    Jokers are not included, since they have no number of their own.

    Parameters:
        tiles (list of Tile): The list of tiles to map.

    Returns:
        a dict built such that: tile_map[number][color] = Tile
    """
    tile_map = {}
    for tile in tiles:
        if tile.is_joker:
            continue
        tile_map.setdefault(tile.number, {})
        tile_map[tile.number].setdefault(tile.color, tile)

    return tile_map

def _find_jokers(tiles):
    """
    Find the jokers in the hand, at most one per color.
    """
    jokers = {}
    for tile in tiles:
        if tile.is_joker:
            jokers.setdefault(tile.color, tile)

    return list(jokers.values())

def _find_sets_for_number(color_map, jokers):
    """
    Find all the 3 or 4 wide sets for a single number.

    Parameters:
        color_map (dict of Tile): The tiles of this number, by color.
        jokers (list of Tile): The jokers available to fill in missing colors.

    Returns:
        list of list of Tile: A list of all the sets found for this number.
    """
    sets = []
    real_tiles = list(color_map.values())

    # Pick 2 to 4 real tiles of different colors, then fill the rest of the set with jokers
    # to reach a size of 3 or 4. Jokers always go at the end, since order doesn't matter in a set.
    for num_real in range(2, 5):
        for real in combinations(real_tiles, num_real):
            for size in (3, 4):
                num_jokers = size - num_real
                if num_jokers < 0 or num_jokers > len(jokers):
                    continue
                for joker_combo in combinations(jokers, num_jokers):
                    sets.append(list(real) + list(joker_combo))

    return sets
