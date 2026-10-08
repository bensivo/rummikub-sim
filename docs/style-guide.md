# Style Guide

Derived from the author's code as it stands today. The reference files are
`src/rummikub_sim/core/find_runs.py` and `tests/rummikub_sim/core/test_find_runs.py`; when in doubt, imitate them.

## Source code

### Structure

- One public function per module at the top (e.g. `find_runs`), followed by private helpers (`_leading_underscore`)
  **in the order they are called**. The top function reads as a short, high-level outline of the algorithm:

  ```python
  def find_runs(tiles):
      tile_map = _build_tile_map(tiles)

      three_runs = _find_three_runs(tile_map)
      extended_runs = []
      for run in three_runs:
          extended_runs.extend(
              _extend_run(run, tile_map)
          )

      return three_runs + extended_runs
  ```

- Break the problem into small named steps: build a lookup structure, generate candidates, filter, extend.
- Plain functions and simple data (lists, dicts of `Tile`). No classes unless there is state (`Game`, `Player`, `Tile`).
- Simple, loop-based code over clever one-liners. Use `all(...)` / comprehensions only where they read naturally.
- Prefer lookup maps (`tile_map[color][number]`) over repeated scanning.
- Use recursion when it expresses the problem (`_extend_run` calls itself on each extension).
- Don't mutate inputs; copy first (`run.copy() + [next_tile]`).
- Early-return for edge cases, with a comment saying why (`# Can't extend past 13 ...`).
- Raise `ValueError` with a short message for impossible states.
- Import the specific names needed: `from rummikub_sim.core.serialization import set_to_str`.
- Two spaces before inline comments are fine, but keep them short.

### Docstrings

Every function gets a triple-quote docstring, opening and closing `"""` on their own lines.

- Public functions and functions with real inputs/outputs use the **Parameters / Returns** format, with types in parens:

  ```python
  """
  Find all the possible runs (3 or more consecutive numbers of the same color)
  contained in the tiles given

  Parameters:
      tiles (list of Tile): The list of tiles to search for runs in.

  Returns:
      list of list of Tile: A list of all the runs found in the input tiles.
  """
  ```

- Describe data structures with the shape spelled out: `a dict built such that: tile_map[color][number] = Tile`.
- Tiny or obvious helpers can use a one/two-sentence docstring, optionally with an `Example:` line:
  `Example: _slot_value([r1,r2,rJ], 2) would return 3, because the J is acting as a 3 here.`
- Docstrings say *what and why*, in plain English with domain terms (run, set, joker, meld).

### Comments

- Comment the **intent** of each block, in a sentence, on the line above it
  (`# Look for jokers in the hand`, `# Only keep the runs where each tile is not null ...`).
- Explain domain rules and non-obvious edge cases in comments (e.g. why a joker in slot 14 is invalid).
- Use `NOTE:` for caveats on data (`# NOTE: if joker, number should be -1`) and `TODO:` for known improvements,
  ideally with a concrete counter-example.
- Comments are full sentences, normally capitalized.

### Naming

- `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE` for constants.
- Descriptive, domain-based names: `three_runs`, `extended_runs`, `potential_runs`, `last_value`, `next_tile`, `red_joker`.
- Names of sets of tiles are plural (`tiles`, `runs`); a single one is singular (`run`, `tile`).
- Tile string notation (`r2`, `bJ`, `[r2,r3,rJ]`) is used for examples in docs, comments, and tests.

### Formatting

- 4-space indents, blank line between logical steps inside a function.
- Top-level functions are separated by one blank line (existing files vary between 1 and 2; prefer 2 per PEP 8 in new code).
- No type hints currently; types are documented in docstrings.

## Tests

Follow `test_find_runs.py`.

- File path mirrors the source path: `src/rummikub_sim/core/find_runs.py` -> `tests/rummikub_sim/core/test_find_runs.py`.
- Plain pytest functions; no classes, no fixtures unless needed.
- Test names: `test__<function>__<behavior>` with double underscores, snake_case behavior
  (`test__find_runs__handles_jokers`, `test__find_runs__extends_run_ending_in_joker`).
- Every test body is split by **Given / When / Then** comments, each a full sentence describing the scenario:

  ```python
  def test__find_runs__with_overlapping():
      # Given: 2 overlapping runs in the same hand
      tiles = set_from_str("[r2,r3,r4,r5]")

      # When: We call find_runs
      runs = find_runs(tiles)
      runs_str = [set_to_str(run) for run in runs]

      # Then: All options are identified
      assert len(runs) == 3
      assert "[r2,r3,r4]" in runs_str
      assert "[r3,r4,r5]" in runs_str
      assert "[r2,r3,r4,r5]" in runs_str
  ```

- Build input with `set_from_str("[...]")` and compare via `set_to_str` strings, so assertions are readable tile notation
  rather than object comparisons.
- Assert the count (`len(runs) == N`) **and** each expected item with `in` / `not in`. Assert the negative case
  when a rule forbids something (`"[r12,r13,rJ]" not in runs_str`).
- When listing many expected results, add a trailing comment naming each (`# j23`, `# 2j4`).
- For regression tests of subtle bugs, put a `# note:` at the top of the test explaining what the bug was and why it happened,
  before the Given.
- Keep one scenario per test; add a new test for each new rule/edge case (jokers, boundary of 13, overlapping, multiples).
- Shared setup helpers go at the bottom of the file with a docstring (`make_game_with_hand` in `test_player.py`).
