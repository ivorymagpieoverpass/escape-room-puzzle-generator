"""Puzzle-level models — the atoms every room is built from."""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PuzzleKind(str, Enum):
    LOGIC = "logic"
    CIPHER = "cipher"
    PHYSICAL = "physical"
    OBSERVATION = "observation"
    COOPERATIVE = "cooperative"
    TIMED = "timed"


class Difficulty(int, Enum):
    TRIVIAL = 1
    EASY = 2
    MODERATE = 3
    HARD = 5
    BRUTAL = 8


class Puzzle(BaseModel):
    puzzle_id: str
    kind: PuzzleKind
    title: str = Field(..., min_length=3, max_length=120)
    prompt: str = Field(..., min_length=10, max_length=4000)
    solution: str = Field(..., min_length=1, max_length=512)
    hints: list[str] = Field(default_factory=list, max_length=10)
    difficulty: int = Field(3, ge=1, le=10)
    depends_on: list[str] = Field(default_factory=list)
    props: list[str] = Field(default_factory=list)
    is_red_herring: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("puzzle_id")
    @classmethod
    def _stable_id(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("puzzle_id too short")
        return v

    def fingerprint(self) -> str:
        """Deterministic hash of the solvable core (title/prompt/solution)."""
        blob = f"{self.kind.value}|{self.title}|{self.prompt}|{self.solution}"
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]