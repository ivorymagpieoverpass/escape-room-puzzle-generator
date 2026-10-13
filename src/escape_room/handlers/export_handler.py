"""ExportHandler — read/write room bundles with size + schema guards."""

from __future__ import annotations

import json
from pathlib import Path

from escape_room.models.config_schema import AppConfig
from escape_room.models.room_schema import RoomBundle
from escape_room.utils.logging import get_logger

log = get_logger(__name__)


class ExportError(RuntimeError):
    """Raised on oversized, malformed, or out-of-root room bundles."""


class ExportHandler:
    def __init__(self, config: AppConfig) -> None:
        self._cfg = config
        self._max_bytes = config.safety.max_room_bytes

    def write_room(self, room: RoomBundle, dest: Path) -> Path:
        dest.parent.mkdir(parents=True, exist_ok=True)
        payload = room.model_dump_json(indent=2).encode("utf-8")
        if len(payload) > self._max_bytes:
            raise ExportError(
                f"room bundle {len(payload)}B exceeds max {self._max_bytes}B"
            )
        dest.write_bytes(payload)
        log.info("wrote room %s -> %s (%dB)", room.room_id, dest, len(payload))
        return dest

    def read_room(self, path: Path) -> RoomBundle:
        if not path.exists():
            raise ExportError(f"room not found: {path}")
        raw = path.read_bytes()
        if len(raw) > self._max_bytes:
            raise ExportError(f"room bundle exceeds max size: {path}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ExportError(f"invalid JSON in {path}: {exc}") from exc
        return RoomBundle.model_validate(data)