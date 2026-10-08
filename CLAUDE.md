# CLAUDE.md

Rummikub simulator in Python (>= 3.13, `uv`, `pytest`). Run tests with `uv run pytest`.

Project docs live in `docs/`. Read them before making changes:

- [docs/overview.md](docs/overview.md): what the project is, current status, Rummikub vocabulary, and tile string notation (`[r2,r3,rJ]`).
- [docs/index.md](docs/index.md): where to find what in the codebase, plus an "I want to..." lookup. Start here to locate code.
- [docs/style-guide.md](docs/style-guide.md): the author's code and test style. Follow it for all new code and tests;
  `core/find_runs.py` and `tests/rummikub_sim/core/test_find_runs.py` are the reference examples.

Keep docs current: if you add, move, or remove files, update `docs/index.md`; if you change the project's capabilities,
update the Status section of `docs/overview.md`.
