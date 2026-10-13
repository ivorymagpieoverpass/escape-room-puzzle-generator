"""LLM backends. Register new backends here."""

from __future__ import annotations

from escape_room.services.llm.base import LLMBackend
from escape_room.services.llm.mock_backend import MockBackend

__all__ = ["LLMBackend", "MockBackend"]