# Contributing to escape-room-puzzle-generator

Thanks for wanting to help build the room. This is a hobbyist/educational
project for generating AI-driven escape room puzzles, layouts, and hint
chains. Contributions are welcome from puzzle designers, ML tinkerers,
and anyone who's ever hand-authored a red herring.

## Ground rules

- **Python 3.11+** is the target runtime. CI runs on 3.11 and 3.12.
- **No proprietary model weights** committed to the repo. Use the
  `models/` loader and point at your own local GGUF/ONNX file via
  `config/default.toml`.
- **Every generator module ships with a deterministic seed path.** If
  your feature can't reproduce the same room from the same seed, it
  isn't mergeable.
- **Tests are required** for anything under `escape_room/core/` or
  `escape_room/handlers/`. `pytest -q` must pass locally.

## Dev setup

```bash
git clone https://github.com/<you>/escape-room-puzzle-generator.git
cd escape-room-puzzle-generator
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
pytest -q
```

## Adding a new puzzle archetype

1. Drop a module in `escape_room/puzzles/` that subclasses
   `BasePuzzleArchetype`.
2. Register it in `escape_room/puzzles/registry.py` (or use the
   `@register_archetype("your_name")` decorator).
3. Add a fixture room under `tests/fixtures/rooms/` and a test that
   asserts the archetype produces solvable output for seeds 0-99.
4. Update `docs/archetypes.md` if you add new config keys.

## Adding a new LLM backend

Backends live in `escape_room/services/llm/`. Implement the
`LLMBackend` protocol (`generate`, `embed`, `health`). Register in
`escape_room/services/llm/__init__.py`. Do not add network calls that
phone home — this tool runs fully offline by default.

## Style

- `ruff` for lint, `black` for format, `mypy --strict` on `core/` and
  `models/`.
- Type hints on all public functions. `from __future__ import annotations`
  at the top of every module.
- Logging via `escape_room.utils.logging.get_logger(__name__)`, never
  bare `print()` outside `cli/`.

## Code of conduct

Be the kind of contributor whose hints are fair and whose red herrings
are *earned*. Harassment, doxxing, or shipping puzzles that leak
personal data gets you banned.

## PR checklist

- [ ] Tests pass (`pytest -q`)
- [ ] Lint passes (`ruff check .`)
- [ ] Types pass (`mypy escape_room`)
- [ ] Determinism test passes for any new generator
- [ ] `CHANGELOG.md` entry added under `[Unreleased]`