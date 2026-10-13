"""HintRanker — orders hints by usefulness before they hit the room bundle."""

from __future__ import annotations

from escape_room.models.puzzle_schema import Puzzle


class HintRanker:
    """Ranks hints by (short > long) and (specific > vague) heuristics."""

    _VAGUE_MARKERS = ("maybe", "perhaps", "somewhere", "something", "somehow")

    def rank(self, puzzle: Puzzle) -> list[str]:
        return sorted(puzzle.hints, key=self._score, reverse=True)

    def _score(self, hint: str) -> float:
        score = 0.0
        score += max(0.0, 3.0 - len(hint) / 40.0)
        score -= sum(0.5 for m in self._VAGUE_MARKERS if m in hint.lower())
        score += 0.25 * hint.count(" ")  # specifics tend to have more tokens
        return score