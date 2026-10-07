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
    # extended_runs = _extend_three_runs(three_runs, tile_map)
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

            # Add any runs which don't have nulls (indicating that tile is not in hand)
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

    if last_tile.number == 13:
        return []

    # See if we can extend the run with the next consecutive tile of the same color
    next_tile = tile_map[color].get(last_tile.number + 1)
    if next_tile is not None:
        extended_runs.append(run.copy() + [next_tile])

    # See if we have any jokers available to just add to the end
    red_joker = tile_map.get("red", {}).get("J")
    black_joker = tile_map.get("black", {}).get("J")
    red_joker_available = red_joker is not None and red_joker not in run
    black_joker_available = black_joker is not None and black_joker not in run

    if red_joker_available:
        extension = run.copy() + [red_joker]
        # Double check that the extension doesn't put the joker past the "13" spot
        if extension[-2].number <= 12 or extension[-3].number <= 11:
            extended_runs.append(extension)

    if black_joker_available:
        extension = run.copy() + [black_joker]

        # Double check that the extension doesn't put the joker past the "13" spot
        if extension[-2].number <= 12 or extension[-3].number <= 11:
            extended_runs.append(extension)

    # Recursively call extend run again, to find all possible extensions
    for extended_run in extended_runs:
        extended_runs.extend(_extend_run(extended_run, tile_map))

    return extended_runs

