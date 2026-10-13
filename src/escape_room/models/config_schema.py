"""Typed config schema — the contract every loader must satisfy."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LLMConfig(BaseModel):
    backend: Literal["local", "mock", "openai_compat"] = "local"
    model_path: Path = Path("models/gguf/qwen2.5-7b-instruct-q4_k_m.gguf")
    n_ctx: int = Field(8192, ge=512, le=131_072)
    temperature: float = Field(0.85, ge=0.0, le=2.0)
    top_p: float = Field(0.92, gt=0.0, le=1.0)
    max_tokens: int = Field(1024, ge=64, le=32_768)


class GenerationConfig(BaseModel):
    default_theme: str = "abandoned-lab"
    default_difficulty: int = Field(3, ge=1, le=10)
    puzzle_count_min: int = Field(4, ge=1, le=32)
    puzzle_count_max: int = Field(9, ge=1, le=32)
    hint_budget: int = Field(3, ge=0, le=10)
    red_herring_ratio: float = Field(0.2, ge=0.0, le=0.75)

    @field_validator("puzzle_count_max")
    @classmethod
    def _max_ge_min(cls, v: int, info) -> int:
        mn = info.data.get("puzzle_count_min", 1)
        if v < mn:
            raise ValueError("puzzle_count_max must be >= puzzle_count_min")
        return v


class PathsConfig(BaseModel):
    output_dir: Path = Path("rooms/generated")
    vault_dir: Path = Path("puzzles/vault")
    assets_root: Path = Path("assets/rooms")
    log_dir: Path = Path("logs")


class SafetyConfig(BaseModel):
    allow_custom_logic: bool = False
    max_room_bytes: int = Field(2_097_152, ge=4096)
    prompt_sandbox: bool = True


class AppConfig(BaseModel):
    llm: LLMConfig = LLMConfig()
    generation: GenerationConfig = GenerationConfig()
    paths: PathsConfig = PathsConfig()
    safety: SafetyConfig = SafetyConfig()