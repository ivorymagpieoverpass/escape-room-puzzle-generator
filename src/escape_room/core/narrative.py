"""NarrativeWeaver — stitches puzzle prompts into a coherent room story."""

from __future__ import annotations

import random

from escape_room.models.puzzle_schema import Puzzle
from escape_room.services.llm.base import LLMBackend
from escape_room.services.llm.mock_backend import MockBackend

_THEME_OPENERS: dict[str, str] = {
    "abandoned-lab": "The fluorescents died years ago. Something in here still hums.",
    "haunted-manor": "The floorboards remember every foot that ever crossed them.",
    "cyber-vault": "Cold air, blue light, and a door that wants a password you don't have.",
    "space-station": "Gravity's been off for six hours. The alarms stopped an hour ago.",
    "ancient-tomb": "Sand in your collar. Torchlight on glyphs older than the language you think in.",
}


class NarrativeWeaver:
    def __init__(self, rng: random.Random, backend: LLMBackend | None = None) -> None:
        self._rng = rng
        self._backend = backend or MockBackend()

    def weave(self, theme: str, puzzles: list[Puzzle]) -> str:
        opener = _THEME_OPENERS.get(theme, _THEME_OPENERS["abandoned-lab"])
        beats = [f"- {p.title}: {p.prompt.splitlines()[0]}" for p in puzzles]
        body = "\n".join(beats)
        return f"{opener}\n\n{body}\n\nThe exit is real. So is the time limit."
</thinking>