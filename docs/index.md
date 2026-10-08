# Codebase Index (where to find what)

See [overview.md](overview.md) for what the project is and [style-guide.md](style-guide.md) for how to write code here.

## Source: `src/`

| File | What's in it |
|------|--------------|
| `src/main.py` | Demo script: 2 players, sets up a game, runs 20 ticks. |
| `src/rummikub_sim/__init__.py` | Public exports: `Game`, `Player`, `Tile`. |
| `src/rummikub_sim/tile.py` | `Tile` class (color, number, `is_joker`; value equality + hash). |
| `src/rummikub_sim/game.py` | `Game`: builds/shuffles the draw pile, deals hands (`setup_game`), advances turns (`tick`). Holds `players`, `board`, `draw_pile`, `current_player_index`. |
| `src/rummikub_sim/player.py` | `Player`: hand, `has_melded`, `draw_tile`, `play_turn` (turn logic), `play_move`, `plan_initial_meld` (greedy 30-pt planner), `find_potential_moves`. **Strategy decisions live here.** |

### Core rules logic: `src/rummikub_sim/core/`

| File | What's in it |
|------|--------------|
| `core/find_runs.py` | `find_runs(tiles)`: every valid run in a hand, with jokers. Helpers: `_build_tile_map`, `_find_three_runs`, `_extend_run`, `_slot_value` (the number a tile occupies in a run, inferring jokers). |
| `core/find_sets.py` | `find_sets(tiles)`: every valid 3/4-tile set, with jokers. Helpers: `_build_tile_map`, `_find_jokers`, `_find_sets_for_number`. |
| `core/scoring.py` | `set_value(tiles)` point value of a run/set; `INITIAL_MELD_MIN_POINTS = 30`. Imports `_slot_value` from `find_runs`. |
| `core/serialization.py` | `set_from_str` / `set_to_str`: tile-string notation (`"[r2,r3,rJ]"`) <-> `list[Tile]`. |

## Tests: `tests/`

Mirror the `src/` layout.

| File | Covers |
|------|--------|
| `tests/rummikub_sim/core/test_find_runs.py` | `find_runs`: basic, multiple, overlapping, jokers, joker over 13, extension bug. |
| `tests/rummikub_sim/core/test_find_sets.py` | `find_sets`. |
| `tests/test_player.py` | Turn logic: drawing, playing sets, initial meld. Has the `make_game_with_hand` helper at the bottom. |
| `tests/test_game.py` | Game setup (14 tiles per hand, 78 left in the pile for 2 players). |

## Config / misc

- `pyproject.toml`: project metadata, `pytest` dependency, `uv_build` backend.
- `.python-version`, `uv.lock`: Python/uv pinning.

## "I want to..." quick lookup

- Change what counts as a valid run -> `core/find_runs.py` (+ `test_find_runs.py`)
- Change what counts as a valid set -> `core/find_sets.py`
- Change how a player picks moves -> `player.py` (`play_turn`, `find_potential_moves`, `plan_initial_meld`)
- Change deck contents or dealing -> `game.py` (`setup_game`)
- Change point values or meld minimum -> `core/scoring.py`
- Write a hand for a test -> `set_from_str("[r2,r3,r4]")`, or `make_game_with_hand` in `test_player.py`
