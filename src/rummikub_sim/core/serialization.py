from rummikub_sim.tile import Tile


def set_from_str(s):
    """Parse a string like "b1,b2,bJ" (brackets optional) into a list of Tiles. Inverse of print_set."""
    COLOR_CODES = {'b': 'black', 'r': 'red', 'u': 'blue', 'o': 'orange'}
    tiles = []
    for token in s.strip().strip("[]").split(","):
        token = token.strip()
        if not token:
            continue
        color = COLOR_CODES[token[0]]
        if token[1:] == 'J':
            tiles.append(Tile(color, -1, is_joker=True))
        else:
            tiles.append(Tile(color, int(token[1:])))
    return tiles


def set_to_str(tiles):
    s = "["
    for tile in tiles:
        if tile.color == 'black':
            s += 'b'
        elif tile.color == 'red':
            s += 'r'
        elif tile.color == 'blue':
            s += 'u'
        elif tile.color == 'orange':
            s += 'o'

        if tile.is_joker:
            s += 'J'
        else:
            s += str(tile.number)

        s+= ','

    s = s.rstrip(',')  # Remove the trailing comma for cleaner output
    s += "]"
    return s
