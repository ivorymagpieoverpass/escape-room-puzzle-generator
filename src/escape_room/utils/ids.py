"""ID helpers — stable, human-scannable room identifiers."""

from __future__ import annotations

import hashlib


def room_id(*, theme: str, seed: int, fingerprint: str) -> str:
    """Stable room id: <theme-slug>-<seed>-<fp6>."""
    slug = "-".join(theme.lower().split())
    short = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[: