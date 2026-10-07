from rummikub_sim.core.serialization import set_to_str

def find_runs(tiles):
    """
    Find all the possible runs (3 or more consecutive numbers of the same color)
    contained in the tiles given

    Parameters:
        tiles (list of Tile): The list of tiles to search for runs in.

    Returns:
        list of list of Tile: A list of all the runs found in the input tiles.
    """
    tile_map = _build_tile_map(tiles)

    three_runs = _find_three_runs(tile_map)
    extended_runs = []
    for run in three_runs:
        extended_runs.extend(
            _extend_run(run, tile_map)
        )

    return three_runs + extended_runs

def _build_tile_map(tiles):
    """
    Build a map of tiles by color and number from the given list of tiles.
    Used as a quickly-accessed lookup structure for finding runs. 

    Parameters:
        tiles (list of Tile): The list of tiles to map.

    Returns:
        a dict built such that: tile_map[color][number] = Tile
    """
    tile_map = {}
    for tile in tiles:
        tile_map.setdefault(tile.color, {})

        if tile.is_joker:
            tile_map[tile.color].setdefault("J", tile)
        else:
            tile_map[tile.color].setdefault(tile.number, tile)

    return tile_map

def _find_three_runs(tile_map):
    """
    Find all the possible 3-wide runs (3 consecutive numbers of the same color)
    contained in the tile map given.

    Parameters:
        tile_map (dict of dict of Tile): A map of tiles by color and number.

    Returns:
        list of list of Tile: A list of all the 3-wide runs found in the input tile map.
    """
    runs = []

    # Look for jokers in the hand
    red_joker = tile_map.get("red", {}).get("J")
    black_joker = tile_map.get("black", {}).get("J")

    # For each color, slide a 3-wide window from 1 to 11 (e.g. 123,234,345...), and see if that run can be made 
    # either directly, or using jokers to fill in missing numbers.
    colors = list(tile_map.keys())
    for color in colors:
        for i in range(1, 12):
            potential_runs = []

            first = tile_map[color].get(i)
            second = tile_map[color].get(i+1)
            third = tile_map[color].get(i+2)

            # Generate all the possible 3-wide runs using these 3 tiles
            potential_runs.append([first, second, third])

            if red_joker is not None:
                potential_runs.append([red_joker, second, third])
                potential_runs.append([first, red_joker, third])
                potential_runs.append([first, second, red_joker])
            if black_joker is not None:
                potential_runs.append([black_joker, second, third])
                potential_runs.append([first, black_joker, third])
                potential_runs.append([first, second, black_joker])

            # Only keep the runs where each tile is not null (indicating it exists in hand)
            for potential_run in potential_runs:
                if all(tile is not None for tile in potential_run):
                    runs.append(potential_run)

    return runs

def _extend_run(run, tile_map):
    """
    Take the run, and produce any potential extensions of it possible in our tile map
    """
    extended_runs = []
    last_tile = run[-1]
    color = last_tile.color
    last_value = _slot_value(run, len(run) - 1)

    # Can't extend past 13 (this also covers a joker sitting in the 13 slot)
    if last_value >= 13:
        return []

    # See if we can extend the run with the next tile of the same color
    next_tile = tile_map[color].get(last_value + 1)
    if next_tile is not None:
        extended_runs.append(run.copy() + [next_tile])

    # See if we have any jokers available to just add to the end
    red_joker = tile_map.get("red", {}).get("J")
    black_joker = tile_map.get("black", {}).get("J")

    for joker in (red_joker, black_joker):
        if joker is not None and joker not in run:
            extended_runs.append(run.copy() + [joker])

    # Recursively extend each of the new runs
    for extended_run in list(extended_runs):
        extended_runs.extend(_extend_run(extended_run, tile_map))

    return extended_runs


def _slot_value(run, index):
    """
    Get the number a tile occupies in the run. Jokers have no number of their own,
    so their value is inferred from the nearest real tile in the run.

    Example: _slot_value([r1,r2,rJ], 2) would return 3, because the J is acting as a 3 here.
    """
    for i, tile in enumerate(run):
        if not tile.is_joker:
            return tile.number + (index - i)
    raise ValueError("run contains only jokers")
