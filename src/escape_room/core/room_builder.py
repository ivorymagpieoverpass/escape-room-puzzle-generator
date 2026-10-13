"""RoomBuilder — orchestrates theme -> puzzle graph -> narrative."""

from __future__ import annotations

import random
from dataclasses import dataclass

from escape_room.core.graph_layout import PuzzleGraph
from escape_room.core.narrative import NarrativeWeaver
from escape_room.models.config_schema import AppConfig
from escape_room.models.room_schema import RoomBundle
from escape_room.puzzles.registry import archetypes_for_theme
from escape_room.utils.ids import room_id
from escape_room.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class BuildRequest:
    theme: str
    difficulty: int
    seed: int


class RoomBuilder:
    """Deterministic room assembler. Same seed => same room, byte-for-byte."""

    def __init__(self, config: AppConfig) -> None:
        self._cfg = config

    def build(self, theme: str, difficulty: int, seed: int) -> RoomBundle:
        rng = random.Random(seed)
        gen = self._cfg.generation

        count = rng.randint(gen.puzzle_count_min, gen.puzzle_count_max)
        archetypes = archetypes_for_theme(theme)
        if not archetypes:
            raise ValueError(f"no archetypes registered for theme={theme!r}")

        graph = PuzzleGraph(rng=rng)
        puzzles = [
            rng.choice(archetypes).instantiate(
                rng=rng, difficulty=difficulty, index=i, hint_budget=gen.hint_budget
            )
            for i in range(count)
        ]
        graph.link(puzzles, red_herring_ratio=gen.red_herring_ratio)

        narrative = NarrativeWeaver(rng=rng).weave(theme=theme, puzzles=puzzles)
        rid = room_id(theme=theme, seed=seed, fingerprint=graph.fingerprint())

        log.info("built room %s: %d puzzles, %d hints", rid, len(puzzles), sum(len(p.hints) for p in puzzles))
        return RoomBundle(
            room_id=rid,
            theme=theme,
            difficulty=difficulty,
            seed=seed,
            narrative=narrative,
            puzzles=puzzles,
            entry_puzzle_id=graph.entry_id,
            exit_puzzle_id=graph.exit_id,
        )