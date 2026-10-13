"""Room bundle schema — the top-level artifact written to disk."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from escape_room.models.puzzle_schema import Puzzle


class RoomBundle(BaseModel):
    schema_version: str = "0.4"
    room_id: str
    theme: str
    difficulty: int = Field(3, ge=1, le=10)
    seed: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    narrative: str = Field(..., max_length=8000)
    puzzles: list[Puzzle] = Field(..., min_length=1)
    entry_puzzle_id: str
    exit_puzzle_id: str
    generator_version: str = "0.4.2"

    @field_validator("room_id")
    @classmethod
    def _room_id_shape(cls, v: str) -> str:
        if not v or " " in v:
            raise ValueError("room_id must be non-empty, no spaces")
        return v

    @property
    def total_hints(self) -> int:
        return sum(len(p.hints) for p in self.puzzles)

    def dependency_graph(self) -> dict[str, list[str]]:
        return {p.puzzle_id: list(p.depends_on) for p in self.puzzles}