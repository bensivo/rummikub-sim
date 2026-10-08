# Project Overview

`rummikub-sim` is a Python simulator of Rummikub, built to test different game strategies against each other.
Simulated players take turns on a shared board until the game ends; the goal is to make the player's decision logic
swappable so strategies can be compared.

## Status

Early / work in progress. Currently implemented:

- A 106-tile deck: 2 copies of numbers 1-13 in 4 colors, plus 2 jokers (red and black). Shuffled, 14 tiles dealt per player.
- Finding every valid **run** and **set** in a hand (jokers supported).
- Turn loop: a player plays moves until none are left, and draws a tile only if they played nothing.
- **Initial meld** rule: a player's first play must total 30+ points (`INITIAL_MELD_MIN_POINTS`).
- A greedy initial-meld planner (known to be suboptimal, see the TODO in `Player.plan_initial_meld`).
- Rearranging the board: after the initial meld, a player can take tiles from board melds (split runs, free jokers, etc.) as long as the board stays valid. The player greedily picks the rearrangement that plays the most hand tiles.

Not yet implemented (as of writing): a win condition or game end,
scoring across games, pluggable strategies, and running many games for statistics.

## Domain vocabulary

- **Tile**: has a `color` (`black`, `red`, `blue`, `orange`) and a `number` (1-13). Jokers have `is_joker=True`, `number=-1`
  and a color of `black` or `red`.
- **Run**: 3+ consecutive numbers of the same color (e.g. `[r2,r3,r4]`). Max number is 13; no wrap-around.
- **Set**: 3 or 4 tiles of the same number, each a different color (e.g. `[r5,b5,o5]`).
- **Move**: one run or set a player puts on the board (a `list` of `Tile`).
- **Board**: `game.board`, a list of moves.
- **Meld / initial meld**: the first play of the game for a player; must be worth 30+ points.
- **Tick**: one player's turn (`Game.tick`).

## Tile string notation

Used in tests and logs. Color codes: `b` black, `r` red, `u` blue, `o` orange. Joker is `J`.

- `r12` = red 12, `bJ` = black joker.
- A set of tiles is `[r2,r3,rJ]`; brackets are optional when parsing.
- Convert with `set_from_str` / `set_to_str` in `core/serialization.py`.

## Tooling

- Python >= 3.13, managed with `uv` (`uv.lock`, `uv_build` backend).
- Tests: `pytest` (`uv run pytest`).
- Demo: `uv run python src/main.py` plays 20 ticks between two players and prints each draw/play.
