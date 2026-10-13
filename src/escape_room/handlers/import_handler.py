"""ImportHandler — pull in third-party rooms, clamp paths, sanitize."""

from __future__ import annotations

from pathlib import Path

from escape_room.handlers.export_handler import ExportHandler
from escape_room.models.config_schema import AppConfig
from escape_room.models.room_schema import RoomBundle
from escape_room.utils.logging import get_logger

log = get_logger(__name__)


class ImportHandler:
    def __init__(self, config: AppConfig) -> None:
        self._cfg = config
        self._export = ExportHandler(config)
        self._root = config.paths.assets_root.resolve()

    def import_room(self, source: Path) -> RoomBundle:
        room = self._export.read_room(source)
        for puzzle in room.puzzles:
            for prop in puzzle.props:
                self._assert_within_root(prop)
        log.info("imported %s (%d puzzles)", room.room_id, len(room.puzzles))
        return room

    def _assert_within_root(self, rel_path: str) -> None:
        candidate = (self._root / rel_path).resolve()
        if self._root not in candidate.parents and candidate != self._root:
            raise ValueError(f"prop path escapes assets_root: {rel_path!r}")