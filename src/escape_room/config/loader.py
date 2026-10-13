"""TOML config loader with env-var overrides and strict validation."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from escape_room.models.config_schema import AppConfig


class ConfigError(RuntimeError):
    """Raised when config is missing, malformed, or fails validation."""


def _apply_env_overrides(raw: dict[str, Any]) -> dict[str, Any]:
    """ERPG__SECTION__KEY=value overrides. Values coerced to str."""
    for env_key, env_val in os.environ.items():
        if not env_key.startswith("ERPG__"):
            continue
        parts = env_key.split("__")[1:]
        if len(parts) != 2:
            continue
        section, key = parts[0].lower(), parts[1].lower()
        raw.setdefault(section, {})[key] = env_val
    return raw


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise ConfigError(f"config not found: {path}")
    with path.open("rb") as fh:
        raw = tomllib.load(fh)
    raw = _apply_env_overrides(raw)
    try:
        return AppConfig.model_validate(raw)
    except Exception as exc:  # pydantic ValidationError
        raise ConfigError(f"invalid config at {path}: {exc}") from exc